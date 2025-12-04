**How to Reproduce the Chicago 311 Data Curation Workflow**

Our workflow is modeled based on the USGS Data Lifecycle Model.


1. **Plan**
- Define the scope of the curated dataset: 311 service requests in City of Chicago 
- Plan data cleaning, standardization, and documentation steps. 
2. **Collect** 
- Obtain raw data from the City of Chicago Open Data Portal: 
311 Service Requests Dataset. 
- Extract a sample subset from the data using random sampling. Implement using the df.sample() API in Pandas.
- Example code: sample_df = df.sample(n=1000, random_state=42)
- To view the raw dataset used for our project, clone this repository and navigate to the "Curated Dataset/1_Raw/" folder.

3. **Process** 
- To clean the data, navigate to the Data Cleaning directory in our project. Run the scripts inside that directory.
- Specifically, run these two commands:
   - python cleanRawData.py
   - python deidentification.py
 - The cleanRawData.py script drops duplicate records, drops records with missing address, converts zip code to string, and imputes blank values with "UNKNOWN". It performs feature engineering by create a new field RESOLUTION_TIME_HOURS. RESOLUTION_TIME_HOURS is the  difference between CLOSED_DATE and CREATED_DATE timestamps.
 - The deidentification.py script performs K-Anonymity, where K = 5, to generalize zip code and geographical coordinates.
 - The final curated dataset will show up in the "Dataset/3_Deidentified/"" directory.

4.  **Analyze**
- Navigate to the Data Analysis Jupyter Notebooks directory.
- Run the segmentation_model.ipynb Jupyter notebook to identify clusters under 
which the 311 requests fall under. To determine the clusters, 
segmentation_model.ipynb uses a K-means clustering algorithm. 311 requests 
falling in the same clusters are most similar to each other. This is done via 
unsupervised learning. 
- Run the CS_598_Project_Feature_Importance (2).ipynb notebook. This 
notebook uses Random Forest prediction models to predict the time to close of a 
311 service request based on provided input. Additionally, it will output the 
importance of each feature to the overall output. 

5. **Preserve**
- Store the curated dataset as a CSV file with a clear naming convention. 
- Version scripts and workflow documentation to ensure reproducibility. 
- Save all files into GitHub to allow future auditing. 
6. **Share**
- Prepare metadata using DataCite JSON format, including authorship, 
contributors, rights, and provenance. 
- Document the meaning of each field in the curated dataset via data dictionary. 
- Document the entire curation workflow. 
- In the future, one can share the dataset in a public repository such as Zenodo. 
7. **Reuse** 
- Metadata and documentation provide full context for future users to understand, 
reproduce, and analyze the dataset.


**Computational Environment** 
● Operating System: Windows 10 
● Programming Language: Python 3.11 
● Python Packages and Versions: 
| Package     | Version | Purpose                                |
|-------------|---------|------------------------------------------|
| pandas      | 2.1.1   | Data manipulation and CSV file processing |
| numpy       | 1.26.2  | Numeric computation                      |
| matplotlib  | 3.8.2   | Plotting and visualization               |
| seaborn     | 0.12.2  | Visualization                            |
| jupyterlab  | 4.2.1   | View and run interactive notebooks        |


○ It is recommended to use conda or venv to manage dependencies 
○ Example: conda create -n chicago311 python=3.11 pandas numpy matplotlib 
seaborn jupyterlab 
● Version Control: 
Git (for workflow scripts, notebooks, and versioning) 
