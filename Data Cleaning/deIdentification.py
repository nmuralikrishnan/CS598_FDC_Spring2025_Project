import pandas as pd
import os
import sys

# Simple import works because config.py is in the same directory (Project/src)
try:
    import config 
except ImportError:
    print("Import Error: Could not import 'config' module. Please check that 'config.py' is in the same directory.")
    sys.exit(1)

# --- Define paths using config file and Project root ---
try:
    # Determine the script's absolute directory (e.g., /path/to/Project/src)
    script_path = os.path.realpath(__file__)
    script_dir = os.path.dirname(script_path)
    
    # Calculate the Project root directory using the HOME_DIR specified in config.
    project_root = os.path.abspath(os.path.join(script_dir, config.HOME_DIR))

    # Input path: The Cleaned file is the input for the de-identification script.
    CLEANED_FILE_PATH = os.path.join(project_root, config.CLEANED_OUTPUT_PATH, config.CLEANED_OUTPUT_FILENAME)
    
    # Output path for the de-identified file
    DEIDENTIFIED_FILE_PATH = os.path.join(project_root, config.DEIDENTIFID_OUTPUT_PATH, config.DEIDENTIFID_OUTPUT_FILENAME)
    DEIDENTIFICATION_REPORT_PATH = os.path.join(project_root,  config.DEIDENTIFID_OUTPUT_PATH, "deidentification_summary_report.md")

except Exception as e:
    print(f"Path Configuration Error: {e}")
    sys.exit(1)

# --- K-ANONYMITY CONFIGURATION ---
K_ANONYMITY_THRESHOLD = config.K_ANONYMITY_THRESHOLD

# Columns that are retained, generalized, and used to define the equivalence classes (QIAs)
QUASI_IDENTIFIERS = ["COMMUNITY_AREA", "WARD", "POLICE_DISTRICT", "ZIP_CODE"]
# Columns that are too specific and MUST be dropped entirely
EXPLICIT_DROP_COLUMNS = [
    "STREET_ADDRESS",
    "STREET_NUMBER",
    "STREET_NAME",
    "STREET_DIRECTION",
    "STREET_TYPE",
    "LOCATION" 
]
# Columns that will be masked/generalized instead of dropped (Now implicitly handled in the generalization section)
GENERALIZE_COLUMNS = [
    "ZIP_CODE",
    "LATITUDE",
    "LONGITUDE"
]
# -----------------------------------

print(f"Loading cleaned data from: {CLEANED_FILE_PATH}")

# Load the cleaned dataset
try:
    df = pd.read_csv(CLEANED_FILE_PATH)
except FileNotFoundError:
    print(f"Error: Cleaned input file not found at {CLEANED_FILE_PATH}.")
    sys.exit(1)

# --- De-Identification (K-Anonymity) Process ---
initial_record_count = len(df)
initial_columns = df.columns.tolist()

# Drop highly specific identifiers
df_anonymized = df.drop(columns=[col for col in EXPLICIT_DROP_COLUMNS if col in df.columns], errors='ignore')


#  Generalize ZIP_CODE to the first three digits (Area code masking)
if 'ZIP_CODE' in df_anonymized.columns:
    # Retain the first three characters if length is > 3, otherwise treat as 'NA' (if not already handled)
    df_anonymized['ZIP_CODE'] = df_anonymized['ZIP_CODE'].astype(str).str[:3].str.replace('NA', 'NAX')
    
#  Generalize LATITUDE and LONGITUDE (Coordinate Rounding)
coordinate_cols_dropped = []
if 'LATITUDE' in df_anonymized.columns and 'LONGITUDE' in df_anonymized.columns:
    # Round to 3 decimal places (approx. 100 meter resolution)
    df_anonymized['LATITUDE'] = df_anonymized['LATITUDE'].round(3)
    df_anonymized['LONGITUDE'] = df_anonymized['LONGITUDE'].round(3)
    
    # Drop X/Y coordinates as they are redundant high-precision data after rounding
    if 'X_COORDINATE' in df_anonymized.columns:
        df_anonymized.drop(columns=['X_COORDINATE'], errors='ignore', inplace=True)
        coordinate_cols_dropped.append('X_COORDINATE')
    if 'Y_COORDINATE' in df_anonymized.columns:
        df_anonymized.drop(columns=['Y_COORDINATE'], errors='ignore', inplace=True)
        coordinate_cols_dropped.append('Y_COORDINATE')

# Enforce K-anonymity by Suppression on generalized data
# The QIAs must be converted to string for consistent grouping, especially for NaN/NA values
for col in QUASI_IDENTIFIERS:
    if col in df_anonymized.columns:
        df_anonymized[col] = df_anonymized[col].astype(str)

# Calculate the size of each equivalence class (group)
# Use the generalized QIAs to form the groups
valid_qias = [qia for qia in QUASI_IDENTIFIERS if qia in df_anonymized.columns]
if not valid_qias:
    print("ERROR: No valid Quasi-Identifiers found after generalization. Cannot enforce K-anonymity.")
    sys.exit(1)

equiv_class_counts = df_anonymized.groupby(valid_qias).size().reset_index(name='COUNT')

# Merge the counts back into the DataFrame
df_anonymized = df_anonymized.merge(equiv_class_counts, on=valid_qias, how='left')

# Suppress (drop) records where the count is less than K
df_anonymized_k = df_anonymized[df_anonymized['COUNT'] >= K_ANONYMITY_THRESHOLD].copy()

# Drop the temporary count column
df_anonymized_k.drop(columns=['COUNT'], inplace=True)

final_record_count = len(df_anonymized_k)
suppressed_records = initial_record_count - final_record_count
final_columns = df_anonymized_k.columns.tolist()

print(f"K-anonymity (k={K_ANONYMITY_THRESHOLD}) successfully enforced on: {', '.join(valid_qias)} (Generalization + Suppression)")
print(f"Records suppressed to ensure privacy: {suppressed_records:,}")
print(f"Retained records: {final_record_count:,}")

# Save the K-Anonymized and Generalized DataFrame
try:
    # Ensure output directory exists
    output_dir = os.path.dirname(DEIDENTIFIED_FILE_PATH)
    os.makedirs(output_dir, exist_ok=True) 
    
    df_anonymized_k.to_csv(DEIDENTIFIED_FILE_PATH, index=False)
    
    print(f"\nK-Anonymized and Generalized dataset saved successfully to: {DEIDENTIFIED_FILE_PATH}")
    print(f"Final shape of anonymized data: {df_anonymized_k.shape}")
except Exception as e:
    print(f"Error saving anonymized file: {e}")

# --- Generate Final De-identification Report ---

dropped_explicitly = [col for col in EXPLICIT_DROP_COLUMNS if col in initial_columns]
dropped_coords = coordinate_cols_dropped
generalized = ["ZIP_CODE (3-digit mask)", "LATITUDE (Rounded to 3 decimal places)", "LONGITUDE (Rounded to 3 decimal places)"]
qias_used = valid_qias


report_content = f"# De-Identification (K-Anonymity) Summary Report\n\n"
report_content += f"This report summarizes the de-identification process applied to the cleaned service request data to enforce **K-anonymity** and protect privacy.\n\n"
report_content += f"---"

report_content += f"## K-Anonymity Configuration\n"
report_content += f"- **K-Threshold:** $k={K_ANONYMITY_THRESHOLD}$\n"
report_content += f"- **Quasi-Identifiers (QIAs) Used:** {', '.join(qias_used)}\n\n"
report_content += f"---"

report_content += f"## Data Suppression and Retention\n"
report_content += f"| Metric | Before De-identification | After K-Anonymity |\n"
report_content += f"| :--- | :---: | :---: |\n"
report_content += f"| **Total Records** | {initial_record_count:,} | {final_record_count:,} |\n"
report_content += f"| **Records Suppressed** | N/A | {suppressed_records:,} (Records with group size < $k$) |\n"
report_content += f"| **Shape** | {initial_record_count} rows, {len(initial_columns)} cols | {final_record_count} rows, {len(final_columns)} cols |\n\n"
report_content += f"---"

report_content += f"## Generalization and Masking Details\n"
report_content += f"The following columns were **generalized (masked)** to reduce their precision while retaining analytic utility:\n"
report_content += f"| Column | Generalization Method |\n"
report_content += f"| :--- | :--- |\n"
for item in generalized:
     report_content += f"| {item.split(' (')[0]} | {item.split('(')[1].strip(')')} |\n"
report_content += f"\n"

report_content += f"## Columns Removed\n"
report_content += f"The following columns were **removed entirely** as they were direct or high-precision identifiers:\n"
report_content += f"- **Explicitly Dropped:** {', '.join(dropped_explicitly)}\n"
report_content += f"- **Redundant Coordinates Dropped (after generalization):** {', '.join(dropped_coords)}\n"

# Save the de-identification summary report
try:
    with open(DEIDENTIFICATION_REPORT_PATH, 'w') as f:
        f.write(report_content)
    print(f"De-identification summary report saved to: {DEIDENTIFICATION_REPORT_PATH}")
except Exception as e:
    print(f"Error saving de-identification report: {e}")
