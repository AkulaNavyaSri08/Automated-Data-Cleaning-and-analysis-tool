# Automated Data Cleaning and Analysis Tool

## Overview
The **Automated Data Cleaning and Analysis Tool** is a Python-based application designed to simplify the preprocessing and analysis of raw datasets. It helps users identify data quality issues, clean datasets, and generate meaningful analytical insights through an interactive interface.

The tool is suitable for employee, student, and generic datasets and ensures that all dashboards and analytics are generated using cleaned data for accurate results.

---

## Features
- Upload datasets in **CSV** or **Excel** format
- Automatic **data quality assessment**
- Data Quality Score generation
- Rule-based **data cleaning**:
  - Missing value handling
  - Duplicate removal
  - Data type correction
- Dataset type detection:
  - Employee dataset
  - Student dataset
  - Generic dataset
- Domain-specific dashboards:
  - Payroll list and salary insights
  - Student performance summaries
  - Generic statistical overviews
- **User-driven analytics toolkit**:
  - Descriptive statistics
  - Group-by analysis
  - Top-K analysis
  - Threshold-based filtering
  - Correlation analysis
- Download cleaned datasets and analytical reports

---

## Technology Stack
- **Programming Language:** Python  
- **Libraries:** Pandas, NumPy  
- **UI Framework:** Streamlit  
- **Data Handling:** CSV, Excel  

---

## Project Structure
```yaml
    Automated_Cleaning_Tool/
    │
    ├── app.py
    ├── core/
    │ ├── data_loader.py
    │ └── cleaning_pipeline.py
    │ └── datatype_fix.py
    │ └── datatype_handler.py
    │ └── missing_values.py
    │ └── outliers.py
    │ └── primary_key_detector.py
    │
    ├── analysis/
    │ ├── dataset_detector.py
    │ └── data_quality.py
    │ └── data_quality_score.py
    │ └── employee_analysis.py
    │ └── student_analysis.py
    │ └── generic_analysis.py
    │ └── user_analytics.py
    │ └── outlier_stats.py
    │
    ├── reports/
    │ └── summary.py
    |
    ├── sample_data/
    │
    ├── requirements.txt
    └── README.md

```
---

## Installation
1. Clone or download the project.
2. Navigate to the project directory.
3. Install required dependencies:
   ```pip install -r requirements.txt```
## How to Run
Run the Streamlit application using:
    `streamlit run app.py`

The application will open in your web browser.

## Usage Workflow
1. Upload a dataset (CSV or Excel).
2. View dataset preview and data quality score.
3. Clean the dataset using the Cleaning tab.
4. Generate dashboards based on cleaned data.
5. Perform custom analytics using the Analytics Toolkit.
6. Download cleaned datasets or analysis reports.

## Key Design Highlights
- Uses rule-based logic (no machine learning)
- Modular and scalable architecture
- Analytics and dashboards operate only on cleaned data
- User-friendly and exam-ready implementation

## Applications
- Academic projects
- Data preprocessing automation
- Quick exploratory data analysis
- Learning data cleaning and analytics concepts

## Conclusion

This project provides an efficient and structured approach to automated data cleaning and analysis. By combining data quality assessment, dataset categorization, and user-driven analytics, it offers a reliable solution for handling real-world datasets with minimal manual effort.

### Author
*Akula Navya Sri*