# ==============================================================================
# YOLO 模型訓練腳本 (YOLO Training Pipeline)
# 作用: 載入預訓練模型並透過遷移學習 (Transfer Learning) 微調自定義資料集。
# ==============================================================================

# [FIRST OCCURRENCE: YOLO class] Ultralytics 核心高階封裝類別。
# - 提供模型載入 (load)、遷移學習訓練 (train)、驗證評估 (val)、推論預測 (predict) 與模型匯出 (export) 等全生命週期介面。
from ultralytics import YOLO

# =========================================================
# 1. 載入模型與權重初始化 (Model Initialization)
# =========================================================
# [FIRST OCCURRENCE: YOLO("...") - 遷移學習 Transfer Learning]
# - 傳入預訓練權重檔 (如 "yolo11n.pt" 或自定義模型名稱)。
# - 機制: 若本地無此檔案，Ultralytics 會自動從官方 GitHub 下載。
# - 原理: 模型已在 COCO 資料集 (百萬張圖片) 上學會提取邊緣、紋理、幾何形狀等通用特徵。
#   我們藉此作為起點進行微調 (Fine-tuning)，大幅減少從零訓練所需的時間與資料量。
model = YOLO("yolo26n.pt")  # 載入輕量級預訓練權重

# =========================================================
# 2. 啟動訓練流程 (Start Model Training)
# =========================================================
# [FIRST OCCURRENCE: model.train()] 封裝 PyTorch 訓練迴圈與反向傳播 (Backpropagation)
# - 自動配置 DataLoader (資料載入器)、Optimizer (預設 AdamW/SGD)、學習率排程器與損失函數 (Loss Functions)。
model.train(
    # [FIRST OCCURRENCE: data] 資料集設定檔路徑
    # - 指向包含 train/val 目錄路徑與類別名稱定義的 data.yaml 檔案。
    data="/content/drive/MyDrive/Colab_YOLO_Practice/data.yaml",
    # [FIRST OCCURRENCE: epochs] 訓練總輪數 (Training Epochs)
    # - 1 個 Epoch 代表神經網路將「整個訓練集」完整看過並更新權重一次。
    # - 100 代表重複學習 100 次。過程中會自動評估驗證集並保存歷史最佳權重 (best.pt)。
    epochs=100,
    # [FIRST OCCURRENCE: imgsz] 輸入影像解析度 (Image Size)
    # - DataLoader 會自動將圖片等比例縮放並透過 Letterbox 補黑邊至 640x640 像素。
    # - 640 是 YOLO 兼顧特徵辨識度與 GPU 推論速度的標準經典尺寸。
    imgsz=640,
    # [FIRST OCCURRENCE: batch] 每批次處理的圖片數量 (Batch Size)
    # - 每次計算梯度並更新神經網路權重時同時送入的圖片張數。
    # - 較大的 Batch 可以使梯度更新更穩定並充分利用 GPU，但會消耗更多顯存 (VRAM)。
    # - 若在 Colab 遇到 CUDA Out of Memory (OOM) 顯存不足錯誤，可調降為 8 或 4。
    batch=16,
    # [FIRST OCCURRENCE: device] 指定運算硬體 (Compute Device)
    # - device=0 代表使用第 1 張 NVIDIA 顯示卡 (CUDA:0) 進行平行硬體加速運算。
    # - 若無 GPU 可設為 'cpu'；多卡環境可設為 [0, 1]。
    device=0,  # 使用 GPU 加速
    # [FIRST OCCURRENCE: name] 訓練實驗專案名稱 (Experiment Name)
    # - 訓練產物（訓練日誌、Loss 與 mAP 曲線圖 results.png、混淆矩陣、以及
    #   最終權重 weights/best.pt 與 weights/last.pt）會自動儲存在Colab的暫存磁碟 /content/runs/detect/yolo26n_car_plate/ 目錄下，瀏覽介面不會顯示content這一層，直接找runs資料夾。
    name="yolo26n_car_plate",
)
