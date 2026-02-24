# ContainerHandle

**ContainerHandle** 是一個專為大氣環境監測數據處理而設計的 Python 專案。它主要用於處理來自不同儀器（如 AE33, SMPS, Nephelometer 等）的原始數據，並提供化學成分、光學性質、粒徑分佈及 VOC 等資料的後續計算與分析功能。

## 專案結構

本專案主要分為兩個核心模組：

### 1. `rawDataReader` (原始數據讀取)
負責讀取各種儀器的原始數據檔案，進行標準化處理（如時間索引、欄位名稱清洗）與數據品管 (QC)。

**支援儀器 / 格式：**
* **氣膠光學：**
  * `AE33`, `AE43` (Aethalometer - 黑碳)
  * `NEPH`, `Aurora` (Nephelometer - 散射)
* **粒徑分佈：**
  * `SMPS` (Scanning Mobility Particle Sizer) - 包含 `SMPS_TH`, `SMPS_aim11`, `SMPS_genr` 等不同型號的 SMPS
  * `APS_3321` (Aerodynamic Particle Sizer)
* **化學成分 / 氣體：**
  * `OCEC` (有機碳/元素碳) - 包含 `OCEC_RES`, `OCEC_LCRES`
  * `TEOM` (質量濃度)
  * `VOC` (揮發性有機物) - 包含 `VOC_TH`, `VOC_ZM`
  * `IGAC` (化學質量) - 包含 `IGAC_TH`, `IGAC_ZM`
* **其他：**
  * `Table`, `EPA_vertical`

### 2. `dataProcess` (數據處理與分析)
對原始數據進行進一步處理與分析的功能。

* **Chemistry (化學模組):**
  * 化學物種質量重建 (Mass Reconstruction)
  * 莫耳濃度轉換 (ug -> umol)
  * ISORROPIA 模型介面 (熱力學平衡計算)
* **Optical (光學模組):**
  * Mie Theory 計算 (`_mie.py`, `_mie_sd.py`)
  * 散射與吸收係數計算 (`_scattering.py`, `_absorption.py`)
  * IMPROVE 公式
* **SizeDistr (粒徑分佈模組):**
  * 粒徑分佈合併演算法 (Merging size distributions)
  * 統計參數計算
* **VOC (揮發性有機物模組):**
  * 生成潛勢計算 (Potential formation)

---

## 安裝與依賴

### 系統需求
* Python 3.x
* Anaconda / Miniconda

### 安裝步驟

本專案提供了一個安裝批次檔 `install.bat`，可自動透過 conda 安裝所需的依賴套件。

1. **Clone 或下載此專案** 到本地端。
2. **執行安裝腳本**：
   在目錄下雙擊 `install.bat` 或在終端機執行：
   ```cmd
   install.bat
   ```

### 依賴套件 (`install.txt`)
主要依賴包括：
* `pandas` (數據處理)
* `scipy` (科學計算)
* `PyMieScatt` (光學 Mie 散射計算)
* `openpyxl` (Excel 讀寫)
* `lxml` (XML/HTML 解析)

---

## 使用範例 (Usage)

### 1. 讀取儀器數據

使用 `rawDataReader` 下的模組來讀取特定儀器的數據。通常每個模組都有一個 `reader` 類別。

```python
from ContainerHandle.rawDataReader import AE33

file_path = r"path/to/your/AE33_data"

# 初始化讀取器
ae33_reader = AE33.reader(file_path)

df_ae33 = ae33_reader()

```

### 2. 數據處理 (化學重組範例)

使用 `dataProcess` 進行分析，例如使用 `Optical` 模組進行米氏散射計算。

```python
import pandas as pd

from ContainerHandle.dataProcess import Optical

file_output_path = r"path/to/your/Mie"
psd_file = r"path/to/your/psd.pkl"
RI_file = r"path/to/your/RI.pkl"


df_psd = pd.read_pickle(psd_file)
df_RI = pd.read_pickle(RI_file)

opt_process = Optical(path_out=file_output_path,
                      excel=False,
                      csv=True)

mie = opt_process.Mie(df_psd, df_RI)
```







