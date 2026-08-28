from pathlib import Path
import cv2
import torch
import easyocr
from ultralytics import YOLO


def run_2step_ocr_detection():
    # 1. 使用 pathlib 定位專案路徑 (最佳實作)
    # __file__ 為當前腳本路徑: .../06_computer_vision/src/06_computer_vision/yolo_detection_2step_ocr.py
    # 向上退兩層定位到子專案根目錄: .../06_computer_vision/
    project_root = Path(__file__).resolve().parents[2]

    # 尋找圖片目錄 (支援 image 或 img 資料夾名稱)
    img_dir = project_root / "image"
    if not img_dir.exists():
        img_dir = project_root / "img"
        img_dir.mkdir(parents=True, exist_ok=True)

    # 輸入圖片與輸出圖片路徑
    input_image_path = img_dir / "Cars78.png"
    output_image_path = img_dir / "test_car_ocr_detected.jpg"

    # 檢查輸入圖片是否存在
    if not input_image_path.exists():
        raise FileNotFoundError(
            f"找不到目標圖片: {input_image_path}\n請確認圖片是否放置於該路徑。"
        )

    print(f"[*] 專案根目錄: {project_root}")
    print(f"[*] 讀取圖片路徑: {input_image_path}")

    # 2. 尋找並載入 YOLO 模型 (優先載入 best.pt)
    model_candidates = [
        project_root.parent / "best.pt",
        project_root / "best.pt",
        Path("best.pt"),
        project_root / "yolo26n.pt",
        Path("yolo26n.pt"),
    ]
    model_path = next((p for p in model_candidates if p.exists()), Path("best.pt"))
    print(f"[*] 正在載入 YOLO 模型: {model_path} ...")
    model = YOLO(str(model_path))

    # 3. 初始化 EasyOCR 辨識器 (車牌主要由英文字母與數字組成，使用 'en' 辨識)
    use_gpu = torch.cuda.is_available()
    print(f"[*] 正在初始化 EasyOCR 模型 (GPU 加速: {use_gpu})...")
    reader = easyocr.Reader(["en"], gpu=use_gpu)

    # 4. 進行第一階段：YOLO 物件偵測 (定位車牌位置)
    print("[*] [第 1 階段] 進行 YOLO 物件偵測推理...")
    results = model(input_image_path)
    result = results[0]
    boxes = result.boxes

    # 使用 OpenCV 讀取原始圖片以進行裁切與標註繪製
    image = cv2.imread(str(input_image_path))
    if image is None:
        raise RuntimeError(f"無法讀取圖片: {input_image_path}")

    img_h, img_w = image.shape[:2]
    detected_plates = []

    print("\n" + "=" * 60)
    print(f"[*] YOLO 共偵測到 {len(boxes)} 個物件，開始進行車牌裁切與 OCR 辨識...")
    print("=" * 60)

    # 5. 進行第二階段：裁切車牌區域並使用 EasyOCR 辨識車牌號碼
    for i, box in enumerate(boxes, start=1):
        class_id = int(box.cls[0].item())
        class_name = result.names[class_id]
        confidence = float(box.conf[0].item())

        # 取得邊界框座標 (xmin, ymin, xmax, ymax) 並防呆邊界限制
        xyxy = box.xyxy[0].cpu().numpy().astype(int)
        xmin = max(0, xyxy[0])
        ymin = max(0, xyxy[1])
        xmax = min(img_w, xyxy[2])
        ymax = min(img_h, xyxy[3])

        # 裁切車牌區域
        cropped_plate = image[ymin:ymax, xmin:xmax]

        # 儲存裁切出來的車牌影像，方便檢視
        crop_save_path = img_dir / f"test_car_crop_{i}.jpg"
        if cropped_plate.size > 0:
            cv2.imwrite(str(crop_save_path), cropped_plate)

        # 執行 EasyOCR 文字辨識
        ocr_results = reader.readtext(cropped_plate)

        # 解析 OCR 結果，串接辨識到的文字
        recognized_texts = []
        for bbox, text, ocr_conf in ocr_results:
            # 清理文字 (保留英數及常見符號)
            cleaned_text = text.strip().upper()
            if cleaned_text:
                recognized_texts.append(cleaned_text)

        plate_text = " ".join(recognized_texts) if recognized_texts else "UNKNOWN"

        detected_plates.append(
            {
                "index": i,
                "class_name": class_name,
                "confidence": confidence,
                "plate_text": plate_text,
                "bbox": [xmin, ymin, xmax, ymax],
                "crop_path": crop_save_path,
            }
        )

        print(
            f"{i:02d}. 類別: {class_name:<10} | YOLO 信心度: {confidence:.2%} | "
            f"車牌辨識結果: [{plate_text}]"
        )
        print(f"    - 裁切影像已儲存至: {crop_save_path}")

        # 6. 在畫面上繪製邊界框與標籤 (車牌號碼顯示於信心指數上方，上下並排)
        # 繪製邊界框 (綠色，線寬 3)
        cv2.rectangle(image, (xmin, ymin), (xmax, ymax), (0, 255, 0), 3)

        # 標籤分為兩行：上方為車牌辨識結果，下方為類別與信心度
        label_top = f"Plate: {plate_text}"
        label_bottom = f"{class_name} {confidence:.1%}"

        # 計算兩行文字的尺寸以繪製文字背景框
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 0.65
        thickness = 2
        line_gap = 6
        pad_x = 8
        pad_y = 6

        (w1, h1), _ = cv2.getTextSize(label_top, font, font_scale, thickness)
        (w2, h2), _ = cv2.getTextSize(label_bottom, font, font_scale, thickness)
        max_w = max(w1, w2)
        total_h = h1 + h2 + line_gap + pad_y * 2

        # 確保文字背景框不會超出圖片頂部 (若上方空間不足則繪製於框內)
        if ymin - total_h >= 0:
            bg_ymin = ymin - total_h
        else:
            bg_ymin = max(0, ymin)
        bg_ymax = bg_ymin + total_h
        bg_xmin = xmin
        bg_xmax = min(xmin + max_w + pad_x * 2, img_w)

        # 繪製文字背景框 (深藍色底框)
        cv2.rectangle(
            image,
            (bg_xmin, bg_ymin),
            (bg_xmax, bg_ymax),
            (20, 20, 160),
            -1,
        )

        # 繪製第一行文字：車牌號碼 (上方)
        text1_y = bg_ymin + pad_y + h1
        cv2.putText(
            image,
            label_top,
            (bg_xmin + pad_x, text1_y),
            font,
            font_scale,
            (0, 255, 255),  # 黃色高亮顯示車牌
            thickness,
            cv2.LINE_AA,
        )

        # 繪製第二行文字：類別與信心度 (下方)
        text2_y = text1_y + line_gap + h2
        cv2.putText(
            image,
            label_bottom,
            (bg_xmin + pad_x, text2_y),
            font,
            font_scale,
            (255, 255, 255),  # 白色顯示信心度
            thickness,
            cv2.LINE_AA,
        )

    # 7. 儲存標註後的圖片至 image 資料夾
    cv2.imwrite(str(output_image_path), image)
    print("=" * 60)
    print(f"[✓] 兩階段車牌辨識完成！標註圖片已另存至: {output_image_path}")

    # 8. 開啟視窗顯示辨識結果 (可選)
    # cv2.imshow("2-Step YOLO + EasyOCR License Plate Recognition", image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()


if __name__ == "__main__":
    run_2step_ocr_detection()
