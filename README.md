# Chicago 311 Service Request Data Curation Project

## Overview

This project demonstrates comprehensive data curation practices on Chicago 311 Service Request data, following the USGS Data Lifecycle Model. The workflow includes data collection, cleaning, de-identification using K-anonymity, analysis, and complete provenance documentation.

This README is not the final report. The final report PDF can be viewed in our Coursera submission.

**Course:** CS 598 - Foundations of Data Curation  
**Institution:** University of Illinois at Urbana-Champaign  
**Team:** Murali Natarajan, Ramitha Kotarkonda, Matthew Guan

## Data Source

**Original Dataset:** Chicago 311 Service Requests  
**Source:** City of Chicago Open Data Portal  
**URL:** https://data.cityofchicago.org/Service-Requests/311-Service-Requests/v6vf-nfxy/data_preview  
**License:** Public Domain  
**Access Date:** December 3, 2025


## Project Structure

```
CS598_FDC_Spring2025_Project/
├── Curated Dataset/
│   ├── 1_Raw/                          # Raw sampled data (199,999 records)
│   ├── 2_Cleaned/                      # Cleaned data (194,104 records)
│   └── 3_Deidentified/                 # K-anonymized data (193,841 records)
│
├── Data Cleaning/                      # Processing scripts
│   ├── config.py                       # Configuration parameters
│   ├── cleanRawData.py                 # Data cleaning script
│   └── deIdentification.py             # K-anonymity implementation
│
├── Data Analysis Jupyter Notebooks/    # Analysis notebooks
│   ├── segmentation_model.ipynb        # K-Means clustering
│   └── CS_598_Project_Feature_Importance (2).ipynb
│
├── Metadata/                           # Documentation
│   ├── metadata.json                   # DataCite metadata
│   └── data_dictionary.csv             # Field descriptions
│   └── Codebook.md                     # Codebook

├── Data Models and Abstractions/       # Data models
│   ├── schema.json                     # JSON schema for the curated dataset
│   └── ontology.jsonld                 # Ontology
│
├── Docs/                               # Project reports
│
├── Provenance/                         # Generated provenance (after running scripts)
│   ├── chicago_311_provenance.json     # W3C PROV data
│   ├── chicago_311_provenance.png      # Provenance graph
│   └── provenance_summary.md           # Human-readable summary
│
├── Workflow/                           # Generated workflow (after running scripts)
│   ├── workflow_detailed.png           # Workflow diagram
│   └── workflow_documentation.md       # Workflow guide
│
├── generate_provenance.py              # Provenance generator
├── workflow_diagram.py                 # Workflow diagram generator
├── validate_provenance.py              # Provenance validator
├── run_all_steps.sh                    # Complete automation script
├── requirements.txt                    # Python dependencies
└── README.md                           # This file
```

## Complete Data Pipeline

```
City of Chicago Open Data Portal
    ↓
[1] Data Collection & Sampling (random, n=199,999, seed=42)
    ↓
Raw Dataset (199,999 records, 39 columns)
    ↓
[2] Data Cleaning (cleanRawData.py)
    • Remove duplicates: -5,690
    • Drop unlocatable: -205
    • Standardize fields
    • Feature engineering: RESOLUTION_TIME_HOURS
    ↓
Cleaned Dataset (194,104 records, 36 columns)
    ↓
[3] De-identification (deIdentification.py)
    • K-Anonymity (k=5)
    • Generalize ZIP codes (3-digit)
    • Round coordinates (3 decimals)
    • Drop 8 identifier columns
    • Suppress 263 records
    ↓
K-Anonymized Dataset (193,841 records, 28 columns)
    ↓
[4] Analysis
    • Segmentation (K-Means Clustering)
    • Feature Importance (Random Forest)
    ↓
Analysis Results (Clusters + Feature Rankings)
```

## Quick Start

### Prerequisites
- Python 3.11
- macOS, Linux, or Windows with WSL

### Complete Process (Automated)

Run everything with one command:

```bash
./run_all_steps.sh
```

This script will:
1. Install all dependencies
2. Run data cleaning
3. Run de-identification
4. Run analysis notebooks
5. Generate provenance documentation
6. Generate workflow diagrams

### Manual Steps

**1. Install Dependencies**
```bash
pip install -r requirements.txt
```

**2. Run Data Cleaning**
```bash
cd "Data Cleaning"
python cleanRawData.py
```

**3. Run De-identification**
```bash
python deIdentification.py
cd ..
```

**4. Run Analysis**
```bash
cd "Data Analysis Jupyter Notebooks"
jupyter lab
# Open and run both notebooks
cd ..
```

**5. Generate Documentation**
```bash
python generate_provenance.py
python workflow_diagram.py
```

## Data Quality Metrics

| Stage | Records | Columns | Change |
|-------|---------|---------|--------|
| Raw | 199,999 | 39 | Baseline |
| Cleaned | 194,104 | 36 | -5,895 (-2.9%) |
| K-Anonymized | 193,841 | 28 | -263 (-0.14%) |
| **Total Retention** | **193,841** | **28** | **96.9%** |

### Quality Improvements
- Duplicates removed: 5,690 (2.8%)
- Unlocatable records removed: 205 (0.1%)
- All geographic fields standardized
- New analytical feature created: RESOLUTION_TIME_HOURS

### Privacy Protection
- K-anonymity enforced: k=5
- Quasi-identifiers generalized: 4 fields
- Direct identifiers removed: 8 columns
- All records belong to groups of ≥5

## Key Processing Operations

### Data Cleaning Operations

**1. Duplicate Removal**
- Identified via `DUPLICATE` flag
- Removed: 5,690 records

**2. Unlocatable Records**
- Missing both address and coordinates
- Removed: 205 records

**3. Standardization**
- `CITY`: Title case, fill with 'Chicago'
- `STATE`: Expand to 'Illinois', fill missing
- `ZIP_CODE`: Convert to string, 'NA' for missing
- `CREATED_DEPARTMENT`: Fill with 'Unknown'

**4. Feature Engineering**
- Created `RESOLUTION_TIME_HOURS` = (CLOSED_DATE - CREATED_DATE) in hours
- Split `CREATED_DATE` into date and time components

### De-identification Operations

**1. ZIP Code Generalization**
- Method: Truncate to 3 digits
- Example: "60601" → "606"
- Preserves regional patterns

**2. Coordinate Rounding**
- Method: Round to 3 decimal places (~100m precision)
- Example: 41.881832 → 41.882
- Prevents exact location identification

**3. Identifier Removal**
- Removed: STREET_ADDRESS, STREET_NUMBER, STREET_NAME, STREET_DIRECTION, STREET_TYPE, LOCATION
- Also removed: X_COORDINATE, Y_COORDINATE (redundant)

**4. K-Anonymity Enforcement**
- Threshold: k=5
- QIAs: COMMUNITY_AREA, WARD, POLICE_DISTRICT, ZIP_CODE
- Suppressed 263 records in groups < 5

## Analysis Methods

### Segmentation Analysis (K-Means Clustering)
- **Notebook:** `segmentation_model.ipynb`
- **Purpose:** Identify natural groupings in service requests
- **Method:** K-Means unsupervised learning
- **Input:** K-anonymized dataset
- **Output:** Cluster assignments and characteristics

### Feature Importance Analysis (Random Forest)
- **Notebook:** `CS_598_Project_Feature_Importance (2).ipynb`
- **Purpose:** Predict resolution time and identify key factors
- **Method:** Random Forest regression
- **Target Variable:** RESOLUTION_TIME_HOURS
- **Output:** Feature importance rankings and model performance

## Provenance & Workflow Documentation

### Generated Documentation

After running the scripts, you'll have:

**Provenance Files** (`Provenance/` directory):
- `chicago_311_provenance.json` - W3C PROV-compliant provenance data
- `chicago_311_provenance.png` - Visual provenance graph
- `provenance_summary.md` - Human-readable summary

**Workflow Files** (`Workflow/` directory):
- `workflow_detailed.png` - Detailed workflow diagram
- `workflow_documentation.md` - Complete workflow guide

### What's Documented

**Provenance captures:**
- 15+ entities (datasets, scripts, notebooks, reports)
- 6 activities (collection, cleaning, de-identification, 2 analyses, documentation)
- 7 agents (team members, City of Chicago, UIUC, Python software)
- 50+ relationships (complete data lineage)
- Timestamps for all activities
- Agent attributions

**Workflow captures:**
- All individual processing operations
- Data flow between operations
- Transformation impacts (records affected)
- Analysis methods and results
- Complete reproduction instructions

## Computational Environment

**Hardware:**
- Standard laptop/workstation
- Minimum 8GB RAM
- 1GB free disk space

**Software:**
- Operating System: Windows 10 / macOS / Linux
- Python: 3.11
- Key packages (see requirements.txt):
  - pandas 2.1.1
  - numpy 1.26.2
  - matplotlib 3.8.2
  - seaborn 0.12.2
  - jupyterlab 4.2.1
  - scikit-learn (for analysis)
  - prov 2.0.0 (for provenance)

## Team Contributions

| Team Member | Responsibilities |
|-------------|------------------|
| Murali Natarajan | Data collection, cleaning, de-identification, provenance |
| Ramitha Kotarkonda | Documentation,Segmentation analysis,Reproducabilty  |
| Matthew Guan | Documentation,feature importance modeling, metadata creation, data dictionary, ontology, JSON schema |

## Compliance & Standards

### W3C PROV
- Provenance follows W3C PROV standard
- Machine-readable JSON format
- Interoperable with provenance tools
- Validatable structure

### DataCite
- Metadata follows DataCite schema
- Includes creators, contributors, dates, rights
- Prepared for dataset publication


## Privacy & Ethics

### K-Anonymity Implementation
- **Threshold:** k=5 (industry standard)
- **Method:** Generalization + suppression
- **QIAs:** COMMUNITY_AREA, WARD, POLICE_DISTRICT, ZIP_CODE
- **Guarantee:** All records belong to groups of ≥5



## Citation

If you use this dataset or methodology, please cite:

```bibtex
@dataset{chicago311_2025,
  author = {Natarajan, Murali and Kotarkonda, Ramitha and Guan, Matthew},
  title = {Chicago 311 Service Request Dataset (Curated Sample, K-Anonymized)},
  year = {2025},
  publisher = {University of Illinois at Urbana-Champaign},
  howpublished = {CS 598 - Foundations of Data Curation Project},
  url = {https://data.cityofchicago.org/Service-Requests/311-Service-Requests/v6vf-nfxy/data_preview},
  note = {Derived from City of Chicago Open Data Portal}
}
```
## Terms Of Use

“This site provides applications using data that has been modified for use from its original source, www.cityofchicago.org, the official website of the City of Chicago.  The City of Chicago makes no claims as to the content, accuracy, timeliness, or completeness of any of the data provided at this site.  The data provided at this site is subject to change at any time.  It is understood that the data provided at this site is being used at one’s own risk.”

## Additional Resources

### External Documentation
- **W3C PROV:** https://www.w3.org/TR/prov-overview/
- **DataCite Schema:** https://schema.datacite.org/
- **City of Chicago Data Portal:** https://data.cityofchicago.org/

### Internal Documentation
- Data Dictionary: `Metadata/data_dictionary.csv`
- Metadata: `Metadata/metadata.json`
- Cleaning Report: `Curated Dataset/2_Cleaned/cleaning_summary_report.md`
- De-identification Report: `Curated Dataset/3_Deidentified/deidentification_summary_report.md`

## License

**Original Data:** Public Domain (City of Chicago)  
**This Project:** Educational use (CS 598 course project)  
**Code & Scripts:** Available for academic use

---

**Last Updated:** December 9, 2025  
**Version:** 1.1  
**Status:** Complete
