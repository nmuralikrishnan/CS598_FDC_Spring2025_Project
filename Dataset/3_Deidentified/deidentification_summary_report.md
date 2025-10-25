# De-Identification (K-Anonymity) Summary Report

This report summarizes the de-identification process applied to the cleaned service request data to enforce **K-anonymity** and protect privacy.

---## K-Anonymity Configuration
- **K-Threshold:** $k=5$
- **Quasi-Identifiers (QIAs) Used:** COMMUNITY_AREA, WARD, POLICE_DISTRICT, ZIP_CODE

---## Data Suppression and Retention
| Metric | Before De-identification | After K-Anonymity |
| :--- | :---: | :---: |
| **Total Records** | 194,104 | 193,841 |
| **Records Suppressed** | N/A | 263 (Records with group size < $k$) |
| **Shape** | 194104 rows, 36 cols | 193841 rows, 28 cols |

---## Generalization and Masking Details
The following columns were **generalized (masked)** to reduce their precision while retaining analytic utility:
| Column | Generalization Method |
| :--- | :--- |
| ZIP_CODE | 3-digit mask |
| LATITUDE | Rounded to 3 decimal places |
| LONGITUDE | Rounded to 3 decimal places |

## Columns Removed
The following columns were **removed entirely** as they were direct or high-precision identifiers:
- **Explicitly Dropped:** STREET_ADDRESS, STREET_NUMBER, STREET_NAME, STREET_DIRECTION, STREET_TYPE, LOCATION
- **Redundant Coordinates Dropped (after generalization):** X_COORDINATE, Y_COORDINATE
