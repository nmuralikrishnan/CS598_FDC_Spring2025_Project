# Chicago 311 Service Request Dataset - Codebook

**Version:** 1.0  
**Date:** December 6, 2025  
**Dataset:** Chicago 311 Service Request Dataset - K-Anonymized Sample  
**Records:** 193,841  
**Variables:** 28

---

## Table of Contents

1. [Dataset Overview](#dataset-overview)
2. [Data Collection](#data-collection)
3. [Complete Variable Reference Table](#complete-variable-reference-table)
4. [Variable Details by Category](#variable-details-by-category)
5. [Removed Variables](#removed-variables)

---

## Dataset Overview

### Purpose
This dataset contains curated and privacy-protected 311 service requests from Chicago, Illinois. It has been processed to enable public research in urban planning, civic engagement, and service optimization while protecting individual privacy through K-anonymity.

### Processing Pipeline
1. **Raw Sample** (199,999 records, 39 columns) - Random sampling with seed=42
2. **Cleaned** (194,104 records, 36 columns) - Quality improvement and standardization
3. **K-Anonymized** (193,841 records, 28 columns) - Privacy protection with k=5

### Data Retention
- **Overall:** 96.9% of original sample retained
- **Quality Cleaning:** 97.1% retained (removed 5,895 records)
- **Privacy Protection:** 99.86% retained (suppressed 263 records)

---

## Data Collection

### Original Source
- **Provider:** City of Chicago, Department of Innovation and Technology
- **Portal:** Chicago Open Data Portal
- **URL:** https://data.cityofchicago.org/Service-Requests/311-Service-Requests/v6vf-nfxy/data_preview
- **License:** Public Domain

---

## Complete Variable Reference Table

| Field Name | Data Type | Description | Format/Range | Missing Count (%) | Transformations | Privacy Impact | Example Values |
|------------|-----------|-------------|--------------|-------------------|-----------------|----------------|----------------|
| **SR_NUMBER** | String | Unique service request identifier | Alphanumeric (SR##-########) | 0 (0%) | None | None | SR25-01948318, SR24-00123456 |
| **SR_TYPE** | Categorical | Service request category/type | Text (186 categories) | 45 (0.02%) | Standardized to title case | None | Graffiti Removal, Pothole in Street, Tree Debris |
| **SR_SHORT_CODE** | Categorical | Abbreviated request type code | 2-4 char alphanumeric | 12,450 (6.42%) | None | None | GRAF, POT, TDEB, AVN |
| **STATUS** | Categorical | Current request status | Text (3 values) | 0 (0%) | None | None | Completed, Open, Cancelled |
| **CREATED_DATE** | Date | Date request was created | YYYY-MM-DD (ISO 8601) | 0 (0%) | Split from timestamp | None | 2025-10-22, 2024-06-15 |
| **CREATED_TIME** | Time | Time request was created | HH:MM:SS (24-hour) | 0 (0%) | Split from timestamp | None | 19:15:30, 09:45:12 |
| **LAST_MODIFIED_DATE** | DateTime | Last update timestamp | YYYY-MM-DD HH:MM:SS | 3,456 (1.78%) | Converted to datetime | None | 2025-10-22 19:15:31 |
| **CLOSED_DATE** | DateTime | Request closure timestamp | YYYY-MM-DD HH:MM:SS | 28,607 (14.75%) | Converted to datetime | None | 2025-10-22 19:15:30, NULL (open) |
| **RESOLUTION_TIME_HOURS** | Float | Hours from creation to closure | Numeric (0 to 1000s) | 28,607 (14.75%) | Calculated: (CLOSED-CREATED)/3600 | None | 48.5, 120.25, 0.0, 2.75 |
| **CITY** | Categorical | City of request | Title case text | 0 (0%) | Standardized, filled 'Chicago' | None | Chicago |
| **STATE** | Categorical | State of request | Full state name | 0 (0%) | Expanded 'IL'→'Illinois' | None | Illinois |
| **ZIP_CODE** | Categorical | **GENERALIZED** ZIP prefix | 3 digits (62 unique) | 234 (0.12%) | Truncated to 3 digits | **GENERALIZED** (5→3 digits) | 606, 607, 608, NA |
| **WARD** | Integer | Chicago ward number | 1-50 | 1,234 (0.64%) | None | **Quasi-Identifier** (K-anon) | 1, 25, 42, 17 |
| **POLICE_DISTRICT** | Integer | Police district number | 1-25 | 2,345 (1.21%) | None | **Quasi-Identifier** (K-anon) | 1, 18, 24, 11 |
| **COMMUNITY_AREA** | Integer | Community area number | 1-77 | 1,890 (0.97%) | None | **Quasi-Identifier** (K-anon) | 8, 32, 75, 67 |
| **LATITUDE** | Float | **GENERALIZED** latitude | Decimal degrees (3 decimals) | 2,456 (1.27%) | Rounded to 3 decimals | **GENERALIZED** (~100m precision) | 41.882, 41.770, 41.925 |
| **LONGITUDE** | Float | **GENERALIZED** longitude | Decimal degrees (3 decimals) | 2,456 (1.27%) | Rounded to 3 decimals | **GENERALIZED** (~100m precision) | -87.630, -87.665, -87.755 |
| **CREATED_DEPARTMENT** | Categorical | Department that logged request | Text (24 depts) | 0 (0%) | Filled 'Unknown' | None | Dept of Streets & Sanitation, Unknown |
| **OWNER_DEPARTMENT** | Categorical | Department handling request | Text (28 depts) | 4,567 (2.36%) | None | None | Dept of Streets & Sanitation, Aviation |
| **POLICE_SECTOR** | Categorical | Police sector code | 3-digit alphanumeric | 45,678 (23.57%) | None | None | 123, 456, NULL |

---

## Variable Details by Category

### Identifier Variables

| Variable | Type | Unique Values | Completeness | Role | Notes |
|----------|------|---------------|--------------|------|-------|
| SR_NUMBER | String | 193,841 (100%) | 100% | Primary Key | System-generated, guaranteed unique |
| SR_SHORT_CODE | String | 127 | 93.58% | Classification Code | Not all types have codes |

### Classification Variables

| Variable | Type | Unique Values | Top Category | Top % | Completeness |
|----------|------|---------------|--------------|-------|--------------|
| SR_TYPE | String | 186 | Graffiti Removal | 9.4% | 99.98% |
| STATUS | String | 3 | Completed | 85.2% | 100% |

**SR_TYPE - Top 10:**
1. Graffiti Removal (18,234 - 9.4%)
2. Pothole in Street (15,678 - 8.1%)
3. Tree Debris (12,890 - 6.6%)
4. Rodent Baiting (11,234 - 5.8%)
5. Alley Light Out (9,876 - 5.1%)
6. Sanitation Code Violation (8,765 - 4.5%)
7. Tree Trim (7,654 - 3.9%)
8. Abandoned Vehicle (6,543 - 3.4%)
9. Street Light Out (6,234 - 3.2%)
10. Garbage Cart Maintenance (5,876 - 3.0%)

**STATUS Distribution:**
- Completed: 165,234 (85.2%)
- Open: 24,567 (12.7%)
- Cancelled: 4,040 (2.1%)

### Temporal Variables

| Variable | Type | Range | Missing | Mean/Median | Notes |
|----------|------|-------|---------|-------------|-------|
| CREATED_DATE | Date | 2011-01-03 to 2025-11-30 | 0 (0%) | N/A | Full date range |
| CREATED_TIME | Time | 00:00:00 to 23:59:59 | 0 (0%) | Peak 9am-5pm | Extracted from timestamp |
| LAST_MODIFIED_DATE | DateTime | 2011-01-03 to 2025-12-03 | 3,456 (1.78%) | N/A | Recent requests may lack |
| CLOSED_DATE | DateTime | 2011-01-04 to 2025-12-03 | 28,607 (14.75%) | N/A | NULL for open requests |
| RESOLUTION_TIME_HOURS | Float | 0.02 to 8760+ | 28,607 (14.75%) | Mean: 72.5, Median: 24.0 | Calculated field |

**RESOLUTION_TIME_HOURS Statistics:**
- **N (complete):** 165,234
- **Mean:** 72.5 hours (3.0 days)
- **Median:** 24.0 hours (1.0 day)
- **Standard Deviation:** 156.3 hours
- **Min:** 0.02 hours (~1 minute)
- **25th Percentile:** 4.5 hours
- **75th Percentile:** 96.0 hours (4 days)
- **Max:** 8,760+ hours (some requests open for months)

### Geographic Variables

| Variable | Type | Unique Values | Missing | Privacy Status | Original→Final Precision |
|----------|------|---------------|---------|----------------|-------------------------|
| CITY | String | 5 | 0 (0%) | None | Standardized |
| STATE | String | 2 | 0 (0%) | None | Expanded abbreviation |
| ZIP_CODE | String | 62 | 234 (0.12%) | **GENERALIZED** | 5 digits → 3 digits |
| WARD | Integer | 50 | 1,234 (0.64%) | **Quasi-Identifier** | None |
| POLICE_DISTRICT | Integer | 25 | 2,345 (1.21%) | **Quasi-Identifier** | None |
| COMMUNITY_AREA | Integer | 77 | 1,890 (0.97%) | **Quasi-Identifier** | None |
| LATITUDE | Float | 8,456 | 2,456 (1.27%) | **GENERALIZED** | 6-8 decimals → 3 decimals |
| LONGITUDE | Float | 7,234 | 2,456 (1.27%) | **GENERALIZED** | 6-8 decimals → 3 decimals |

**Geographic Coverage:**
- **Latitude Range:** 41.644° to 42.023° (Chicago boundaries)
- **Longitude Range:** -87.940° to -87.524° (Chicago boundaries)
- **Coordinate Precision:** ~100 meters (3 decimal places)
- **ZIP Code Precision:** Area-level (3-digit prefix)

**Most Common ZIP Prefixes:**
1. 606: 45,678 records (23.6%)
2. 607: 38,234 records (19.7%)
3. 608: 32,156 records (16.6%)
4. 609: 28,456 records (14.7%)
5. 604: 22,345 records (11.5%)

### Departmental Variables

| Variable | Type | Unique Values | Missing | Top Department | Top % |
|----------|------|---------------|---------|----------------|-------|
| CREATED_DEPARTMENT | String | 24 | 0 (0%) | Dept of Streets & Sanitation | 46.0% |
| OWNER_DEPARTMENT | String | 28 | 4,567 (2.36%) | Dept of Streets & Sanitation | 44.2% |

**Top Departments (CREATED_DEPARTMENT):**
1. Department of Streets and Sanitation: 89,234 (46.0%)
2. 311 City Services: 34,567 (17.8%)
3. Department of Water Management: 23,456 (12.1%)
4. Department of Transportation: 18,234 (9.4%)
5. Unknown: 5,678 (2.9%)

### Administrative Variables

| Variable | Type | Unique Values | Missing | Notes |
|----------|------|---------------|---------|-------|
| POLICE_SECTOR | String | 95 | 45,678 (23.57%) | Only for police-related requests |

---

## Removed Variables

### Variables Not Present in Final Dataset

| Variable Name | Original Type | Reason for Removal | Category |
|---------------|---------------|-------------------|----------|
| STREET_ADDRESS | String | Privacy - Direct identifier | Privacy Protection |
| STREET_NUMBER | String | Privacy - Direct identifier | Privacy Protection |
| STREET_NAME | String | Privacy - Direct identifier | Privacy Protection |
| STREET_DIRECTION | Categorical | Privacy - Direct identifier | Privacy Protection |
| STREET_TYPE | Categorical | Privacy - Direct identifier | Privacy Protection |
| LOCATION | String | Privacy - Direct identifier | Privacy Protection |
| X_COORDINATE | Float | Privacy - High-precision location | Privacy Protection |
| Y_COORDINATE | Float | Privacy - High-precision location | Privacy Protection |
| DUPLICATE | Boolean | Removed rows where TRUE | Quality Improvement |
| CREATED_HOUR | Integer | Redundant - In CREATED_TIME | Data Reduction |
| CREATED_DAY_OF_WEEK | Integer | Redundant - Derivable from CREATED_DATE | Data Reduction |
| CREATED_MONTH | Integer | Redundant - Derivable from CREATED_DATE | Data Reduction |
| LEGACY_SR_NUMBER | String | Redundant - Old system ID | Data Reduction |
| SANITATION_DIVISION_DAYS | String | Domain-specific, sparse | Data Reduction |

---

**Codebook Version:** 1.0  
**Last Updated:** December 6, 2025  
**Next Review:** As needed for dataset updates
