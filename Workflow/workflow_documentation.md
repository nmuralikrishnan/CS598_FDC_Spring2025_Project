# Chicago 311 Data Curation - Detailed Workflow Documentation

## Overview
This document describes the complete data curation workflow for the Chicago 311 Service Request dataset, including all detailed processing operations. The workflow follows the USGS Data Lifecycle Model and implements privacy protection through K-anonymity.

## Workflow Visualization

The detailed workflow diagram (`workflow_detailed.png`) shows all individual processing operations performed during data curation. Each box represents a specific operation, and arrows show the data flow.

## Complete Processing Pipeline

```
Raw Sample (199,999 records, 39 columns)
    ↓
┌───────────────────────────────────┐
│   DATA CLEANING OPERATIONS        │
├───────────────────────────────────┤
│ 1. Remove Duplicates  (-5,690)    │
│ 2. Drop Unlocatable   (-205)      │
│ 3. Standardize & Impute           │
│ 4. Feature Engineering            │
└───────────────────────────────────┘
    ↓
Cleaned Dataset (194,104 records, 36 columns)
    ↓
┌───────────────────────────────────┐
│   DE-IDENTIFICATION OPERATIONS    │
├───────────────────────────────────┤
│ 1. Generalize ZIP Code (3-digit)  │
│ 2. Round Coordinates (3 decimals) │
│ 3. Drop Direct Identifiers        │
│ 4. Suppress Records (-263)        │
└───────────────────────────────────┘
    ↓
K-Anonymized Dataset (193,841 records, 28 columns)
    ↓
┌───────────────────────────────────┐
│   ANALYSIS OPERATIONS             │
├───────────────────────────────────┤
│ 1. K-Means Clustering             │
│    (Segmentation Analysis)        │
│ 2. Random Forest Regression       │
│    (Feature Importance)           │
└───────────────────────────────────┘
    ↓
Analysis Results
├─► Cluster Assignments
└─► Feature Importance Rankings
```

## Detailed Processing Stages

### Stage 1: Data Collection and Sampling

**Source:**
- Original dataset: City of Chicago Open Data Portal
- URL: https://data.cityofchicago.org/Service-Requests/311-Service-Requests/v6vf-nfxy
- Access date: December 3, 2025

**Process:**
- Random sampling using `pandas.DataFrame.sample()`
- Sample size: 199,999 records
- Random seed: 42 (for reproducibility)
- Method: `df.sample(n=199999, random_state=42)`

**Output:**
- File: `311_Service_Requests_20251022.csv`
- Location: `Curated Dataset/1_Raw/`
- Records: 199,999
- Columns: 39

**Responsible:** Murali Natarajan (Data Engineer)

---

### Stage 2: Data Cleaning

**Script:** `Data Cleaning/cleanRawData.py`

**Configuration:** `Data Cleaning/config.py`

**Input:**
- `311_Service_Requests_20251022.csv` (199,999 records)

#### Operation 1: Remove Duplicates

**Purpose:** Eliminate duplicate service request records

**Method:**
- Filter records where `DUPLICATE` flag = True
- Drop the filtered records

**Impact:**
- Records removed: 5,690
- Percentage: 2.8% of raw data

**Code:**
```python
df_cleaned = df_cleaned[df_cleaned['DUPLICATE'] == False]
```

#### Operation 2: Drop Unlocatable Records

**Purpose:** Remove records without valid location information

**Method:**
- Identify records missing both `STREET_ADDRESS` AND `LATITUDE`
- Drop these unlocatable records

**Impact:**
- Records removed: 205
- Percentage: 0.1% of raw data

**Code:**
```python
df_cleaned.dropna(subset=['STREET_ADDRESS', 'LATITUDE'], how='all', inplace=True)
```

#### Operation 3: Standardize & Impute

**Purpose:** Standardize field formats and fill missing values

**Operations:**
1. **Date Columns:**
   - Convert `CREATED_DATE`, `LAST_MODIFIED_DATE`, `CLOSED_DATE` to datetime
   - Format: `MM/DD/YYYY HH:MM:SS AM/PM`

2. **Geographic Fields:**
   - `CITY`: Title case, fill missing with 'Chicago'
   - `STATE`: Expand 'IL' to 'Illinois', fill missing with 'Illinois'
   - `ZIP_CODE`: Convert to string, replace missing with 'NA'

3. **Department Field:**
   - `CREATED_DEPARTMENT`: Fill missing with 'Unknown'

**Code:**
```python
# Dates
df_cleaned[col] = pd.to_datetime(df_cleaned[col], errors='coerce')

# Geographic
df_cleaned['CITY'] = df_cleaned['CITY'].str.title().fillna('Chicago')
df_cleaned['STATE'] = df_cleaned['STATE'].replace('IL', 'Illinois').fillna('Illinois')
df_cleaned['ZIP_CODE'] = df_cleaned['ZIP_CODE'].fillna(0).astype(int).astype(str).replace('0', 'NA')

# Department
df_cleaned['CREATED_DEPARTMENT'] = df_cleaned['CREATED_DEPARTMENT'].fillna('Unknown')
```

#### Operation 4: Feature Engineering

**Purpose:** Create new analytical features

**New Features:**

1. **RESOLUTION_TIME_HOURS:**
   - Calculation: `(CLOSED_DATE - CREATED_DATE)` in hours
   - Purpose: Measure service request resolution efficiency
   - Code: `df_cleaned['RESOLUTION_TIME_HOURS'] = (df_cleaned['CLOSED_DATE'] - df_cleaned['CREATED_DATE']).dt.total_seconds() / 3600`

2. **Date/Time Separation:**
   - Split `CREATED_DATE` into:
     - `CREATED_DATE`: Date component only
     - `CREATED_TIME`: Time component only
   - Purpose: Enable temporal analysis

**Column Cleanup:**
- Dropped: `CREATED_HOUR`, `CREATED_DAY_OF_WEEK`, `CREATED_MONTH`, `LEGACY_SR_NUMBER`, `SANITATION_DIVISION_DAYS`
- Reason: Redundant or not needed for analysis

**Output:**
- File: `311_Service_Requests_CLEANED_20251022.csv`
- Location: `Curated Dataset/2_Cleaned/`
- Records: 194,104
- Columns: 36
- Report: `cleaning_summary_report.md`

**Responsible:** Murali Natarajan (Data Engineer)

---

### Stage 3: De-identification (K-Anonymity)

**Script:** `Data Cleaning/deIdentification.py`

**Configuration:** `Data Cleaning/config.py`

**Input:**
- `311_Service_Requests_CLEANED_20251022.csv` (194,104 records)

**Privacy Method:** K-Anonymity with Generalization and Suppression

**K-Anonymity Parameters:**
- **K-threshold:** 5
- **Quasi-Identifiers (QIAs):** COMMUNITY_AREA, WARD, POLICE_DISTRICT, ZIP_CODE

#### Operation 1: Generalize ZIP Code

**Purpose:** Reduce geographic specificity while maintaining utility

**Method:**
- Truncate ZIP codes to first 3 digits
- Example: "60601" → "606"

**Impact:**
- Reduces location precision to broader area
- Maintains regional patterns

**Code:**
```python
df_anonymized['ZIP_CODE'] = df_anonymized['ZIP_CODE'].astype(str).str[:3]
```

#### Operation 2: Round Coordinates

**Purpose:** Generalize precise geographic coordinates

**Method:**
- Round `LATITUDE` and `LONGITUDE` to 3 decimal places
- Precision: ~100 meter resolution
- Example: 41.881832 → 41.882

**Impact:**
- Reduces location precision
- Prevents exact address identification
- Maintains neighborhood-level analysis capability

**Code:**
```python
df_anonymized['LATITUDE'] = df_anonymized['LATITUDE'].round(3)
df_anonymized['LONGITUDE'] = df_anonymized['LONGITUDE'].round(3)
```

**Related Actions:**
- Drop `X_COORDINATE` and `Y_COORDINATE` (redundant high-precision data)

#### Operation 3: Drop Direct Identifiers

**Purpose:** Remove columns containing direct identifiers

**Columns Removed:**
1. `STREET_ADDRESS` - Full street address
2. `STREET_NUMBER` - Building number
3. `STREET_NAME` - Street name
4. `STREET_DIRECTION` - Direction (N, S, E, W)
5. `STREET_TYPE` - Street type (Ave, St, Blvd)
6. `LOCATION` - Combined location string

**Impact:**
- Total columns removed: 6 explicit identifiers + 2 coordinate columns = 8
- Cannot reconstruct exact addresses

#### Operation 4: Suppress Records

**Purpose:** Enforce K-anonymity threshold

**Method:**
1. Group records by QIAs (COMMUNITY_AREA, WARD, POLICE_DISTRICT, ZIP_CODE)
2. Calculate equivalence class size for each group
3. Suppress (remove) records where group size < 5

**Impact:**
- Records suppressed: 263
- Percentage: 0.14% of cleaned data
- **Privacy guarantee:** All remaining records belong to groups of size ≥ 5

**Code:**
```python
# Group and count
equiv_class_counts = df_anonymized.groupby(QIAs).size()

# Suppress small groups
df_anonymized_k = df_anonymized[df_anonymized['COUNT'] >= K_ANONYMITY_THRESHOLD]
```

**Output:**
- File: `311_Service_Requests_K5_ANONYMIZED_GENERALIZED_20251022.csv`
- Location: `Curated Dataset/3_Deidentified/`
- Records: 193,841
- Columns: 28
- Report: `deidentification_summary_report.md`

**Privacy Guarantees:**
- ✅ K-anonymity (k=5) enforced on all records
- ✅ Direct identifiers removed
- ✅ Quasi-identifiers generalized
- ✅ Geographic precision reduced

**Responsible:** Murali Natarajan (Data Engineer)

---

### Stage 4: Data Analysis

**Input:**
- `311_Service_Requests_K5_ANONYMIZED_GENERALIZED_20251022.csv`

Two analytical workflows were performed:

#### Analysis 1: Segmentation (K-Means Clustering)

**Notebook:** `segmentation_model.ipynb`

**Method:** K-Means Clustering (Unsupervised Learning)

**Purpose:**
- Identify natural groupings in service request data
- Discover patterns in request types, locations, and resolution times
- Support targeted service delivery strategies

**Key Parameters:**
- Number of clusters: K
- Random state: Specified for reproducibility

**Outputs:**
- Cluster assignments for each service request
- Cluster characteristics and profiles
- Visualizations of cluster distributions

**Responsible:** Ramitha Kotarkonda (Data Scientist)

#### Analysis 2: Feature Importance (Random Forest)

**Notebook:** `CS_598_Project_Feature_Importance (2).ipynb`

**Method:** Random Forest Regression

**Purpose:**
- Predict service request resolution time
- Identify features that most influence resolution time
- Support resource allocation decisions

**Target Variable:**
- `RESOLUTION_TIME_HOURS`

**Key Parameters:**
- Number of estimators: Specified in notebook
- Max depth: Specified in notebook
- Random state: Specified for reproducibility

**Outputs:**
- Feature importance rankings
- Model performance metrics (R², RMSE)
- Insights into resolution time drivers

**Responsible:** Ramitha Kotarkonda (Data Scientist)

---

## Data Quality Metrics

### Cleaning Stage

| Metric | Value |
|--------|-------|
| Initial records | 199,999 |
| Duplicates removed | 5,690 (2.8%) |
| Unlocatable removed | 205 (0.1%) |
| **Final cleaned records** | **194,104 (97.1%)** |
| Columns reduced | 39 → 36 |

### De-identification Stage

| Metric | Value |
|--------|-------|
| Input records | 194,104 |
| Records suppressed | 263 (0.14%) |
| **Final anonymized records** | **193,841 (99.86%)** |
| Columns reduced | 36 → 28 |
| **Total data retention** | **96.9% of original** |

### Privacy Protection

| Measure | Implementation |
|---------|----------------|
| K-Anonymity | k = 5 (enforced) |
| Quasi-Identifiers | 4 fields |
| Generalized fields | 3 (ZIP, LAT, LONG) |
| Removed identifiers | 8 columns |
| Equivalence classes | All ≥ 5 records |

---

## Computational Environment

**Hardware:**
- Standard laptop/workstation
- Minimum 8GB RAM recommended

**Software:**
- Operating System: Windows 10
- Python: 3.11
- Key packages:
  - pandas 2.1.1
  - numpy 1.26.2
  - matplotlib 3.8.2
  - seaborn 0.12.2
  - jupyterlab 4.2.1

---

*Last Updated: 2025-12-06 20:03:01*  
*Course: CS 598 - Foundations of Data Curation*  
*Institution: University of Illinois at Urbana-Champaign*
