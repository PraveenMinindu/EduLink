# EduLink — ML Pipeline

## Folder Structure
```
ML/
├── models/
│   ├── career_fit_prediction.py    ← Model 1
│   ├── writing_analysis_model.py   ← Model 2
│   ├── job_demand_forecasting.py   ← Model 3
│   ├── salary_prediction.py        ← Model 4
│   ├── education_path.py           ← Model 5
│   ├── job_recommendation.py       ← Model 6
│   └── reasoning_layer.py          ← Model 7
├── datasets/                       ← ADD YOUR CSV FILES HERE
│   ├── synthetic_exam_master_2000.csv
│   ├── institutes_catalog_v2.csv
│   └── synthetic_vacancies_sl_it.csv
├── notebooks/                      ← original .ipynb files
├── main_pipeline.py                ← runs all 7 models
├── firebase_bridge.py              ← Firestore read/write
├── serviceAccountKey.json          ← ADD THIS (never commit)
└── requirements.txt
```

## Step 1 — Install dependencies
```bash
pip install -r requirements.txt
```

## Step 2 — Add your datasets
Copy your CSV files into the `datasets/` folder.
Rename `synthetic_exam_master_2000_FIXED.csv` to `synthetic_exam_master_2000.csv`

## Step 3 — Test the pipeline locally
```bash
cd ML
python main_pipeline.py
```

You should see all 7 models running and a final report printed.

## Step 4 — Add Firebase key
Download `serviceAccountKey.json` from Firebase Console
→ Project Settings → Service Accounts → Generate new private key
Place it in the ML/ folder. NEVER commit this file.

## Step 5 — Run with Firebase
```python
from firebase_bridge import save_mcq, save_writing, save_report, update_status
from main_pipeline import run_pipeline

# Read from Firestore, run pipeline, save back
mcq     = get_mcq("STU001")
writing = get_writing("STU001")
report  = run_pipeline(mcq, writing["text"])
save_report("STU001", report)
update_status("STU001", "done")
```
