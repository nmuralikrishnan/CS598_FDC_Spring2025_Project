#!/bin/bash
# Complete Chicago 311 Data Curation Workflow
# This script runs the entire data processing pipeline from raw data to documentation

set -e  # Exit on error

echo "=========================================="
echo "Chicago 311 Data Curation - Complete Workflow"
echo "=========================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check Python version
echo "Checking Python version..."
python_version=$(python3 --version 2>&1)
echo "Found: $python_version"
echo ""

# Install dependencies
echo "${YELLOW}[1/6] Installing dependencies...${NC}"
pip3 install -r requirements.txt
echo "${GREEN}✓ Dependencies installed${NC}"
echo ""

# Check for Graphviz
echo "Checking for Graphviz..."
if command -v dot &> /dev/null; then
    graphviz_version=$(dot -V 2>&1)
    echo "${GREEN}✓ Graphviz found: $graphviz_version${NC}"
else
    echo "${YELLOW}⚠ Warning: Graphviz not found. Visualizations will not be generated.${NC}"
    echo "To install Graphviz:"
    echo "  - macOS: brew install graphviz"
    echo "  - Ubuntu: sudo apt-get install graphviz"
fi
echo ""

# Step 1: Data Cleaning
echo "${YELLOW}[2/6] Running data cleaning...${NC}"
cd "Data Cleaning"
python3 cleanRawData.py
echo "${GREEN}✓ Data cleaning complete${NC}"
echo ""

# Step 2: De-identification
echo "${YELLOW}[3/6] Running de-identification (K-anonymity)...${NC}"
python3 deIdentification.py
cd ..
echo "${GREEN}✓ De-identification complete${NC}"
echo ""

# Step 3: Analysis
echo "${YELLOW}[4/6] Running analysis notebooks...${NC}"
echo "Note: Analysis notebooks require manual execution in Jupyter Lab"
echo "Skipping automated execution - please run notebooks manually:"
echo "  1. segmentation_model.ipynb"
echo "  2. CS_598_Project_Feature_Importance (2).ipynb"
echo ""
echo "To run analysis:"
echo "  cd 'Data Analysis Jupyter Notebooks'"
echo "  jupyter lab"
echo ""
read -p "Press Enter to continue after running analysis, or Ctrl+C to exit..."
echo ""

# Step 4: Generate Provenance
echo "${YELLOW}[5/6] Generating provenance documentation...${NC}"
python3 generate_provenance.py
echo "${GREEN}✓ Provenance documentation generated${NC}"
echo ""

# Step 5: Generate Workflow
echo "${YELLOW}[6/6] Generating workflow diagrams...${NC}"
python3 workflow_diagram.py
echo "${GREEN}✓ Workflow diagrams generated${NC}"
echo ""

# Summary
echo "=========================================="
echo "${GREEN}✓ Complete Workflow Finished Successfully!${NC}"
echo "=========================================="
echo ""
echo "Generated Files:"
echo ""
echo "Curated Datasets:"
echo "  - Curated Dataset/2_Cleaned/311_Service_Requests_CLEANED_20251022.csv"
echo "  - Curated Dataset/3_Deidentified/311_Service_Requests_K5_ANONYMIZED_GENERALIZED_20251022.csv"
echo ""
echo "Provenance Documentation (Provenance/):"
echo "  - chicago_311_provenance.json"
echo "  - chicago_311_provenance.png"
echo "  - provenance_summary.md"
echo ""
echo "Workflow Documentation (Workflow/):"
echo "  - workflow_detailed.png"
echo "  - workflow_documentation.md"
echo ""
echo "Reports:"
echo "  - Curated Dataset/2_Cleaned/cleaning_summary_report.md"
echo "  - Curated Dataset/3_Deidentified/deidentification_summary_report.md"
echo ""
echo "Next Steps:"
echo "  1. Review Provenance/provenance_summary.md"
echo "  2. Review Workflow/workflow_documentation.md"
echo "  3. View generated PNG diagrams"
echo "  4. Validate provenance: python3 validate_provenance.py"
echo ""
echo "For complete documentation, see:"
echo "  - README.md"
echo "  - DOCUMENTATION.md"
echo ""
