# Data Cleaning Summary Report

## File Information
- **Input File:** `311_Service_Requests_20251022.csv`
- **Output File:** `311_Service_Requests_CLEANED_20251022.csv`
- **Script Run Date:** `2025-10-25 14:41:14`

## Initial Data State (Before Cleaning)
- **Initial Row Count:** 199,999
- **Initial Column Count:** 39
- **Duplicate Records (Flagged as DUPLICATE=True):** 5,690


## Cleaning Actions Performed
1.  **Dropped Duplicate Records (Rows where DUPLICATE was True):** 5,690
2.  **Dropped Unlocatable Records (Missing Address/Coords):** 205
3.  **Imputations/Standardizations:** CITY/STATE standardized and imputed, CREATED_DEPARTMENT filled with 'Unknown', ZIP_CODE converted to string.
4.  **Feature Engineering:** Calculated `RESOLUTION_TIME_HOURS` and split `CREATED_DATE` into `CREATED_DATE_PART`/`CREATED_TIME_PART`.

## Final Data State (After Cleaning)
- **Final Row Count:** 194,104
- **Final Column Count:** 36
- **Total Rows Dropped:** 5,895

