"""
Chicago 311 Service Request Data Curation - Provenance Generation
==================================================================
This script generates W3C PROV-compliant provenance documentation for the 
Chicago 311 Service Request data curation workflow using the prov library.

The provenance model captures:
- Entities: Datasets at each stage of curation
- Activities: Data processing steps
- Agents: People and software involved
- Relationships: How entities, activities, and agents are connected

"""

import json
from datetime import datetime
from prov.model import ProvDocument
from prov.dot import prov_to_dot
import os

# Define namespaces
PROV_NS = "http://www.w3.org/ns/prov#"
CHICAGO311_NS = "http://uiuc.edu/cs598fdc/chicago311#"
DATACITE_NS = "http://purl.org/spar/datacite/"
FOAF_NS = "http://xmlns.com/foaf/0.1/"

def create_provenance_document():
    """
    Creates a comprehensive provenance document for the Chicago 311 data curation workflow.
    
    Returns:
        ProvDocument: The complete provenance document
    """
    
    # Initialize the provenance document
    prov_doc = ProvDocument()
    
    # Register namespaces
    prov_doc.set_default_namespace(CHICAGO311_NS)
    prov_doc.add_namespace('prov', PROV_NS)
    prov_doc.add_namespace('datacite', DATACITE_NS)
    prov_doc.add_namespace('foaf', FOAF_NS)
    prov_doc.add_namespace('chicago311', CHICAGO311_NS)
    
    # ========================================
    # AGENTS (People and Software)
    # ========================================
    
    # Research team members
    murali = prov_doc.agent('chicago311:murali_natarajan', {
        'prov:type': 'prov:Person',
        'foaf:name': 'Murali Natarajan',
        'chicago311:role': 'Team Member'
    })
    
    ramitha = prov_doc.agent('chicago311:ramitha_kotarkonda', {
        'prov:type': 'prov:Person',
        'foaf:name': 'Ramitha Kotarkonda',
        'chicago311:role': 'Team Member'
    })
    
    matthew = prov_doc.agent('chicago311:matthew_guan', {
        'prov:type': 'prov:Person',
        'foaf:name': 'Matthew Guan',
        'chicago311:role': 'Team Member'
    })
    
    # Software agents
    python_env = prov_doc.agent('chicago311:python_environment', {
        'prov:type': 'prov:SoftwareAgent',
        'chicago311:version': 'Python 3.11',
        'chicago311:packages': 'pandas 2.1.1, numpy 1.26.2, matplotlib 3.8.2, seaborn 0.12.2'
    })
    
    # External data provider
    city_of_chicago = prov_doc.agent('chicago311:city_of_chicago', {
        'prov:type': 'prov:Organization',
        'foaf:name': 'City of Chicago Open Data Portal',
        'chicago311:role': 'Original Data Provider'
    })
    
    # University affiliation
    uiuc = prov_doc.agent('chicago311:uiuc', {
        'prov:type': 'prov:Organization',
        'foaf:name': 'University of Illinois at Urbana-Champaign',
        'chicago311:department': 'CS 598 Foundations of Data Curation'
    })
    
    # ========================================
    # ENTITIES (Datasets)
    # ========================================
    
    # Original source dataset
    original_dataset = prov_doc.entity('chicago311:original_311_dataset', {
        'prov:type': 'chicago311:OriginalDataset',
        'prov:label': 'Chicago 311 Service Requests - Original Dataset',
        'datacite:identifier': 'https://data.cityofchicago.org/Service-Requests/311-Service-Requests/v6vf-nfxy',
        'chicago311:source': 'City of Chicago Open Data Portal',
        'chicago311:accessDate': '2025-12-03',
        'chicago311:license': 'Public Domain'
    })
    
    # Raw sampled dataset (Stage 1)
    raw_dataset = prov_doc.entity('chicago311:raw_311_dataset', {
        'prov:type': 'chicago311:RawDataset',
        'prov:label': '311 Service Requests - Raw Sample',
        'chicago311:filename': '311_Service_Requests_20251022.csv',
        'chicago311:location': 'Curated Dataset/1_Raw/',
        'chicago311:recordCount': 199999,
        'chicago311:columnCount': 39,
        'chicago311:sampleMethod': 'Random sampling',
        'prov:generatedAtTime': '2025-10-22T00:00:00'
    })
    
    # Cleaned dataset (Stage 2)
    cleaned_dataset = prov_doc.entity('chicago311:cleaned_311_dataset', {
        'prov:type': 'chicago311:CleanedDataset',
        'prov:label': '311 Service Requests - Cleaned',
        'chicago311:filename': '311_Service_Requests_CLEANED_20251022.csv',
        'chicago311:location': 'Curated Dataset/2_Cleaned/',
        'chicago311:recordCount': 194104,
        'chicago311:columnCount': 36,
        'chicago311:duplicatesRemoved': 5690,
        'chicago311:unlocatableRecordsRemoved': 205,
        'prov:generatedAtTime': '2025-10-25T14:41:14'
    })
    
    # De-identified dataset (Stage 3 - Final)
    deidentified_dataset = prov_doc.entity('chicago311:deidentified_311_dataset', {
        'prov:type': 'chicago311:DeidentifiedDataset',
        'prov:label': '311 Service Requests - K-Anonymized',
        'chicago311:filename': '311_Service_Requests_K5_ANONYMIZED_GENERALIZED_20251022.csv',
        'chicago311:location': 'Curated Dataset/3_Deidentified/',
        'chicago311:recordCount': 193841,
        'chicago311:columnCount': 28,
        'chicago311:kAnonymityThreshold': 5,
        'chicago311:recordsSuppressed': 263,
        'chicago311:privacyMethod': 'K-Anonymity with Generalization',
        'prov:generatedAtTime': '2025-10-25T15:00:00'
    })
    
    # Supporting entities - Scripts
    config_script = prov_doc.entity('chicago311:config_script', {
        'prov:type': 'chicago311:ConfigurationFile',
        'prov:label': 'Configuration File',
        'chicago311:filename': 'config.py',
        'chicago311:location': 'Data Cleaning/',
        'chicago311:purpose': 'Centralized configuration for file paths and parameters'
    })
    
    cleaning_script = prov_doc.entity('chicago311:cleaning_script', {
        'prov:type': 'chicago311:ProcessingScript',
        'prov:label': 'Data Cleaning Script',
        'chicago311:filename': 'cleanRawData.py',
        'chicago311:location': 'Data Cleaning/',
        'chicago311:language': 'Python 3.11'
    })
    
    deidentification_script = prov_doc.entity('chicago311:deidentification_script', {
        'prov:type': 'chicago311:ProcessingScript',
        'prov:label': 'De-identification Script',
        'chicago311:filename': 'deIdentification.py',
        'chicago311:location': 'Data Cleaning/',
        'chicago311:language': 'Python 3.11'
    })
    
    # Analysis notebooks
    segmentation_notebook = prov_doc.entity('chicago311:segmentation_notebook', {
        'prov:type': 'chicago311:AnalysisNotebook',
        'prov:label': 'K-Means Clustering Analysis',
        'chicago311:filename': 'segmentation_model.ipynb',
        'chicago311:location': 'Data Analysis Jupyter Notebooks/',
        'chicago311:method': 'K-Means Clustering',
        'chicago311:purpose': 'Identify service request clusters'
    })
    
    feature_importance_notebook = prov_doc.entity('chicago311:feature_importance_notebook', {
        'prov:type': 'chicago311:AnalysisNotebook',
        'prov:label': 'Feature Importance Analysis',
        'chicago311:filename': 'CS_598_Project_Feature_Importance (2).ipynb',
        'chicago311:location': 'Data Analysis Jupyter Notebooks/',
        'chicago311:method': 'Random Forest Regression',
        'chicago311:purpose': 'Predict resolution time and identify important features'
    })
    
    # Reports
    cleaning_report = prov_doc.entity('chicago311:cleaning_report', {
        'prov:type': 'chicago311:Report',
        'prov:label': 'Data Cleaning Summary Report',
        'chicago311:filename': 'cleaning_summary_report.md',
        'chicago311:location': 'Curated Dataset/2_Cleaned/'
    })
    
    deidentification_report = prov_doc.entity('chicago311:deidentification_report', {
        'prov:type': 'chicago311:Report',
        'prov:label': 'De-identification Summary Report',
        'chicago311:filename': 'deidentification_summary_report.md',
        'chicago311:location': 'Curated Dataset/3_Deidentified/'
    })
    
    # Metadata
    metadata_file = prov_doc.entity('chicago311:metadata', {
        'prov:type': 'chicago311:Metadata',
        'prov:label': 'DataCite Metadata',
        'chicago311:filename': 'metadata.json',
        'chicago311:location': 'Metadata/',
        'chicago311:standard': 'DataCite JSON Schema'
    })
    
    data_dictionary = prov_doc.entity('chicago311:data_dictionary', {
        'prov:type': 'chicago311:Documentation',
        'prov:label': 'Data Dictionary',
        'chicago311:filename': 'data_dictionary.csv',
        'chicago311:location': 'Metadata/'
    })
    
    # ========================================
    # ACTIVITIES (Processing Steps)
    # ========================================
    
    # Activity 1: Data Collection and Sampling
    data_collection = prov_doc.activity('chicago311:data_collection_activity', 
        '2025-12-03T00:00:00', 
        '2025-12-03T12:00:00',
        {
            'prov:type': 'chicago311:DataCollection',
            'prov:label': 'Collect and Sample 311 Data',
            'chicago311:description': 'Obtained raw data from City of Chicago Open Data Portal and extracted sample subset using random sampling'
        }
    )
    
    # Activity 2: Data Cleaning
    data_cleaning = prov_doc.activity('chicago311:data_cleaning_activity',
        '2025-10-25T14:00:00',
        '2025-10-25T14:41:14',
        {
            'prov:type': 'chicago311:DataCleaning',
            'prov:label': 'Clean and Standardize Data',
            'chicago311:description': 'Remove duplicates, handle missing values, standardize formats, and engineer features'
        }
    )
    
    # Activity 3: De-identification
    deidentification = prov_doc.activity('chicago311:deidentification_activity',
        '2025-10-25T14:45:00',
        '2025-10-25T15:00:00',
        {
            'prov:type': 'chicago311:DeIdentification',
            'prov:label': 'Apply K-Anonymity and Generalization',
            'chicago311:description': 'Enforce K-anonymity (k=5) through generalization and suppression',
            'chicago311:privacyTechnique': 'K-Anonymity with Generalization'
        }
    )
    
    # Activity 4: Segmentation Analysis
    segmentation_analysis = prov_doc.activity('chicago311:segmentation_activity',
        None,  # Timing not specified in docs
        None,
        {
            'prov:type': 'chicago311:DataAnalysis',
            'prov:label': 'K-Means Clustering Analysis',
            'chicago311:description': 'Identify clusters of similar service requests using unsupervised learning'
        }
    )
    
    # Activity 5: Feature Importance Analysis
    feature_analysis = prov_doc.activity('chicago311:feature_importance_activity',
        None,
        None,
        {
            'prov:type': 'chicago311:DataAnalysis',
            'prov:label': 'Feature Importance Analysis',
            'chicago311:description': 'Predict resolution time and determine feature importance using Random Forest'
        }
    )
    
    # Activity 6: Documentation
    documentation = prov_doc.activity('chicago311:documentation_activity',
        '2025-10-25T00:00:00',
        '2025-12-06T00:00:00',
        {
            'prov:type': 'chicago311:Documentation',
            'prov:label': 'Create Documentation and Metadata',
            'chicago311:description': 'Generate metadata, reports, and data dictionary'
        }
    )
    
    # ========================================
    # RELATIONSHIPS
    # ========================================
    
    # Dataset derivation chain
    prov_doc.wasDerivedFrom(raw_dataset, original_dataset)
    prov_doc.wasDerivedFrom(cleaned_dataset, raw_dataset)
    prov_doc.wasDerivedFrom(deidentified_dataset, cleaned_dataset)
    
    # Activities generating datasets
    prov_doc.wasGeneratedBy(raw_dataset, data_collection)
    prov_doc.wasGeneratedBy(cleaned_dataset, data_cleaning)
    prov_doc.wasGeneratedBy(deidentified_dataset, deidentification)
    prov_doc.wasGeneratedBy(cleaning_report, data_cleaning)
    prov_doc.wasGeneratedBy(deidentification_report, deidentification)
    prov_doc.wasGeneratedBy(metadata_file, documentation)
    prov_doc.wasGeneratedBy(data_dictionary, documentation)
    
    # Activities using datasets/entities
    prov_doc.used(data_collection, original_dataset)
    prov_doc.used(data_cleaning, raw_dataset)
    prov_doc.used(data_cleaning, cleaning_script)
    prov_doc.used(data_cleaning, config_script)
    prov_doc.used(deidentification, cleaned_dataset)
    prov_doc.used(deidentification, deidentification_script)
    prov_doc.used(deidentification, config_script)
    prov_doc.used(segmentation_analysis, deidentified_dataset)
    prov_doc.used(segmentation_analysis, segmentation_notebook)
    prov_doc.used(feature_analysis, deidentified_dataset)
    prov_doc.used(feature_analysis, feature_importance_notebook)
    
    # Agent attributions - who was responsible
    prov_doc.wasAttributedTo(raw_dataset, city_of_chicago)
    prov_doc.wasAttributedTo(cleaned_dataset, murali)
    prov_doc.wasAttributedTo(deidentified_dataset, murali)
    prov_doc.wasAttributedTo(cleaning_script, murali)
    prov_doc.wasAttributedTo(deidentification_script, murali)
    prov_doc.wasAttributedTo(segmentation_notebook, ramitha)
    prov_doc.wasAttributedTo(feature_importance_notebook, matthew)
    prov_doc.wasAttributedTo(metadata_file, matthew)
    prov_doc.wasAttributedTo(data_dictionary, matthew)
    
    # Agent associations with activities
    prov_doc.wasAssociatedWith(data_collection, city_of_chicago)
    prov_doc.wasAssociatedWith(data_collection, murali)
    prov_doc.wasAssociatedWith(data_cleaning, murali, cleaning_script)
    prov_doc.wasAssociatedWith(data_cleaning, python_env)
    prov_doc.wasAssociatedWith(deidentification, murali, deidentification_script)
    prov_doc.wasAssociatedWith(deidentification, python_env)
    prov_doc.wasAssociatedWith(segmentation_analysis, ramitha, segmentation_notebook)
    prov_doc.wasAssociatedWith(feature_analysis, matthew, feature_importance_notebook)
    prov_doc.wasAssociatedWith(documentation, matthew)
    
    # Activity dependencies (workflow sequence)
    prov_doc.wasInformedBy(data_cleaning, data_collection)
    prov_doc.wasInformedBy(deidentification, data_cleaning)
    prov_doc.wasInformedBy(segmentation_analysis, deidentification)
    prov_doc.wasInformedBy(feature_analysis, deidentification)
    
    # Organizational affiliations
    prov_doc.actedOnBehalfOf(murali, uiuc)
    prov_doc.actedOnBehalfOf(ramitha, uiuc)
    prov_doc.actedOnBehalfOf(matthew, uiuc)
    
    return prov_doc


def save_provenance(prov_doc, output_dir='Provenance'):
    """
    Save provenance document in multiple formats.
    
    Args:
        prov_doc: The provenance document to save
        output_dir: Directory to save the files
    """
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Save as PROV-JSON (primary format for querying and integration)
    json_file = os.path.join(output_dir, 'chicago_311_provenance.json')
    with open(json_file, 'w') as f:
        json.dump(json.loads(prov_doc.serialize()), f, indent=2)
    print(f"✓ Saved PROV-JSON format: {json_file}")
    
    # Generate PNG visualization
    try:
        dot = prov_to_dot(prov_doc)
        
        # Save as PNG only (primary visualization format)
        png_file = os.path.join(output_dir, 'chicago_311_provenance.png')
        dot.write_png(png_file)
        print(f"✓ Saved PNG visualization: {png_file}")
        
    except Exception as e:
        print(f"⚠ Warning: Could not generate PNG visualization: {e}")
        print("  To enable visualizations, install: pip install pydot graphviz")
    

def main():
    """
    Main execution function.
    """
    print("=" * 70)
    print("Chicago 311 Service Request Data - Provenance Generation")
    print("=" * 70)
    print()
    
    print("Creating provenance document...")
    prov_doc = create_provenance_document()
    print(f"✓ Provenance document created with {len(list(prov_doc.get_records()))} records")
    print()
    
    print("Saving provenance in multiple formats...")
    save_provenance(prov_doc)
    print()
    
    print("=" * 70)
    print("Provenance generation complete!")
    print("=" * 70)
    print()
    print("Output files saved in the 'Provenance/' directory:")
    print("  - chicago_311_provenance.json (PROV-JSON format)")
    print("  - chicago_311_provenance.png (Visual diagram)")
    print("  - provenance_summary.md (Human-readable summary)")
    print()
    print("To validate the provenance document, you can use:")
    print("  - W3C PROV Validator: https://provenance.ecs.soton.ac.uk/validator/")
    print("  - Or use prov.model's built-in validation")


if __name__ == "__main__":
    main()
