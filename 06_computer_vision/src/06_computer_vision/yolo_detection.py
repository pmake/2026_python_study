from pathlib import Path
from ultralytics import YOLO


def run_detection():
    # 1. 使用 pathlib 定位專案路徑 (最佳實作)
    # __file__ 為當前腳本路徑: .../06_computer_vision/src/06_computer_vision/yolo_detection.py
    # 向上退兩層定位到子專案根目錄: .../06_computer_vision/
    project_root = Path(__file__).resolve().parents[2]

    # 尋找圖片目錄 (支援 image 或 img 資料夾名稱)
    img_dir = project_root / "image"
    if not img_dir.exists():
        img_dir = project_root / "img"
        img_dir.mkdir(parents=True, exist_ok=True)

    # 輸入圖片與輸出圖片路徑
    input_image_path = img_dir / "test_car.jpg"
    output_image_path = img_dir / "test_car_detected.jpg"

    # 檢查輸入圖片是否存在
    if not input_image_path.exists():
        raise FileNotFoundError(
            f"找不到目標圖片: {input_image_path}\n請確認圖片是否放置於該路徑。"
        )

    print(f"[*] 專案根目錄: {project_root}")
    print(f"[*] 讀取圖片路徑: {input_image_path}")

    # 2. 載入 YOLO26 模型 (yolo26n.pt 為輕量奈米版)
    print("[*] 正在載入 YOLO26 模型...")
    model = YOLO("yolo26n.pt")

    # 3. 進行物件偵測 (Inference)
    print("[*] 正在進行物件偵測推理...")
    results = model(input_image_path)

    # 4. 解析並顯示偵測結果
    result = results[0]
    boxes = result.boxes

    print("\n" + "=" * 40)
    print(f"偵測完成！共偵測到 {len(boxes)} 個物件:")
    print("=" * 40)

    for i, box in enumerate(boxes, start=1):
        class_id = int(box.cls[0].item())
        class_name = result.names[class_id]
        confidence = float(box.conf[0].item())
        xyxy = box.xyxy[0].tolist()
        print(
            f"{i:02d}. 類別: {class_name:<12} | 信心度: {confidence:.2%} | "
            f"座標 (xmin, ymin, xmax, ymax): [{xyxy[0]:.1f}, {xyxy[1]:.1f}, {xyxy[2]:.1f}, {xyxy[3]:.1f}]"
        )

    # 5. 儲存標註後的圖片至 img/image 資料夾
    result.save(filename=str(output_image_path))
    print("=" * 40)
    print(f"[✓] 標註圖片已另存至: {output_image_path}")

    # 6. 開啟視窗顯示偵測結果 (可選)
    # result.show()


if __name__ == "__main__":
    run_detection()
