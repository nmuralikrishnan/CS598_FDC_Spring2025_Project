# Base path for the project. All other paths are relative to this directory.
HOME_DIR = ".."

# Input file details
# Full path will be: HOME_DIR/dataset/raw/311_Service_Requests_20251022.csv
INPUT_FILEPATH = "Dataset/1_Raw/"
INPUT_FILENAME = "311_Service_Requests_20251022.csv"

# Cleaned Output file details
# The cleaned file will be saved to: HOME_DIR/dataset/output/311_Service_Requests_CLEANED_20251022.csv
CLEANED_OUTPUT_PATH = "Dataset/2_Cleaned/"
CLEANED_OUTPUT_FILENAME = "311_Service_Requests_CLEANED_20251022.csv"

# De-Identified Output file details
DEIDENTIFID_OUTPUT_PATH = "Dataset/3_Deidentified/"
DEIDENTIFID_OUTPUT_FILENAME = "311_Service_Requests_K5_ANONYMIZED_GENERALIZED_20251022.csv"

# --- K-ANONYMITY CONFIGURATION ---
K_ANONYMITY_THRESHOLD = 5