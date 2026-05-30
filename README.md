# EduLink — AI-Based Career Guidance System

> **"From confusion to clarity, EduLink guides each student toward the IT career path that fits them best."**

[![Python](https://img.shields.io/badge/Python-3.10-blue)](https://python.org)
[![Flutter](https://img.shields.io/badge/Flutter-Android-blue)](https://flutter.dev)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100-green)](https://fastapi.tiangolo.com)
[![Firebase](https://img.shields.io/badge/Firebase-Firestore-orange)](https://firebase.google.com)
[![Tests](https://img.shields.io/badge/Tests-113%20passing-brightgreen)](/)
[![F1 Score](https://img.shields.io/badge/Career%20Fit%20F1-0.97-brightgreen)](/)

---

## What is EduLink?

EduLink is an AI-powered career guidance mobile application built specifically for Sri Lankan IT students. It combines psychometric personality profiling, semantic writing analysis, live job market data, and real LKR salary benchmarks to recommend the most suitable IT career path for each student.

**Survey of 91 Sri Lankan students showed:**
- 59% never received formal career guidance
- 74.8% would use an AI career guidance system
- 77% have not researched IT job demand in Sri Lanka

EduLink closes this gap.

---

## System Architecture

```
┌─────────────────────────────────────┐
│   Layer 1 — Presentation Layer      │
│   Flutter Android App               │
│   Register → MCQ → Writing →        │
│   Report → Compare → Courses        │
└──────────────┬──────────────────────┘
               │ HTTP REST
┌──────────────▼──────────────────────┐
│   Layer 2 — Application Layer       │
│   FastAPI Backend + ML Pipeline     │
│   7 REST Endpoints + 7 ML Models    │
└──────────────┬──────────────────────┘
               │ Read / Write
┌──────────────▼──────────────────────┐
│   Layer 3 — Data Layer              │
│   Firebase Firestore                │
│   students, mcq, writing, reports   │
└─────────────────────────────────────┘
```

---

## The 7-Model ML Pipeline

```
Student Input (40 MCQ + writing sample)
         ↓
Mathematical Layer (preprocessing)
  → 20 composite features
  → 6 RIASEC scores
  → Holland interest code (e.g. EIR)
  → 26-feature vector
         ↓
Model 1 — Career Fit Prediction
  PySpark Logistic Regression | F1 = 0.97
  8 Sri Lanka IT clusters → top 3
         ↓
Model 2  Writing Analysis     Sentence Transformers MiniLM
Model 3  Job Demand           ARIMA + Adzuna API
Model 4  Salary Prediction    PayScale LKR 2026 + live rate
Model 5  Education Path       25 Sri Lankan IT programs
         ↓
Model 6 — Job Recommendation (3-tier)
  Adzuna live API → TopJobs.lk → local SL fallback
         ↓
Model 7 — AI Reasoning Layer
  final = career×0.40 + writing×0.25 + demand×0.20 + salary×0.15
  → final score 0-100 | High / Medium / Low confidence
         ↓
Final Career Report
  Role + score | Salary LKR | Education | 5 live jobs | Compare
```

---

## Key Results

| Metric | Value |
|--------|-------|
| Career Fit Model F1 Score | **0.97** |
| Total Unit Tests | **113 passing, 0 failing** |
| MCQ Questions | **40** |
| Composite Features | **20** |
| RIASEC Dimensions | **6** |
| Sri Lanka IT Clusters | **8** |
| Feature Vector Size | **26** |
| Flutter Screens | **10** |
| Course Recommendations | **120** |
| SL IT Programs | **25** |
| Survey Respondents | **91** |

---

## Model Comparison

| Model | F1 Score | Accuracy |
|-------|----------|----------|
| **Logistic Regression** ✓ | **0.97** | **0.97** |
| Random Forest | 0.94 | 0.94 |
| Gradient Boosting | 0.93 | 0.93 |
| KNN (k=5) | 0.90 | 0.90 |
| Decision Tree | 0.85 | 0.85 |

Logistic Regression selected — highest accuracy and fully interpretable.

---

## Project Structure

```
EduLink/
├── Backend/
│   ├── main.py                    # FastAPI server + startup preload
│   ├── firebase_bridge.py         # Firestore read/write
│   ├── requirements.txt
│   └── routes/
│       ├── student.py             # register, MCQ, writing endpoints
│       ├── report.py              # generate-report, get-report
│       ├── mcq.py
│       └── writing.py
│
├── ML/
│   ├── main_pipeline.py           # connects all 7 models
│   ├── models/
│   │   ├── career_fit_prediction.py    # Model 1 - RIASEC + cluster scoring
│   │   ├── writing_analysis_model.py   # Model 2 - Sentence Transformers
│   │   ├── job_demand_forecasting.py   # Model 3 - ARIMA + Adzuna
│   │   ├── salary_api.py               # Model 4 - LKR benchmarks
│   │   ├── education_path.py           # Model 5 - 25 SL programs
│   │   ├── job_recommendation.py       # Model 6 - Jaccard similarity
│   │   └── reasoning_layer.py          # Model 7 - weighted fusion
│   ├── notebooks/
│   │   ├── career_fit_prediction_v4.ipynb   # 5-model comparison
│   │   ├── Mathematical_model.ipynb          # RIASEC layer design
│   │   └── Writing_analysis_model.ipynb
│   └── tests/
│       └── test_ml_models.py
│
└── frontend/
    └── lib/
        ├── screens/
        │   ├── register_screen.dart
        │   ├── mcq_screen.dart
        │   ├── writing_screen.dart
        │   ├── report/report_screen.dart     # RIASEC radar chart
        │   ├── compare_screen.dart
        │   └── course_recommendations_screen.dart
        ├── services/api_service.dart
        ├── models/career_report_model.dart
        └── config/app_colors.dart
```

---

## Setup and Installation

### Prerequisites

```
Python 3.10+
Flutter SDK
Firebase account
Adzuna API key
```

### Backend Setup

```bash
cd Backend
pip install -r requirements.txt
```

Create `.env` file in Backend/:
```
FIREBASE_KEY=your_firebase_key
ADZUNA_APP_ID=your_adzuna_app_id
ADZUNA_API_KEY=your_adzuna_api_key
EXCHANGE_RATE_KEY=your_exchange_rate_key
```

Run backend:
```bash
# Set ML path
export PYTHONPATH=../ML   # Linux/Mac
$env:PYTHONPATH = "..\ML" # Windows PowerShell

# Start server
python -m uvicorn main:app --reload --port 8001 --host 0.0.0.0
```

### Flutter Setup

```bash
cd frontend
flutter pub get
flutter run
```

Make sure your phone is on the same WiFi as the backend laptop.

Update `api_service.dart` base URL to your laptop IP:
```dart
static const String baseUrl = 'http://YOUR_LAPTOP_IP:8001/student';
```

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/student/register` | Register new student |
| POST | `/student/submit-mcq` | Submit 40 MCQ answers (120s) |
| POST | `/student/submit-writing` | Submit writing sample |
| POST | `/student/generate-report/{id}` | Run 7-model pipeline (180s) |
| GET | `/student/report/{id}` | Get career report |
| GET | `/student/report-status/{id}` | Poll generation status |
| GET | `/student/skills/{id}` | Get skill recommendations (24h cache) |

Swagger UI: `http://localhost:8001/docs`

---

## Salary Data Sources

| Source | Year | Type |
|--------|------|------|
| PayScale Sri Lanka | 2026 | Entry level LKR |
| Glassdoor Colombo | May 2026 | Entry level LKR |
| TechSalary.lk | 2025 | Mid level LKR |
| ExchangeRate-API | Live | USD/LKR conversion |

---

## Testing

```bash
cd ML
python -m pytest tests/test_ml_models.py -v

# Backend tests
cd Backend
python -m pytest tests/test_backend.py -v
```

```
113 tests passing
0 failures
100% pass rate
```

---

## Theoretical Foundations

| Theory | Author | Application |
|--------|--------|-------------|
| Holland RIASEC Theory | Holland 1997 | Personality to career mapping |
| Trait-Factor Theory | Dawis 1994 | Composite feature design |
| SCCT | Lent et al. 1994 | Self-efficacy in career choice |
| O*NET Importance Ratings | US DOL | RIASEC weight calibration |

---

## Future Work

**Immediate (June–July 2026)**
- Collect real student MCQ data from Sri Lankan schools
- Retrain career fit model on real data
- Compare F1 with synthetic baseline

**Short Term (July–August 2026)**
- Connect skill extractor to main pipeline
- 3 months Adzuna data → activate real trend calculation
- User testing with real students

**Medium Term (August–September 2026)**
- 6 months data → ARIMA fully active
- Build TechSalary.lk web scraper
- Partner with TopJobs.lk for Sri Lanka live data

---

## Team

| Member | Role | Student ID |
|--------|------|------------|
| W. A. P. M. Weerakkody | System Architect & Backend & ML | 22ug2-0076 |
| S. S. Ellawala | Data Scientist & Model Analytics | 22ug2-0570 |
| K. A. M. N. Rajakaruna | Frontend & Live Integrations | 22ug2-0161 |

**Supervised by:** Dr. Chameera De Silva  
**Co-Supervised by:** Mr. Kavinda Tharindu  
**University:** SLTC Research University  
**Course:** CCS3301 — Capstone Project 2025  
**Batch:** 2026A

---

## Related Work

| Paper | Gap |
|-------|-----|
| Kiranmai et al. 2025 — AI career recommendation using ML | Global context, not adapted to Sri Lanka |
| Faruque et al. 2024 — NLP career prediction for CS students | No personality theory, no salary data |
| Frej et al. 2024 — Course recommender considering job market | No mobile deployment, no local education |
| Pinto et al. 2025 — Explainable AI in labour market | Theoretical only, no working implementation |

EduLink addresses all four gaps in one integrated system.

---

## License

This project was developed as a Final Year Project at SLTC Research University. All rights reserved.
