# ============================================================
# EduLink — FastAPI Main Application
# ============================================================

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import student, mcq, writing, report
from routes import report_v2
from routes.admin import auth as admin_auth
from routes.admin import universities, programs, dashboard

app = FastAPI(
    title="EduLink API",
    description="AI-Driven Career Guidance System for Sri Lankan IT Students",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Student routes ────────────────────────────────────────────
app.include_router(student.router, prefix="/student", tags=["Student"])
app.include_router(mcq.router,     prefix="/student", tags=["MCQ"])
app.include_router(writing.router, prefix="/student", tags=["Writing"])
app.include_router(report.router,  prefix="/student", tags=["Report"])

# ── V2 routes — assessment-based ─────────────────────────────
app.include_router(report_v2.router, prefix="/student", tags=["Report V2"])

# ── Admin routes ──────────────────────────────────────────────
app.include_router(admin_auth.router,   prefix="/admin/auth",            tags=["Admin Auth"])
app.include_router(universities.router, prefix="/admin/universities",    tags=["Admin Universities"])
app.include_router(programs.router,     prefix="/admin/degree-programs", tags=["Admin Programs"])
app.include_router(dashboard.router,    prefix="/admin/dashboard",       tags=["Admin Dashboard"])

# ── Health ────────────────────────────────────────────────────
@app.get("/ping", tags=["Health"])
def ping():
    return {"status": "EduLink API is running", "version": "2.0.0"}

@app.get("/", tags=["Health"])
def root():
    return {"message": "Welcome to EduLink API", "docs": "/docs"}
