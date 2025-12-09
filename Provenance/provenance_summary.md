# Chicago 311 Service Request Data - Provenance Summary

## Overview
This document provides a human-readable summary of the W3C PROV-compliant provenance 
information for the Chicago 311 Service Request curated dataset.

## Data Lineage

### Source
- **Original Dataset**: Chicago 311 Service Requests from City of Chicago Open Data Portal
- **Access Date**: December 3, 2025
- **URL**: https://data.cityofchicago.org/Service-Requests/311-Service-Requests/v6vf-nfxy
- **License**: Public Domain

### Processing Pipeline

```
Original Dataset (City of Chicago)
    ↓ [Data Collection & Sampling]
Raw Dataset (199,999 records, 39 columns)
    ↓ [Data Cleaning]
Cleaned Dataset (194,104 records, 36 columns)
    ↓ [De-identification]
De-identified Dataset (193,841 records, 28 columns)
    ↓ [Analysis]
Segmentation & Feature Importance Models
```

## Processing Steps

### 1. Data Collection and Sampling 
- **Activity**: Extract sample from original dataset
- **Method**: Random sampling
- **Input**: 311 Service Request dataset
- **Output**: 199,999 records in `311_Service_Requests_20251022.csv`
- **Responsible**: Murali Natarajan

### 2. Data Cleaning
- **Activity**: Clean and standardize data
- **Script**: `cleanRawData.py`
- **Operations**:
  - Removed 5,690 duplicate records
  - Removed 205 unlocatable records (missing address/coordinates)
  - Standardized CITY and STATE fields
  - Imputed missing values (CREATED_DEPARTMENT → 'Unknown')
  - Converted ZIP_CODE to string format
  - Feature engineering: Created RESOLUTION_TIME_HOURS field
  - Split CREATED_DATE into date and time components
- **Input**: 199,999 records, 39 columns
- **Output**: 194,104 records, 36 columns in `311_Service_Requests_CLEANED_20251022.csv`
- **Responsible**: Murali Natarajan
- **Documentation**: `cleaning_summary_report.md`

### 3. De-identification 
- **Activity**: Apply privacy protection through K-anonymity
- **Script**: `deIdentification.py`
- **Privacy Method**: K-Anonymity (k=5) with Generalization and Suppression
- **Quasi-Identifiers Used**: COMMUNITY_AREA, WARD, POLICE_DISTRICT, ZIP_CODE
- **Operations**:
  - Generalized ZIP_CODE to 3-digit prefixes
  - Rounded LATITUDE and LONGITUDE to 3 decimal places (~100m resolution)
  - Removed explicit identifiers: STREET_ADDRESS, STREET_NUMBER, STREET_NAME, etc.
  - Dropped X_COORDINATE and Y_COORDINATE (redundant after rounding)
  - Suppressed 263 records with equivalence class size < 5
- **Input**: 194,104 records, 36 columns
- **Output**: 193,841 records, 28 columns in `311_Service_Requests_K5_ANONYMIZED_GENERALIZED_20251022.csv`
- **Responsible**: Murali Natarajan
- **Documentation**: `deidentification_summary_report.md`

### 4. Data Analysis
Two analytical workflows were performed on the de-identified dataset:

#### 4a. Segmentation Analysis
- **Notebook**: `segmentation_model.ipynb`
- **Method**: K-Means Clustering (Unsupervised Learning)
- **Purpose**: Identify clusters of similar service requests
- **Analyst**: Ramitha Kotarkonda

#### 4b. Feature Importance Analysis
- **Notebook**: `CS_598_Project_Feature_Importance (2).ipynb`
- **Method**: Random Forest Regression
- **Purpose**: Predict resolution time and determine feature importance
- **Analyst**: Mathew Guan

### 5. Documentation and Metadata
- **Activity**: Create comprehensive documentation
- **Outputs**:
  - DataCite-compliant metadata (`metadata.json`)
  - Data dictionary (`data_dictionary.csv`)
  - Processing reports
- **Responsible**: Matthew Guan

## Contributors

### Team (University of Illinois at Urbana-Champaign)
- **Murali Natarajan**
- **Ramitha Kotarkonda**
- **Matthew Guan**

### Data Provider
- **City of Chicago**: Original data source and curator


## Computational Environment

- **Operating System**: Windows/Mac/Linux
- **Programming Language**: Python 3.11
- **Key Libraries**:
  - pandas 2.1.1 (data manipulation)
  - numpy 1.26.2 (numeric computation)
  - matplotlib 3.8.2 (visualization)
  - seaborn 0.12.2 (visualization)
  - jupyterlab 4.2.1 (interactive notebooks)

## Configuration
Centralized configuration managed through `config.py` with parameters for:
- File paths (input, cleaned output, de-identified output)
- K-anonymity threshold (k=5)
- Processing parameters

## Quality Metrics

### Data Quality Improvements
- **Duplicate Removal**: 5,690 records (2.8% of raw data)
- **Completeness**: Removed 205 unlocatable records (0.1%)
- **Standardization**: All CITY, STATE, and ZIP_CODE fields standardized
- **Feature Engineering**: Added RESOLUTION_TIME_HOURS for analysis

### Privacy Protection
- **K-Anonymity**: k=5 threshold enforced on 4 quasi-identifiers
- **Generalization**: ZIP codes and coordinates generalized
- **Suppression**: 263 records (0.14%) suppressed to maintain privacy
- **Explicit Identifier Removal**: 8 columns containing direct identifiers removed

## Data Lifecycle Model
This workflow follows the USGS Data Lifecycle Model:
1. **Plan**: Defined scope and curation strategy
2. **Collect**: Obtained data from City of Chicago Open Data Portal
3. **Process**: Cleaned and de-identified data
4. **Analyze**: Performed clustering and predictive modeling
5. **Preserve**: Version-controlled in Git repository
6. **Share**: Documented with metadata and data dictionary
7. **Reuse**: Prepared for future analysis and reproduction

## Provenance Standards
This provenance documentation follows:
- **W3C PROV**: World Wide Web Consortium Provenance standard
- **DataCite**: Metadata schema for dataset citation and discovery

## Files Generated
- `chicago_311_provenance.json`: PROV-JSON format (machine-readable)
- `chicago_311_provenance.png`: Visual provenance graph
- `provenance_summary.md`: This human-readable summary

---
*Generated on: 2025-12-06 20:02:59*