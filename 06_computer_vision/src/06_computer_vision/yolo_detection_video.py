from pathlib import Path
import cv2
from ultralytics import YOLO


def run_video_detection():
    # 1. 使用 pathlib 定位專案路徑 (最佳實作)
    # __file__ 為當前腳本路徑: .../06_computer_vision/src/06_computer_vision/yolo_detection_video.py
    # 向上退兩層定位到子專案根目錄: .../06_computer_vision/
    project_root = Path(__file__).resolve().parents[2]

    # 尋找影片目錄 (支援 image 或 img 資料夾名稱)
    img_dir = project_root / "image"
    if not img_dir.exists():
        img_dir = project_root / "img"
        img_dir.mkdir(parents=True, exist_ok=True)

    # 輸入影片與輸出影片路徑
    input_video_path = img_dir / "video.mp4"
    output_video_path = img_dir / "video_detected.mp4"

    # 檢查輸入影片是否存在
    if not input_video_path.exists():
        raise FileNotFoundError(
            f"找不到目標影片: {input_video_path}\n請確認影片是否放置於該路徑。"
        )

    print(f"[*] 專案根目錄: {project_root}")
    print(f"[*] 讀取影片路徑: {input_video_path}")

    # 2. 尋找並載入 YOLO 模型 (優先載入 best.pt，若無則依序尋找)
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

    # 3. 初始化 OpenCV 視訊讀取與寫入物件
    cap = cv2.VideoCapture(str(input_video_path))
    if not cap.isOpened():
        raise RuntimeError(f"無法開啟影片檔案: {input_video_path}")

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    print(f"[*] 影片資訊: 解析度 {width}x{height} | FPS: {fps:.2f} | 總影格數: {total_frames}")

    # 設定輸出影片格式 (MP4V)
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    out = cv2.VideoWriter(str(output_video_path), fourcc, fps, (width, height))

    print("[*] 開始進行影片物件偵測推論 (按 'q' 鍵可中斷)...")
    print("=" * 50)

    frame_idx = 0
    try:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            frame_idx += 1

            # 4. 進行物件偵測 (Inference)
            results = model(frame, verbose=False)
            result = results[0]

            # 取得標註後的影格 (含邊界框與標籤)
            annotated_frame = result.plot()

            # 寫入輸出影片
            out.write(annotated_frame)

            # 即時視窗顯示 (可選)
            cv2.imshow("YOLO Video Detection", annotated_frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                print("\n[!] 使用者手動中斷偵測。")
                break

            # 顯示處理進度 (每 30 幀更新一次終端進度)
            if frame_idx % 30 == 0 or frame_idx == total_frames:
                detected_count = len(result.boxes)
                progress = (frame_idx / total_frames * 100) if total_frames > 0 else 0
                print(
                    f"處理進度: [{frame_idx}/{total_frames}] ({progress:.1f}%) | "
                    f"當前影格偵測到 {detected_count} 個物件"
                )

    finally:
        # 5. 釋放資源
        cap.release()
        out.release()
        cv2.destroyAllWindows()

    print("=" * 50)
    print(f"[✓] 影片偵測完成！共處理 {frame_idx} 幀。")
    print(f"[✓] 標註影片已另存至: {output_video_path}")


if __name__ == "__main__":
    run_video_detection()
