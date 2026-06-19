# HPV Cancer Prediction Tool

A machine learning web application for classifying HPV status (HPV Positive / HPV Negative) in cancer samples using transcriptomic biomarkers.

## Overview

This app uses a **LASSO Logistic Regression** model trained on gene expression data to predict HPV status. It was developed at ICMR-National Institute of Translational Virology and AIDS Research.

**Developers:**
- Ms. Vaishnavi Anilkumar Shirpurkar
- Dr. Abdul Arif Khan (ICMR-NITVAR)

## Features

- **Manual Prediction** — Enter expression values for 20 biomarker genes individually
- **Batch Prediction** — Upload a CSV file with multiple samples
- Download a sample input CSV for reference

## Biomarker Genes Used (20)

`ADAMTS19`, `DLK1`, `ADH1B`, `DPP6`, `ZCCHC12`, `PEG3`, `HSPB7`, `NCAM1`, `NMU`, `FOXN1`, `LHX2`, `PADI3`, `ZIC2`, `FOXA1`, `NLRP7`, `ABCA12`, `KREMEN2`, `ANGPTL1`, `TMEM40`, `FAM83C`

## Model

- **Algorithm:** LASSO Logistic Regression
- **Input:** Gene Expression Matrix (RNA-seq / transcriptome data)
- **Output:** HPV Positive / HPV Negative with confidence score (%)
- **Features:** 20 LASSO-selected biomarker genes

## Input CSV Format

| Sample | ADAMTS19 | DLK1 | ... |
|--------|----------|------|-----|
| S1     | 0.45     | 1.23 | ... |
| S2     | 0.78     | 0.91 | ... |

- First column: Sample ID
- Remaining columns: Gene expression values (one gene per column)
- Column names must match the gene list above (case-insensitive)

## Local Setup

```bash
# 1. Clone the repository
git clone https://github.com/<your-username>/hpv-cancer-prediction.git
cd hpv-cancer-prediction

# 2. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate    # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the app
shiny run app.py
```

Then open your browser at `http://127.0.0.1:8000`.

## Dependencies

| Package | Version |
|---------|---------|
| shiny | 1.6.3 |
| scikit-learn | 1.9.0 |
| joblib | 1.5.3 |
| numpy | 2.4.6 |
| pandas | 3.0.3 |

## Deployment

This app is deployed on **ShinyApps.io** (Posit Cloud). See deployment instructions in `DEPLOY.md`.

## Files

```
├── app.py                  # Main Shiny application
├── hpv_paper.pkl           # Trained LASSO model
├── training_genes.pkl      # Gene list used during model training
├── requirements.txt        # Python dependencies
└── www/
    ├── cancer_banner.jpeg  # Header image
    ├── positive.png        # HPV+ result icon
    ├── negative.png        # HPV- result icon
    ├── predict.png         # Predict icon
    └── sample_input.csv    # Sample input file for download
```
