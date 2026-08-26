import json
import os

notebook = {
    "cells": [],
    "metadata": {
        "language_info": {
            "name": "python",
            "version": "3.10.0"
        },
        "orig_nbformat": 4
    },
    "nbformat": 4,
    "nbformat_minor": 2
}

def add_md(content):
    notebook["cells"].append({
        "cell_type": "markdown",
        "metadata": {},
        "source": [line + "\n" for line in content.strip().split("\n")]
    })

def add_code(content):
    notebook["cells"].append({
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [line + "\n" for line in content.strip().split("\n")]
    })

# --- Markdown: Title & Intro ---
add_md("""# 🔬 光譜資料前處理與特徵強化實戰教學 (Spectral Preprocessing)

在近紅外光譜（NIR）、拉曼光譜（Raman）、紅外光譜（FTIR）等光譜辨識領域中，**每筆樣本的「絕對強度」通常受到樣品厚度、表面散射、光源衰減與濃度漂移等物理因素干擾**。
辨識材料的真正核心在於**各波長下的「相對吸收峰比例與光譜形狀（Spectral Fingerprint）」**。

本 Notebook 將帶領你從**虛擬光譜資料的建立**開始，依序示範與視覺化以下光譜常用前處理方法：
1. **原始資料狀態 (Raw Spectra)**：包含基線平移、濃度倍率差異、隨機噪聲
2. **樣本正規化 (Row-wise Normalizer - L2 & Max)**：消除整體能量/厚度差異
3. **標準正態變量變換 (SNV - Standard Normal Variate)**：消除表面散射與基線漂移
4. **多元散射校正 (MSC - Multiplicative Scatter Correction)**：以參考/平均光譜校正散射
5. **Savitzky-Golay 濾波與導數 (SG Smoothing & 1st/2nd Derivative)**：平滑去噪、消除基線與解析重疊峰
6. **PCA 降維降噪效果對比 (Before vs. After Comparison)**：驗證前處理如何顯著提升材質分群與辨識度
""")

# --- Code: Imports & Font Setup ---
add_code("""import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter
from sklearn.preprocessing import Normalizer
from sklearn.decomposition import PCA

# 設定 Matplotlib 中文字型與繪圖風格
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei', 'SimHei', 'Arial', 'sans-serif']
plt.rcParams['axes.unicode_minus'] = False
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
""")

# --- Markdown: Cell 1 Data Generation ---
add_md(r"""---
## 📦 第 0 步：建立虛擬光譜樣本資料 (Synthetic Spectral Data)

我們模擬 **3 種不同材質 (Material A, Material B, Material C)**：
- 每種材質具有**獨特的特徵吸收峰（高斯峰）**。
- 模擬真實測量中的干擾：
  1. **濃度 / 厚度差異**：光譜強度等比例縮放 ($k \in [0.6, 1.8]$)。
  2. **基線漂移 (Baseline Drift)**：由於光學路徑或儀器溫漂造成的線性/二次平移。
  3. **隨機噪聲 (Random Noise)**：感測器熱噪聲。
""")

# --- Code: Data Generation ---
add_code("""# 1. 定義波長範圍 (例如近紅外 900 nm ~ 1700 nm, 共 400 個波長點)
wavelengths = np.linspace(900, 1700, 400)

# 高斯峰函數
def gaussian_peak(x, center, width, height):
    return height * np.exp(-((x - center) ** 2) / (2 * width ** 2))

# 2. 定義 3 種材質的「純淨理想光譜特徵」
pure_A = (gaussian_peak(wavelengths, 1100, 30, 1.2) + 
          gaussian_peak(wavelengths, 1400, 40, 0.8))

pure_B = (gaussian_peak(wavelengths, 1200, 35, 1.0) + 
          gaussian_peak(wavelengths, 1400, 30, 1.1) + 
          gaussian_peak(wavelengths, 1600, 25, 0.6))

pure_C = (gaussian_peak(wavelengths, 1050, 40, 0.7) + 
          gaussian_peak(wavelengths, 1300, 35, 1.3) + 
          gaussian_peak(wavelengths, 1550, 45, 0.9))

pure_materials = {'材質 A': pure_A, '材質 B': pure_B, '材質 C': pure_C}

# 3. 為每種材質產生多筆包含物理干擾的樣本
np.random.seed(42)
samples_per_class = 8
raw_spectra = []
labels = []

for label, pure_spec in pure_materials.items():
    for _ in range(samples_per_class):
        # 物理干擾 1: 濃度/厚度隨機倍率 (0.6 ~ 1.8 倍)
        scale = np.random.uniform(0.6, 1.8)
        
        # 物理干擾 2: 基線平移與傾斜 (線性 + 微二次漂移)
        b0 = np.random.uniform(0.2, 0.8)
        b1 = np.random.uniform(-0.0003, 0.0003) * (wavelengths - 900)
        b2 = np.random.uniform(-0.0000005, 0.0000005) * ((wavelengths - 1300) ** 2)
        baseline = b0 + b1 + b2
        
        # 物理干擾 3: 感測器高斯隨機噪聲
        noise = np.random.normal(0, 0.015, len(wavelengths))
        
        # 合成測量光譜
        measured_spec = scale * pure_spec + baseline + noise
        raw_spectra.append(measured_spec)
        labels.append(label)

raw_spectra = np.array(raw_spectra)
labels = np.array(labels)

print(f"[成功] 虛擬資料生成完成！")
print(f"• 樣本總數: {raw_spectra.shape[0]} 筆 (每種材質 {samples_per_class} 筆)")
print(f"• 特徵維度 (波長點數): {raw_spectra.shape[1]} 個波長點 ({int(wavelengths[0])} ~ {int(wavelengths[-1])} nm)")
""")

# --- Markdown: Raw Data Plot ---
add_md("""---
## 📊 步驟 0：觀察原始光譜 (Raw Spectra)

在原始光譜圖中可以觀察到：
- 同一材質內部因**樣品厚度/濃度倍率不同**與**基線高度不同**，曲線散落在各個高度。
- 視覺上不同材質的曲線完全交錯混雜，很難直接依據絕對吸收值進行分類。
""")

# --- Code: Plot Raw Data ---
add_code("""color_map = {'材質 A': '#1f77b4', '材質 B': '#ff7f0e', '材質 C': '#2ca02c'}

plt.figure(figsize=(12, 5))
for i in range(len(raw_spectra)):
    plt.plot(wavelengths, raw_spectra[i], color=color_map[labels[i]], alpha=0.7, lw=1.5,
             label=labels[i] if i in [0, samples_per_class, samples_per_class*2] else "")

plt.title('【原始光譜】Raw Spectra (含基線漂移、厚度倍率差異與噪聲)', fontsize=14, fontweight='bold', pad=10)
plt.xlabel('波長 (Wavelength, nm)', fontsize=12)
plt.ylabel('吸光度 (Absorbance / Intensity)', fontsize=12)
plt.legend(title='樣本類別', loc='upper right', frameon=True)
plt.tight_layout()
plt.show()
""")

# --- Markdown: Step 1 Normalizer ---
add_md(r"""---
## 📐 步驟 1：樣本正規化 (Row-wise Normalizer)

### 💡 核心原理
`sklearn.preprocessing.Normalizer` 是針對**每筆樣本（Row）**進行獨立縮放，將每條光譜向量長度調為 1：
- **Max Normalization ($norm='max'$)**：每筆光譜除以自身的最大值，將峰值限制在 1。
- **L2 Normalization ($norm='l2'$)**：除以歐幾里得範數 $\sqrt{\sum x_i^2}$，使整體光譜能量一致。

> **效果**：立即消除不同樣本因「濃度/厚度倍率」造成的巨大上下幅度差異！
""")

# --- Code: Step 1 Normalizer ---
add_code("""# 使用 Scikit-Learn 的 Normalizer (分別測試 L2 與 Max)
normalizer_l2 = Normalizer(norm='l2')
spectra_norm_l2 = normalizer_l2.fit_transform(raw_spectra)

normalizer_max = Normalizer(norm='max')
spectra_norm_max = normalizer_max.fit_transform(raw_spectra)

# 繪圖比較
fig, axes = plt.subplots(1, 2, figsize=(16, 5))

for i in range(len(raw_spectra)):
    axes[0].plot(wavelengths, spectra_norm_max[i], color=color_map[labels[i]], alpha=0.7, lw=1.5,
                 label=labels[i] if i in [0, samples_per_class, samples_per_class*2] else "")
axes[0].set_title('1. Max Normalizer (各光譜最高點縮放至 1)', fontsize=13, fontweight='bold')
axes[0].set_xlabel('波長 (nm)')
axes[0].set_ylabel('正規化強度')
axes[0].legend(loc='upper right')

for i in range(len(raw_spectra)):
    axes[1].plot(wavelengths, spectra_norm_l2[i], color=color_map[labels[i]], alpha=0.7, lw=1.5,
                 label=labels[i] if i in [0, samples_per_class, samples_per_class*2] else "")
axes[1].set_title('2. L2 Normalizer (各光譜向量長度縮放至 1)', fontsize=13, fontweight='bold')
axes[1].set_xlabel('波長 (nm)')
axes[1].set_ylabel('正規化強度')
axes[1].legend(loc='upper right')

plt.tight_layout()
plt.show()
""")

# --- Markdown: Step 2 SNV ---
add_md(r"""---
## 🎯 步驟 2：標準正態變量變換 (SNV - Standard Normal Variate)

### 💡 核心原理
SNV 是光譜化學計量學（Chemometrics）中最經典且最常用的前處理方法。
針對**單筆光譜向量 $x$**：
$$z_i = \\frac{x_i - \\bar{x}}{s_x}$$
其中 $\\bar{x}$ 為該筆光譜所有波長點的**平均值**，$s_x$ 為該筆光譜的**標準差**。

> **效果**：
> - **減去平均值**：消除了光譜的整體基線偏移（Baseline Offset）。
> - **除以標準差**：消除了光譜的尺度與散射倍率差異（Scaling/Scatter Effect）。
> - 同材質的光譜會高度重疊聚攏，展現出高度一致的特徵形狀！
""")

# --- Code: Step 2 SNV ---
add_code("""def snv(spectra):
    \"\"\"
    對光譜矩陣執行 Standard Normal Variate (SNV)
    參數 spectra: shape 為 (n_samples, n_wavelengths)
    \"\"\"
    # 對每一列 (樣本) 計算 mean 與 std
    mean = np.mean(spectra, axis=1, keepdims=True)
    std = np.std(spectra, axis=1, keepdims=True)
    return (spectra - mean) / std

# 執行 SNV 轉換
spectra_snv = snv(raw_spectra)

# 繪圖視覺化
plt.figure(figsize=(12, 5))
for i in range(len(raw_spectra)):
    plt.plot(wavelengths, spectra_snv[i], color=color_map[labels[i]], alpha=0.7, lw=1.5,
             label=labels[i] if i in [0, samples_per_class, samples_per_class*2] else "")

plt.title('【SNV 轉換後光譜】Standard Normal Variate (消除基線平移與散射倍率)', fontsize=14, fontweight='bold', pad=10)
plt.xlabel('波長 (nm)', fontsize=12)
plt.ylabel('SNV 標準化吸光度', fontsize=12)
plt.legend(title='樣本類別', loc='upper right', frameon=True)
plt.tight_layout()
plt.show()
""")

# --- Markdown: Step 3 MSC ---
add_md(r"""---
## 🔬 步驟 3：多元散射校正 (MSC - Multiplicative Scatter Correction)

### 💡 核心原理
MSC 假設每筆光譜 $x_i$ 與一條「理想參考光譜」（通常取所有樣本的**平均光譜 $\\bar{x}_{\\text{ref}}$**）之間存在線性關係：
$$x_i = a_i + b_i \\cdot \\bar{x}_{\\text{ref}} + e_i$$
- $a_i$：該樣本的加性偏移（基線平移）
- $b_i$：該樣本的乘性係數（散射/厚度倍率）

透過一元線性回歸求出每筆樣本的 $a_i$ 與 $b_i$ 後，進行校正：
$$x_{i, \\text{corrected}} = \\frac{x_i - a_i}{b_i}$$

> **效果**：將所有光譜校準到同一基準線上，特別適用於顆粒樣品散射造成的干擾。
""")

# --- Code: Step 3 MSC ---
add_code("""def msc(spectra, reference=None):
    \"\"\"
    多元散射校正 (Multiplicative Scatter Correction)
    \"\"\"
    spectra = np.array(spectra)
    if reference is None:
        # 若未指定參考光譜，預設以全體樣本之平均光譜作為參考
        reference = np.mean(spectra, axis=0)
    
    corrected = np.zeros_like(spectra)
    for i in range(spectra.shape[0]):
        # 針對每筆光譜與參考光譜做一元線性回歸 (polyfit degree=1)
        fit = np.polyfit(reference, spectra[i], 1, full=True)
        b = fit[0][0]  # 斜率 (乘性散射係數)
        a = fit[0][1]  # 截距 (加性基線偏移)
        corrected[i] = (spectra[i] - a) / b
        
    return corrected, reference

# 執行 MSC
spectra_msc, ref_spectrum = msc(raw_spectra)

# 繪圖視覺化
plt.figure(figsize=(12, 5))
for i in range(len(raw_spectra)):
    plt.plot(wavelengths, spectra_msc[i], color=color_map[labels[i]], alpha=0.7, lw=1.5,
             label=labels[i] if i in [0, samples_per_class, samples_per_class*2] else "")

# 畫出參考基準光譜
plt.plot(wavelengths, ref_spectrum, color='black', linestyle='--', lw=2, label='參考平均光譜 (Reference)')

plt.title('【MSC 校正後光譜】Multiplicative Scatter Correction (多元散射校正)', fontsize=14, fontweight='bold', pad=10)
plt.xlabel('波長 (nm)', fontsize=12)
plt.ylabel('校正後吸光度', fontsize=12)
plt.legend(title='樣本類別', loc='upper right', frameon=True)
plt.tight_layout()
plt.show()
""")

# --- Markdown: Step 4 Savitzky-Golay ---
add_md(r"""---
## 📈 步驟 4：Savitzky-Golay 濾波與導數 (SG Smoothing, 1st & 2nd Derivative)

### 💡 核心原理
Savitzky-Golay 濾波器利用滑動窗口內的**多項式擬合**，在保留光譜形狀特徵的同時計算平滑值或各階導數：
1. **0 階導數 (SG Smoothing)**：消除感測器高頻隨機雜訊。
2. **1 階導數 (1st Derivative)**：**消除常數基線偏移**（斜率為 0 的平移），將吸收峰頂點轉變為零交叉點（Zero-crossing）。
3. **2 階導數 (2nd Derivative)**：**消除線性傾斜基線**，將寬吸收峰轉換為尖銳的負向谷值，極大提升重疊峰的分辨率（Peak Resolution）！
""")

# --- Code: Step 4 Savitzky-Golay ---
add_code("""# 設定 SG 參數：滑動窗口寬度 window_length (必須為奇數), 多項式階數 polyorder
window = 25
poly = 3

# 1. 平滑 (0階導數)
spectra_sg_smooth = savgol_filter(raw_spectra, window_length=window, polyorder=poly, deriv=0, axis=1)

# 2. 一階導數 (1st Derivative)
spectra_sg_d1 = savgol_filter(raw_spectra, window_length=window, polyorder=poly, deriv=1, axis=1)

# 3. 二階導數 (2nd Derivative)
spectra_sg_d2 = savgol_filter(raw_spectra, window_length=window, polyorder=poly, deriv=2, axis=1)

# 繪製三種 SG 處理結果
fig, axes = plt.subplots(3, 1, figsize=(12, 12), sharex=True)

# 平滑
for i in range(len(raw_spectra)):
    axes[0].plot(wavelengths, spectra_sg_smooth[i], color=color_map[labels[i]], alpha=0.7, lw=1.5)
axes[0].set_title('1. SG 平滑去噪 (0 階導數) - 去除隨機毛刺雜訊', fontsize=12, fontweight='bold')
axes[0].set_ylabel('吸光度')

# 一階導數
for i in range(len(raw_spectra)):
    axes[1].plot(wavelengths, spectra_sg_d1[i], color=color_map[labels[i]], alpha=0.7, lw=1.5)
axes[1].axhline(0, color='gray', linestyle='--', alpha=0.5)
axes[1].set_title('2. SG 一階導數 (1st Derivative) - 消除常數基線平移', fontsize=12, fontweight='bold')
axes[1].set_ylabel('一階導數值')

# 二階導數
for i in range(len(raw_spectra)):
    axes[2].plot(wavelengths, spectra_sg_d2[i], color=color_map[labels[i]], alpha=0.7, lw=1.5,
                 label=labels[i] if i in [0, samples_per_class, samples_per_class*2] else "")
axes[2].axhline(0, color='gray', linestyle='--', alpha=0.5)
axes[2].set_title('3. SG 二階導數 (2nd Derivative) - 消除線性斜率基線，極大幅度增強重疊峰解析度', fontsize=12, fontweight='bold')
axes[2].set_xlabel('波長 (nm)', fontsize=12)
axes[2].set_ylabel('二階導數值')
axes[2].legend(loc='lower right')

plt.tight_layout()
plt.show()
""")

# --- Markdown: Step 5 Comprehensive Comparison & PCA ---
add_md(r"""---
## 🏆 步驟 5：總結全覽與機器學習分群驗證 (PCA 分離度對比)

前處理是否真的有效？最直觀的驗證方式是使用 **主成分分析 (PCA)** 將高維光譜降至 2 維空間，觀察不同材質樣本的**群聚與分離程度**。
""")

# --- Code: Step 5 Summary Dashboard & PCA ---
add_code("""# 1. 彙整所有前處理方法於同一張儀表板中
methods = {
    '1. 原始光譜 (Raw)': raw_spectra,
    '2. L2 Normalizer': spectra_norm_l2,
    '3. SNV 轉換': spectra_snv,
    '4. MSC 校正': spectra_msc,
    '5. SG 二階導數': spectra_sg_d2
}

fig, axes = plt.subplots(3, 2, figsize=(16, 12))
axes = axes.flatten()

for idx, (title, data) in enumerate(methods.items()):
    ax = axes[idx]
    for i in range(len(data)):
        ax.plot(wavelengths, data[i], color=color_map[labels[i]], alpha=0.7, lw=1.2)
    ax.set_title(title, fontsize=12, fontweight='bold')
    ax.set_xlabel('波長 (nm)')

# 隱藏第 6 個空子圖
axes[5].axis('off')
plt.suptitle('【光譜前處理方法全覽比較】', fontsize=16, fontweight='bold', y=0.99)
plt.tight_layout()
plt.show()

# 2. PCA 降維投影對比：原始光譜 vs. SNV vs. SG 2nd Derivative
fig, axes = plt.subplots(1, 3, figsize=(18, 5))

pca_targets = [
    ('原始光譜 (Raw)', raw_spectra),
    ('SNV 轉換後', spectra_snv),
    ('SG 二階導數後', spectra_sg_d2)
]

for idx, (name, data) in enumerate(pca_targets):
    pca = PCA(n_components=2)
    pca_result = pca.fit_transform(data)
    
    ax = axes[idx]
    for lbl in np.unique(labels):
        mask = (labels == lbl)
        ax.scatter(pca_result[mask, 0], pca_result[mask, 1], 
                   color=color_map[lbl], label=lbl, s=70, alpha=0.85, edgecolors='k')
    
    var_exp = np.sum(pca.explained_variance_ratio_) * 100
    ax.set_title(f'{name} PCA 分佈 (解釋變異: {var_exp:.1f}%)', fontsize=13, fontweight='bold')
    ax.set_xlabel('主成分 1 (PC1)')
    ax.set_ylabel('主成分 2 (PC2)')
    ax.legend(title='材質')
    ax.grid(True, linestyle='--', alpha=0.6)

plt.suptitle('【PCA 降維分群效果對比】：前處理使混雜的材質特徵變得清晰可分！', fontsize=15, fontweight='bold', y=1.03)
plt.tight_layout()
plt.show()
""")

# --- Markdown: Conclusion & Cheat Sheet ---
add_md(r"""---
## 📚 總結：光譜前處理方法選擇指南 (Cheatsheet)

| 前處理方法 | 主要解決問題 | 適用場景 | 推薦工具 |
| :--- | :--- | :--- | :--- |
| **Normalizer (L2 / Max)** | 樣品厚度、濃度倍率縮放差異 | 快速將所有光譜能量/幅值調整至相同等級 | `sklearn.preprocessing.Normalizer` |
| **SNV** | 表面顆粒散射 + 總體基線垂直平移 | 固體粉末、片狀樣品近紅外（NIR）與拉曼光譜分析 | 自定義 NumPy 函式 (`(x - mean) / std`) |
| **MSC** | 樣品間散射差異與乘性基線漂移 | 樣本群體具有相似化學骨架、需統一對齊基準時 | 自定義一元回歸函式 (`polyfit`) |
| **SG 平滑 (0階)** | 感測器高頻隨機白雜訊 | 光譜信噪比（SNR）較低時 | `scipy.signal.savgol_filter(deriv=0)` |
| **SG 一階/二階導數** | 複雜基線傾斜漂移、多吸收峰重疊難以區分 | 精細光譜峰位辨識、定量建模前去除基線干擾 | `scipy.signal.savgol_filter(deriv=1/2)` |

> **建議實務工作流 (Best Practice Workflow)**：
> 1. 先用 **SG 平滑 (0階)** 降低噪聲。
> 2. 依樣品型態選用 **SNV** 或 **Normalizer** 消除散射與厚度強度差異。
> 3. 若基線仍有非線性漂移，可進一步結合 **SG 一階或二階導數**。
> 4. 最後接續進行 **PCA 降維** 或 **機器學習分類/迴歸模型**。
""")

output_path = r"c:\Users\User\Desktop\0826\2026_python_study\05_machine_learning\src\05_machine_learning\光譜資料前處理與視覺化-Spectral Preprocessing.ipynb"

with open(output_path, "w", encoding="utf-8") as f:
    json.dump(notebook, f, ensure_ascii=False, indent=2)

print(f"Notebook successfully written to {output_path}")
