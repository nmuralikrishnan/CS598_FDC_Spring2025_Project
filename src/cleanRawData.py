import pandas as pd
import numpy as np
import os
import sys
import config 

# --- Define paths using config file and Project root ---
try:
    #Determine the script's root directory (Project/src)
    script_dir = os.path.dirname(os.path.realpath(__file__))

    # The Project root is one level up from the script directory (e.g., /path/to/Project)
    project_root = os.path.dirname(script_dir)

    INPUT_FILE_PATH = os.path.join(project_root, config.INPUT_FILEPATH,config.INPUT_FILENAME)
    OUTPUT_FILE_PATH = os.path.join(project_root, config.CLEANED_OUTPUT_PATH , config.CLEANED_OUTPUT_FILENAME)

    REPORT_FILE_PATH = os.path.join(os.path.dirname(config.CLEANED_OUTPUT_PATH), "cleaning_summary_report.md")

except Exception as e:
    print(f"Path Configuration Error: {e}")
    sys.exit(1)

# Load the dataset
try:
    # Assuming the data file is '311_Service_Requests_20251022.csv'
    df_cleaned = pd.read_csv(INPUT_FILE_PATH)
except FileNotFoundError:
    print(f"Error: Input file not found at {INPUT_FILE_PATH}. Please check your config file and directory structure.")
    sys.exit(1)

# --- CAPTURE INITIAL STATS ---
initial_shape = df_cleaned.shape
initial_count = len(df_cleaned)
initial_duplicate_count = 0
if 'DUPLICATE' in df_cleaned.columns:
    # Recapture this essential metric for the report
    initial_duplicate_count = df_cleaned['DUPLICATE'].sum()
else:
    initial_duplicate_count = 0

# --- Define columns for cleaning and type conversion ---
date_columns = ['CREATED_DATE', 'LAST_MODIFIED_DATE', 'CLOSED_DATE']

# Columns to be dropped after processing (DUPLICATE is dropped)
cols_to_drop = ["CREATED_HOUR", "CREATED_DAY_OF_WEEK", "CREATED_MONTH","LEGACY_SR_NUMBER","SANITATION_DIVISION_DAYS"]

df_cleaned.drop(columns=cols_to_drop, inplace=True, errors='ignore')

# Drop records where DUPLICATE is True
if 'DUPLICATE' in df_cleaned.columns:
    df_cleaned = df_cleaned[df_cleaned['DUPLICATE'] == False].reset_index(drop=True)

# Convert date/time columns to datetime objects (MUST be done before extracting time)
for col in date_columns:
    # errors='coerce' turns invalid/missing date strings into NaT (Not a Time)
    df_cleaned[col] = pd.to_datetime(df_cleaned[col], errors='coerce', format='%m/%d/%Y %I:%M:%S %p')

for col in date_columns:
    if col in df_cleaned.columns and not pd.api.types.is_datetime64_any_dtype(df_cleaned[col]):
        print(f"Validation Error: Column '{col}' failed to convert to datetime and is still type {df_cleaned[col].dtype}.")
        # If the conversion failed, we exit gracefully instead of causing an AttributeError later.
        sys.exit(1)


# Fill CREATED_DEPARTMENT with 'Unknown' 
df_cleaned['CREATED_DEPARTMENT'] = df_cleaned['CREATED_DEPARTMENT'].fillna('Unknown')

# Convert ID/Code columns
# ZIP_CODE Replacing NaN with 'NA'
df_cleaned['ZIP_CODE'] = df_cleaned['ZIP_CODE'].fillna(0).astype(int).astype(str).replace('0', 'NA')


# Standardize CITY and STATE casing and abbreviations
df_cleaned['CITY'] = df_cleaned['CITY'].str.title()
df_cleaned['STATE'] = df_cleaned['STATE'].replace('IL', 'Illinois')
df_cleaned['CITY'] = df_cleaned['CITY'].fillna('Chicago')
df_cleaned['STATE'] = df_cleaned['STATE'].fillna('Illinois')

# Drop rows where both STREET_ADDRESS and LATITUDE are missing (unlocatable records)
pre_location_drop_rows = len(df_cleaned)
df_cleaned.dropna(subset=['STREET_ADDRESS', 'LATITUDE'], how='all', inplace=True)
location_dropped_rows = pre_location_drop_rows - len(df_cleaned)


#Calculate Resolution Time (for Completed requests)
df_cleaned['RESOLUTION_TIME'] = df_cleaned['CLOSED_DATE'] - df_cleaned['CREATED_DATE']
df_cleaned['RESOLUTION_TIME_HOURS'] = df_cleaned['RESOLUTION_TIME'].dt.total_seconds() / 3600
df_cleaned.drop(columns=['RESOLUTION_TIME'], inplace=True)

#Split CREATED_DATE into separate Date and Time columns.
df_cleaned['CREATED_TIME'] = df_cleaned['CREATED_DATE'].dt.time.astype(str)
df_cleaned['CREATED_DATE'] = df_cleaned['CREATED_DATE'].dt.date.astype(str)


# Save the final cleaned DataFrame to a new file
df_cleaned.to_csv(OUTPUT_FILE_PATH, index=False)


# --- CAPTURE FINAL STATS ---
final_shape = df_cleaned.shape
total_dropped_rows = initial_shape[0] - final_shape[0]

# --- Generate Cleaning Report ---
# REPORT_FILENAME = 'cleaning_summary_report.md'
# REPORT_DIR = os.path.dirname(OUTPUT_FILE_PATH)
# REPORT_FILE_PATH = os.path.join(REPORT_DIR, REPORT_FILENAME)

report_content = f"""# Data Cleaning Summary Report

## File Information
- **Input File:** `{os.path.basename(INPUT_FILE_PATH)}`
- **Output File:** `{os.path.basename(OUTPUT_FILE_PATH)}`
- **Script Run Date:** `{pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}`

## Initial Data State (Before Cleaning)
- **Initial Row Count:** {initial_shape[0]:,}
- **Initial Column Count:** {initial_shape[1]:,}
- **Duplicate Records (Flagged as DUPLICATE=True):** {initial_duplicate_count:,}


## Cleaning Actions Performed
1.  **Dropped Duplicate Records (Rows where DUPLICATE was True):** {initial_duplicate_count:,}
2.  **Dropped Unlocatable Records (Missing Address/Coords):** {location_dropped_rows:,}
3.  **Imputations/Standardizations:** CITY/STATE standardized and imputed, CREATED_DEPARTMENT filled with 'Unknown', ZIP_CODE converted to string.
4.  **Feature Engineering:** Calculated `RESOLUTION_TIME_HOURS` and split `CREATED_DATE` into `CREATED_DATE_PART`/`CREATED_TIME_PART`.

## Final Data State (After Cleaning)
- **Final Row Count:** {final_shape[0]:,}
- **Final Column Count:** {final_shape[1]:,}
- **Total Rows Dropped:** {total_dropped_rows:,}

"""

# Write the report file
with open(REPORT_FILE_PATH, 'w') as f:
    f.write(report_content)

print(f"Cleaning summary report saved to: {REPORT_FILE_PATH}")
# ------------------------------------

print(f"Data cleaning complete. The final cleaned dataset has been saved to: {OUTPUT_FILE_PATH}")
