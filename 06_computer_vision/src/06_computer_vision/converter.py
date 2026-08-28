"""
Pascal VOC (XML) 轉 AnyLabeling (JSON) 轉換工具
作用: 將指定資料夾中的所有 VOC .xml 標註檔案轉換為 AnyLabeling 相容的 .json 標註檔。
預設將2026_python_study\training_samples資料夾中的所有 xml 格式annotation檔案轉換為 json 格式，並將結果儲存在2026_python_study\training_samples\converted資料夾中。
"""

import argparse
import json
from pathlib import Path
import xml.etree.ElementTree as ET

# 預設標籤對照表 (可依照專案需求擴充或修改)
# 例如: 將 XML 中的 'licence' 或 'license' 自動對照為 AnyLabeling 的 'car_plate'
DEFAULT_LABEL_MAPPING = {
    "licence": "car_plate",
    "license": "car_plate",
}


def xml_to_anylabeling_json(
    xml_path: Path,
    output_json_path: Path | None = None,
    label_mapping: dict[str, str] | None = None,
) -> Path:
    """將單一 Pascal VOC XML 檔案轉換為 AnyLabeling JSON 格式。

    :param xml_path: XML 檔案路徑
    :param output_json_path: 輸出的 JSON 檔案路徑 (若為 None 則輸出在同資料夾下同名 .json)
    :param label_mapping: 類別名稱對照表字典
    :return: 產生的 JSON 檔案路徑
    """
    if label_mapping is None:
        label_mapping = DEFAULT_LABEL_MAPPING

    if output_json_path is None:
        output_json_path = xml_path.with_suffix(".json")

    # 1. 解析 XML 內容
    tree = ET.parse(xml_path)
    root = tree.getroot()

    # 2. 取得圖片名稱 (若無則預設為同名的 .png 檔)
    filename_elem = root.find("filename")
    if filename_elem is not None and filename_elem.text:
        image_path = filename_elem.text.strip()
    else:
        image_path = f"{xml_path.stem}.png"

    # 3. 取得圖片尺寸
    size_elem = root.find("size")
    if size_elem is not None:
        image_width = int(float(size_elem.findtext("width", "0")))
        image_height = int(float(size_elem.findtext("height", "0")))
    else:
        image_width = 0
        image_height = 0

    # 4. 解析所有標註物件 (<object>)
    shapes = []
    for obj in root.iter("object"):
        raw_name = obj.findtext("name", "").strip()
        # 套用類別名稱對照 (若無對照則保留原名稱)
        label = label_mapping.get(raw_name, raw_name)

        bndbox = obj.find("bndbox")
        if bndbox is None:
            continue

        xmin = float(bndbox.findtext("xmin", "0"))
        ymin = float(bndbox.findtext("ymin", "0"))
        xmax = float(bndbox.findtext("xmax", "0"))
        ymax = float(bndbox.findtext("ymax", "0"))

        shapes.append(
            {
                "label": label,
                "text": "",
                "points": [[xmin, ymin], [xmax, ymax]],
                "group_id": None,
                "shape_type": "rectangle",
                "flags": {},
            }
        )

    # 5. 組裝 AnyLabeling 格式字典
    json_data = {
        "version": "0.4.36",
        "flags": {},
        "shapes": shapes,
        "imagePath": image_path,
        "imageData": None,
        "imageHeight": image_height,
        "imageWidth": image_width,
    }

    # 6. 寫入 JSON 檔案
    output_json_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_json_path, "w", encoding="utf-8") as f:
        json.dump(json_data, f, indent=2, ensure_ascii=False)

    return output_json_path


def convert_folder(
    input_dir: str | Path,
    output_dir: str | Path | None = None,
    label_mapping: dict[str, str] | None = None,
) -> int:
    """批次將資料夾內所有 .xml 檔案轉換為 AnyLabeling .json 格式。

    :param input_dir: 包含 .xml 檔案的資料夾路徑
    :param output_dir: 輸出 .json 的資料夾 (預設為 input_dir 下的 'converted' 子資料夾)
    :param label_mapping: 類別名稱對照表字典
    :return: 成功轉換的檔案總數
    """
    input_path = Path(input_dir).resolve()
    # 預設輸出在 input_dir 底下的 converted 資料夾
    output_path = (
        Path(output_dir).resolve() if output_dir else input_path / "converted"
    )

    if not input_path.exists():
        raise FileNotFoundError(f"找不到指定的輸入資料夾: {input_path}")

    xml_files = sorted(list(input_path.glob("*.xml")))
    if not xml_files:
        print(f"[*] 在目錄中未找到任何 .xml 檔案: {input_path}")
        return 0

    # 確保輸出資料夾存在
    output_path.mkdir(parents=True, exist_ok=True)

    print(f"[*] 開始轉換目錄: {input_path}")
    print(f"[*] 找到 {len(xml_files)} 個 .xml 標註檔...")
    print(f"[*] 輸出目錄: {output_path}")
    print("=" * 50)

    success_count = 0
    for xml_file in xml_files:
        target_json = output_path / f"{xml_file.stem}.json"
        try:
            xml_to_anylabeling_json(xml_file, target_json, label_mapping)
            print(f"  [✓] {xml_file.name:<20} -> {target_json.name}")
            success_count += 1
        except Exception as e:
            print(f"  [✗] {xml_file.name:<20} 轉換失敗: {e}")

    print("=" * 50)
    print(
        f"[✓] 轉換完成！成功處理 {success_count}/{len(xml_files)} 個檔案。"
    )
    print(f"[*] 輸出位置: {output_path}")
    return success_count


def main():
    # 使用 pathlib 定位專案根目錄與預設資料夾路徑
    script_dir = Path(__file__).resolve()
    # parents[3] 為工作區根目錄 2026_python_study
    workspace_root = script_dir.parents[3]
    # parents[2] 為子專案目錄 06_computer_vision
    subproject_root = script_dir.parents[2]

    # 優先選擇工作區根目錄下的 training_samples，若不存在則檢查子專案目錄
    if (workspace_root / "training_samples").exists():
        default_dir = workspace_root / "training_samples"
    else:
        default_dir = subproject_root / "training_samples"

    default_output_dir = default_dir / "converted"

    parser = argparse.ArgumentParser(
        description="將 Pascal VOC XML 標註檔轉為 AnyLabeling JSON 格式"
    )
    parser.add_argument(
        "--dir",
        "-d",
        type=str,
        default=str(default_dir),
        help=f"指定要轉換的資料夾路徑 (預設: {default_dir})",
    )
    parser.add_argument(
        "--output",
        "-o",
        type=str,
        default=str(default_output_dir),
        help=f"指定輸出 JSON 資料夾路徑 (預設: {default_output_dir})",
    )

    args = parser.parse_args()
    convert_folder(input_dir=args.dir, output_dir=args.output)




if __name__ == "__main__":
    main()
