<div align="center">

# EduLink
### AI-Driven Career Intelligence & Guidance Platform
#### *For Sri Lankan IT Undergraduates*

[![Python](https://img.shields.io/badge/Python-3.10-3776AB?style=flat&logo=python&logoColor=white)](https://python.org)
[![Flutter](https://img.shields.io/badge/Flutter-Android-02569B?style=flat&logo=flutter&logoColor=white)](https://flutter.dev)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100-009688?style=flat&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Firebase](https://img.shields.io/badge/Firebase-Firestore-FFCA28?style=flat&logo=firebase&logoColor=black)](https://firebase.google.com)
[![F1 Score](https://img.shields.io/badge/Career%20Fit%20F1-0.9706-brightgreen?style=flat)](/)
[![License](https://img.shields.io/badge/License-Academic-lightgrey?style=flat)](/)

> *"From confusion to clarity — EduLink guides each Sri Lankan IT student toward the career that fits them best."*

**BSc Honours in Data Science — Final Year Capstone Project**  
SLTC Research University · 2026

</div>

---

## What is EduLink?

EduLink is a research-backed AI career intelligence platform that classifies Sri Lankan IT undergraduates into eight career clusters using a multi-model machine learning pipeline. It combines psychometric personality profiling (Holland's RIASEC theory), semantic writing analysis, live job market data, and localized LKR salary benchmarks to deliver a personalized career intelligence report with a professional 9-page PDF output.

### Why EduLink?

A survey of 91 Sri Lankan IT students revealed:

| Finding | Statistic |
|---------|-----------|
| Never received formal career guidance | **59%** |
| Would use an AI career guidance system | **74.8%** |
| Have not researched Sri Lanka IT job demand | **77%** |

Existing career guidance tools are generic, global, and disconnected from the Sri Lanka IT market. EduLink closes this gap.

---

## System Architecture

EduLink uses a four-tier architecture:

```
┌──────────────────────────────────────────────────────┐
│  PRESENTATION TIER                                   │
│  Flutter Android App (Student-facing)                │
│  Flutter Web Admin Panel (Knowledge Management)      │
└───────────────────────┬──────────────────────────────┘
                        │ HTTP / REST API
┌───────────────────────▼──────────────────────────────┐
│  APPLICATION TIER                                    │
│  FastAPI Backend · Python 3.10 · Port 8002           │
│  12 REST Endpoints · Background task processing      │
└───────────────────────┬──────────────────────────────┘
                        │
┌───────────────────────▼──────────────────────────────┐
│  ML PIPELINE TIER                                    │
│  7-Model Pipeline · PySpark + scikit-learn           │
│  Sentence Transformers · ICTA Benchmarks             │
│  Adzuna API · Rule-based Evidence Synthesis          │
└───────────────────────┬──────────────────────────────┘
                        │ Read / Write
┌───────────────────────▼──────────────────────────────┐
│  DATA TIER                                           │
│  Firebase Firestore · Firebase Authentication        │
│  Assessment-specific data isolation                  │
│  Admin Panel → degree_programs collection            │
└──────────────────────────────────────────────────────┘
```

---

## The 7-Model ML Pipeline

```
Student Input
  40-item MCQ (Likert 1–5) + Writing Sample
          │
          ▼
  Mathematical Processing Layer
  → 12 composite psychological features
  → 6 RIASEC dimension scores (0–100)
  → Holland interest code (e.g. ICR)
  → 26-dimensional feature vector
          │
          ▼
┌─────────────────────────────────────────────────────┐
│  M1  Career Fit Prediction                          │
│  Logistic Regression (PySpark) · F1 = 0.9706       │
│  8 Sri Lanka IT career clusters · Top 3 ranked      │
└──────────────────────┬──────────────────────────────┘
                       │
       ┌───────────────┼───────────────────┐
       ▼               ▼                   ▼
  M2 Writing       M3 Job Demand       M4 Salary
  Analysis         Forecasting         Estimation
  Sentence         ARIMA baseline      ICTA benchmarks
  Transformers     + Adzuna API        + live USD/LKR
  5 trait scores   Trend analysis      Future projection
       │               │                   │
       └───────────────┼───────────────────┘
                       │
              ┌────────┴────────┐
              ▼                 ▼
         M5 Education      M6 Job Matching
         Path              Recommendation
         Firestore         Adzuna live API
         Admin Panel       Jaccard similarity
         programmes        cluster tokens
              │                 │
              └────────┬────────┘
                       │
                       ▼
          M7 AI Reasoning Layer
          Multi-model evidence synthesis
          Weighted fusion:
            Career Fit  × 0.40
            Writing     × 0.25
            Demand      × 0.20
            Salary      × 0.15
          8-section career intelligence report
          Evidence convergence detection
          Conflict identification
                       │
                       ▼
          Final Career Report + 9-Page PDF
```

---

## Key Results

| Metric | Value |
|--------|-------|
| Career Fit Model F1 Score | **0.9706** |
| Career Fit Model Accuracy | **0.97** |
| MCQ Questions | **40** |
| Composite Psychological Features | **12** |
| RIASEC Dimensions | **6** |
| Sri Lanka IT Career Clusters | **8** |
| Feature Vector Size | **26** |
| Reasoning Evidence Sources | **6 independent** |
| PDF Report Pages | **9** |
| Flutter Screens | **15+** |
| API Endpoints | **12** |
| Admin Panel Screens | **11** |

### Model Comparison (M1 Career Fit)

| Algorithm | F1 Score | Accuracy | Selected |
|-----------|----------|----------|----------|
| Logistic Regression | **0.9706** | **0.97** | ✅ |
| Random Forest | 0.94 | 0.94 | |
| Gradient Boosting | 0.93 | 0.93 | |
| K-Nearest Neighbours (k=5) | 0.90 | 0.90 | |
| Decision Tree | 0.85 | 0.85 | |

Logistic Regression selected — highest F1 score and fully interpretable coefficients.

---

## Features

### Student App (Flutter Android)
- **Psychometric Assessment** — 40-item MCQ across 4 sections
- **Writing Analysis** — Semantic analysis of career-readiness writing sample
- **Career Report** — Recommended role, score, confidence, RIASEC radar chart
- **AI Reasoning** — 8-section evidence-synthesis explanation
- **Salary Intelligence** — Current LKR range + 3–5 year projection (ICTA benchmarks)
- **Education Recommendations** — Top 5 Sri Lanka IT programmes from Admin Panel
- **Live Job Matches** — Adzuna API with Jaccard similarity scoring
- **Skill Gap Analysis** — Cluster-specific skill requirements
- **Multiple Assessments** — Assessment history with independent report preservation
- **PDF Export** — 9-page professional career report with charts and MCQ responses
- **Dashboard** — Assessment history with navigation to any previous report

### Admin Panel (Flutter Web)
- University management (add, edit, delete)
- Degree programme CRUD with full metadata
- Firestore integration — live data feeds into M5 Education Path
- OpenStreetMap integration (flutter_map) for university locations

### AI Reasoning Layer (M7)
- **6 independent evidence sources** assessed per recommendation
- **Evidence convergence** — Strong / Moderate / Weak classification
- **Conflict detection** — flags high fit + weak demand, high fit + low writing
- **8 structured sections** — Career Match, Evidence Convergence, Psychological Alignment, Writing Readiness, Market Context, Development Areas, Education Path, Overall Reasoning
- **Development areas** — cluster-specific, never generic

---

## Project Structure

```
EduLink/
│
├── Backend/                          # FastAPI application
│   ├── main.py                       # App entry point, router registration
│   ├── firebase_bridge.py            # Firestore read/write (v1 + v2)
│   ├── requirements.txt
│   └── routes/
│       ├── student.py                # Register, profile endpoints
│       ├── mcq.py                    # MCQ submission
│       ├── writing.py                # Writing submission
│       ├── report.py                 # V1 report routes
│       ├── report_v2.py              # V2 assessment-based routes
│       └── admin/                    # Admin Panel API routes
│
├── ML/                               # Machine learning pipeline
│   ├── main_pipeline.py              # 7-model end-to-end pipeline
│   ├── models/
│   │   ├── career_fit_prediction.py  # M1 — RIASEC + cluster scoring (F1=0.9706)
│   │   ├── writing_analysis_model.py # M2 — Sentence Transformers
│   │   ├── job_demand_forecasting.py # M3 — ARIMA + Adzuna API
│   │   ├── salary_api.py             # M4 — ICTA benchmarks + live rate
│   │   ├── education_path.py         # M5 — Firestore programme recommendations
│   │   ├── job_api.py                # M6 — Adzuna + Jaccard similarity
│   │   ├── reasoning_layer.py        # M7 — Evidence synthesis (v2.0)
│   │   └── skill_extractor.py        # Cluster-specific skill extraction
│   ├── notebooks/
│   │   ├── career_fit_prediction_v4.ipynb
│   │   ├── Mathematical_model.ipynb
│   │   └── Writing_analysis_model.ipynb
│   └── config/
│
├── frontend/                         # Flutter Android app
│   └── lib/
│       ├── config/
│       │   ├── app_colors.dart
│       │   └── app_constants.dart    # baseUrl configuration
│       ├── models/
│       │   └── career_report_model.dart
│       ├── services/
│       │   ├── api_service.dart      # HTTP client (v1 + v2 endpoints)
│       │   ├── auth_service.dart     # Firebase Auth + user_mappings
│       │   └── pdf_generator.dart    # 9-page PDF generation
│       └── screens/
│           ├── splash_screen.dart
│           ├── login_screen.dart
│           ├── register_screen.dart
│           ├── dashboard_screen.dart
│           ├── mcq_screen.dart
│           ├── writing_screen.dart
│           ├── processing_screen.dart
│           ├── profile_screen.dart
│           ├── roadmap_screen.dart
│           ├── writing_tips_screen.dart
│           ├── skill_gap_screen.dart
│           └── report/
│               ├── report_screen.dart
│               ├── education_screen.dart
│               ├── jobs_screen.dart
│               ├── roles_screen.dart
│               └── compare_screen.dart
│
└── admin/                            # Flutter Web Admin Panel
```

---

## Setup and Installation

### Prerequisites

```
Python 3.10+
Flutter SDK 3.x
Firebase project (Firestore + Authentication enabled)
Adzuna API credentials (free tier)
```

### 1. Clone the Repository

```bash
git clone https://github.com/PraveenMinindu/EduLink.git
cd EduLink
```

### 2. Backend Setup

```bash
cd Backend
pip install -r requirements.txt
```

Create a `.env` file in `Backend/`:

```env
FIREBASE_KEY_PATH=C:\path\to\serviceAccountKey.json
```

Place your `serviceAccountKey.json` (from Firebase Console → Project Settings → Service Accounts) in the `Backend/` folder.

Start the backend:

```bash
# Windows PowerShell
$env:FIREBASE_KEY_PATH = "C:\Users\YourName\Desktop\EduLink\Backend\serviceAccountKey.json"
cd Backend
python -m uvicorn main:app --host 0.0.0.0 --port 8002
```

Swagger UI available at: `http://localhost:8002/docs`

### 3. Flutter App Setup

```bash
cd frontend
flutter pub get
```

Update the base URL in `frontend/lib/config/app_constants.dart`:

```dart
static const String baseUrl = 'http://YOUR_LAPTOP_IP:8002';
```

Find your laptop IP:
```bash
ipconfig   # Windows — look for Wi-Fi IPv4 Address
```

Run the app:
```bash
flutter run
```

> **Note:** Your phone and laptop must be on the same network, or connected via USB debugging.

### 4. ML Pipeline (Direct Test)

```bash
cd ML
python main_pipeline.py
```

This runs the full 7-model pipeline with test data and prints results.

---

## API Endpoints

### V1 Routes (original)

| Method | Endpoint | Description | Timeout |
|--------|----------|-------------|---------|
| POST | `/student/register` | Register new student | 60s |
| POST | `/student/submit-mcq` | Submit 40 MCQ answers | 120s |
| POST | `/student/submit-writing` | Submit writing sample | 120s |
| POST | `/student/generate-report/{id}` | Run 7-model pipeline | 180s |
| GET | `/student/report/{id}` | Retrieve career report | 60s |
| GET | `/student/report-status/{id}` | Poll generation status | 60s |
| GET | `/student/skills/{id}` | Get skill recommendations | 120s |

### V2 Routes (assessment-based)

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/student/submit-mcq-v2` | Save MCQ under assessmentId |
| POST | `/student/submit-writing-v2` | Save writing under assessmentId |
| POST | `/student/generate-report-v2/{assessment_id}` | Generate assessment-specific report |
| GET | `/student/report-v2/{assessment_id}` | Get report by assessmentId |
| GET | `/student/report-status-v2/{assessment_id}` | Poll by assessmentId |
| GET | `/student/history/{student_id}` | Get all assessment history |

---

## Firestore Collections

| Collection | Key | Description |
|-----------|-----|-------------|
| `students` | `{studentId}` | Student profile data |
| `user_mappings` | `{firebaseUID}` | Firebase UID → studentId mapping |
| `mcq_responses` | `{assessmentId}` | MCQ answers per assessment |
| `writing_samples` | `{assessmentId}` | Writing text per assessment |
| `career_reports` | `{assessmentId}` | Full report per assessment |
| `report_status` | `{assessmentId}` | Pipeline status |
| `assessment_history` | `{studentId}` | List of all assessments |
| `degree_programs` | `{programId}` | Admin Panel programmes |
| `universities` | `{universityId}` | Admin Panel universities |
| `career_skills` | `{cluster}` | Cached skill data (24h) |

---

## Data Sources

| Source | Data | Model |
|--------|------|-------|
| ICTA Sri Lanka IT Salary Survey | Role salary benchmarks (LKR) | M4 |
| ExchangeRate-API / Frankfurter | Live USD/LKR rate | M4 |
| Adzuna India API | Live job vacancies | M3, M6 |
| Firestore (Admin Panel) | Sri Lanka IT programmes | M5 |
| Holland 1997 RIASEC Theory | Personality dimensions | M1, M7 |
| Sentence Transformers (HuggingFace) | Pre-trained NLP model | M2 |

---

## Theoretical Foundations

| Theory | Authors | Application in EduLink |
|--------|---------|------------------------|
| Holland's RIASEC Theory | Holland, 1997 | Personality-to-career cluster mapping |
| Trait-Factor Theory | Dawis, 1994 | Composite feature design |
| Social Cognitive Career Theory | Lent et al., 1994 | Self-efficacy in career readiness |
| O\*NET Importance Ratings | US Dept of Labor | RIASEC weight calibration |

---

## Addressing Research Gaps

| Related Work | Gap | EduLink Solution |
|-------------|-----|-----------------|
| Kiranmai et al. 2025 — AI career recommendation | Global context, not Sri Lanka | Localized clusters, ICTA salary, SL programmes |
| Faruque et al. 2024 — NLP career prediction | No personality theory, no salary | RIASEC + ICTA benchmarks + live rate |
| Frej et al. 2024 — Course recommender | No mobile deployment, no local education | Flutter app + Firestore Admin Panel |
| Pinto et al. 2025 — Explainable AI in labour market | Theoretical only | Working deployed system with evidence reasoning |

---

## Team

| Member | Role | Student ID |
|--------|------|------------|
| W. A. P. M. Weerakkody | System Architect · Backend · ML Lead | 22ug2-0076 |
| S. S. Ellawala | Data Scientist · Model Analytics | 22ug2-0570 |
| K. A. M. N. Rajakaruna | Frontend · Live Integrations | 22ug2-0161 |

**Supervisor:** Dr. Chameera De Silva  
**Co-Supervisor:** Mr. Kavinda Tharindu  
**University:** SLTC Research University  
**Programme:** BSc Honours in Data Science  
**Module:** CCS3301 — Capstone Project 2026
**Batch:** 2026B

---

## Future Work

| Timeline | Work |
|----------|------|
| Immediate | Collect real student MCQ data · Retrain M1 on real data |
| Short term | Connect skill extractor to main pipeline · Activate real ARIMA trend |
| Medium term | Build TechSalary.lk scraper · Partner with TopJobs.lk |
| Long term | Cloud deployment (AWS/GCP) · iOS version |

---

## License

This project was developed as a Final Year Capstone Project at SLTC Research University. All rights reserved © 2026.

---

<div align="center">

**EduLink — Empowering Sri Lankan IT Careers through AI**

</div>