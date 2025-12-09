"""
Chicago 311 Data Curation - Workflow Diagram Generator (Streamlined)
====================================================================
This script creates a detailed workflow diagram showing all data processing 
operations in the curation pipeline.

"""

from prov.model import ProvDocument
from prov.dot import prov_to_dot
import os

def create_detailed_processing_workflow():
    """
    Create a detailed diagram showing all processing steps and transformations.
    """
    
    workflow = ProvDocument()
    workflow.set_default_namespace("http://uiuc.edu/cs598fdc/chicago311#")
    workflow.add_namespace('prov', 'http://www.w3.org/ns/prov#')
    
    # Input
    raw = workflow.entity('raw', {
        'prov:label': 'Raw Sample\n(199,999 records)',
    })
    
    # Cleaning operations
    dedup = workflow.activity('clean_remove_duplicates', None, None, {
        'prov:label': 'Remove\nDuplicates\n(-5,690)',
    })
    
    drop_unloc = workflow.activity('clean_drop_unlocatable', None, None, {
        'prov:label': 'Drop\nUnlocatable\n(-205)',
    })
    
    standardize = workflow.activity('clean_standardize', None, None, {
        'prov:label': 'Standardize\n& Impute',
    })
    
    feature_eng = workflow.activity('clean_feature_engineering', None, None, {
        'prov:label': 'Feature\nEngineering',
    })
    
    cleaned = workflow.entity('cleaned', {
        'prov:label': 'Cleaned\n(194,104 records)',
    })
    
    # De-identification operations
    generalize_zip = workflow.activity('deid_generalize_zip', None, None, {
        'prov:label': 'Generalize\nZIP Code\n(3-digit)',
    })
    
    generalize_coords = workflow.activity('deid_generalize_coords', None, None, {
        'prov:label': 'Round\nCoordinates\n(3 decimals)',
    })
    
    drop_identifiers = workflow.activity('deid_drop_identifiers', None, None, {
        'prov:label': 'Drop Direct\nIdentifiers\n(-8 columns)',
    })
    
    suppress = workflow.activity('deid_suppress', None, None, {
        'prov:label': 'Suppress\nRecords\n(-263)',
    })
    
    deidentified = workflow.entity('deidentified', {
        'prov:label': 'K-Anonymized\n(193,841 records)',
    })
    
    # Analysis operations
    segmentation = workflow.activity('analysis_segmentation', None, None, {
        'prov:label': 'K-Means\nClustering\n(Segmentation)',
    })
    
    feature_importance = workflow.activity('analysis_feature_importance', None, None, {
        'prov:label': 'Random Forest\n(Feature\nImportance)',
    })
    
    analysis_results = workflow.entity('analysis_results', {
        'prov:label': 'Analysis Results\n(Clusters +\nFeature Rankings)',
    })
    
    # Connect cleaning pipeline
    workflow.used(dedup, raw)
    workflow.used(drop_unloc, raw)
    workflow.used(standardize, raw)
    workflow.used(feature_eng, raw)
    workflow.wasGeneratedBy(cleaned, dedup)
    workflow.wasGeneratedBy(cleaned, drop_unloc)
    workflow.wasGeneratedBy(cleaned, standardize)
    workflow.wasGeneratedBy(cleaned, feature_eng)
    
    # Connect de-identification pipeline
    workflow.used(generalize_zip, cleaned)
    workflow.used(generalize_coords, cleaned)
    workflow.used(drop_identifiers, cleaned)
    workflow.used(suppress, cleaned)
    workflow.wasGeneratedBy(deidentified, generalize_zip)
    workflow.wasGeneratedBy(deidentified, generalize_coords)
    workflow.wasGeneratedBy(deidentified, drop_identifiers)
    workflow.wasGeneratedBy(deidentified, suppress)
    
    # Derivations
    workflow.wasDerivedFrom(cleaned, raw)
    workflow.wasDerivedFrom(deidentified, cleaned)
    
    # Connect analysis pipeline
    workflow.used(segmentation, deidentified)
    workflow.used(feature_importance, deidentified)
    workflow.wasGeneratedBy(analysis_results, segmentation)
    workflow.wasGeneratedBy(analysis_results, feature_importance)
    workflow.wasDerivedFrom(analysis_results, deidentified)
    
    return workflow


def save_workflow_diagram(output_dir='Workflow'):
    """
    Generate and save detailed workflow diagram.
    
    Args:
        output_dir: Directory to save the diagram
    """
    
    os.makedirs(output_dir, exist_ok=True)
    
    print("=" * 70)
    print("Chicago 311 Data Curation - Detailed Workflow Generation")
    print("=" * 70)
    print()
    
    # Generate detailed workflow
    print("Creating detailed processing workflow diagram...")
    workflow = create_detailed_processing_workflow()
    
    try:
        dot = prov_to_dot(workflow)
        
        # Save as PNG only
        png_file = os.path.join(output_dir, 'workflow_detailed.png')
        dot.write_png(png_file)
        print(f"✓ Saved detailed workflow: {png_file}")
        
    except Exception as e:
        print(f"⚠ Error generating workflow diagram: {e}")
        print("  To enable visualizations, install: pip install pydot graphviz")
        return False
    
    
    print()
    print("=" * 70)
    print("Workflow generation complete!")
    print("=" * 70)
    print()
    print(f"Files saved in '{output_dir}/' directory:")
    print("  - workflow_detailed.png")
    print("  - workflow_documentation.md")
    
    return True


def main():
    """
    Main execution function.
    """
    save_workflow_diagram()


if __name__ == "__main__":
    main()
