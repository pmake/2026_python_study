# 06 Computer Vision

電腦視覺學習專案 (Computer Vision Learning Project)
## 常用模型
### 視覺
- 以下三者樣本成本、訓練成本、推論成本(推理速度)由低到高排序:
    1. Image Classification
    2. Object Detection
    3. Object Segmentation
- Image Classification
    - 影像分類是將整張影像分成不同的類別。
- Object detection
    - 物件偵測是用「矩形框（Bounding Box）」框出影像中特定物體的位置(四個邊界)，以及類別。
    - 使用YOLO演算法進行物件偵測
        - 核心概念：YOLO (You Only Look Once) 是一種即時物件偵測系統，它將物件偵測視為一個迴歸問題，直接預測物件的位置和類別，而不是先生成候選框再分類。
        - 應用例:
            - 車牌辨識: 先用Yolo 定位車牌位置截取車牌影像, 再用OCR辨識小區塊的車牌文字
        - 訓練步驟:
            1. 收集標註好的車牌影像資料集，包含車牌的位置和類別。
                - 就像是設計一本參考書讓模型讀，讀了以後要去參加考試，所以參考書應該要儘量囊括所有可能出現的題型。
                - 比如要定位車牌位置，就要考慮不同的角度、光線、車牌樣式(中英文日韓泰等)等。
                - 為特定的攝影機配置做優化有好有壞:
                    - 好處: 可以以較少的樣本提高模型的準確率、召回率、F1分數等指標。
                    - 壞處: 無法泛化到其他攝影機配置。
            2. 選擇合適的YOLO版本，例如YOLOv5、YOLOv7、YOLOv8等。
                - 
            3. 使用標註好的資料集對YOLO模型進行訓練，以提高其辨識準確率。
            4. 使用測試集對訓練好的YOLO模型進行評估，計算其準確率、召回率、F1分數等指標。
            5. 使用模型部署工具，將訓練好的YOLO模型部署到生產環境中，用於預測新的資料。
        - 模型選擇:
            - Ultralytics YOLO
                - Ultralytics 是一個開源的人工智慧公司, 主要開發 YOLO 演算法的各種模型。
- Object Segmentation
    - 影像分割則是精確到「每一個像素（Pixel-level Mask）」去勾勒物體的輪廓。
## 標記工具
### anylabeling
- GitHub: https://github.com/anylabeling/anylabeling
- 此工具標記時，標記檔格式為.json檔案，和圖片是1對1的關係。
    - 可匯出為多種格式，例如YOLO格式的純文字檔、COCO格式的JSON檔等。

## YOLO 訓練實作流程
### Google colab
    - 先將anylabeling標記完成的圖片和標註檔上傳至Google Drive中
        - classes.txt
        - train
            - images
            - labels
        - val
            - images
            - labels
        - test
            - images
            - labels
        - data.yaml
    - 至 https://colab.research.google.com/
    - 建立一個新的筆記本
        - 完成的lab: https://colab.research.google.com/drive/1b2vVANuQRNAAjD8cT7jOfSUxjJvPHZBP#scrollTo=X4M5Y7iIyNHI
    - 點擊右上角"連線"按钮旁邊的下三角icon，選擇變更執行階段類型，硬體加速器選擇TPU或GPU類型，點擊儲存，然後點擊"連線"按鈕等待取得分配的運算資源
    - 點擊左側的資料夾圖示/掛接雲端硬碟/選擇帳戶 讓Colab取得Google Drive存取權
        - 點擊左側的資料夾圖示，會出現Google Drive的資料夾與檔案
        - 透過介面瀏覽需要的檔案位置，然後點擊介面右側的3個小點，選擇複製路徑(Copy path)，取得檔案或資料夾路徑
    - 編輯data.yaml檔案，使用正確的路徑代入對應的欄位，欄位說明參考"2026_python_study\06_computer_vision\src\06_computer_vision\data.yaml"檔案說明
    - 至此訓練前的準備都已完成, 只需執行以下程式碼即可開始訓練
    - 先在Colab 環境安裝ultralytics套件:
        - 新增一個程式碼區塊並輸入以下指令:
        - pip install ultralytics
    - 撰寫訓練用程式碼:
        - 新增一個程式碼區塊並複製"2026_python_study\06_computer_vision\src\06_computer_vision\yolo_train.py"裡面的程式碼到此程式碼區塊中，並點擊執行開始訓練。
    - 訓練完成後，結果會自動儲存在Colab的暫存磁碟"/content/runs/detect"裡面
    - 檢視參數評估結果，不滿意可修改data.yaml檔案的相關參數重新訓練。
        - 增加樣本數才是提升準確率最有效的方法。
    - "/content/runs/detect/yolo26n_car_plate/weights/best.pt" 檔案即為訓練好的模型檔，可點擊右側3個小點選擇下載，即可應用於推論。
        - 如果訓練多次則會有多個"yolo26n_car_plate-<n>"資料夾，<n>代表第幾次訓練
        - 將yolo_detection.py裡的"model = YOLO("yolo26n.pt")"改為"model = YOLO("best.pt")"，然後執行yolo_detection.py，即可應用於推論。
    
    
