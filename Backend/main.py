# ============================================================
# EduLink — FastAPI Main Application
# ============================================================

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import student, mcq, writing, report
from routes import report_v2

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

# Existing routes — unchanged
app.include_router(student.router, prefix="/student", tags=["Student"])
app.include_router(mcq.router,     prefix="/student", tags=["MCQ"])
app.include_router(writing.router, prefix="/student", tags=["Writing"])
app.include_router(report.router,  prefix="/student", tags=["Report"])

# V2 routes — assessment-based
app.include_router(report_v2.router, prefix="/student", tags=["Report V2"])

@app.get("/ping", tags=["Health"])
def ping():
    return {"status": "EduLink API is running", "version": "2.0.0"}

@app.get("/", tags=["Health"])
def root():
    return {"message": "Welcome to EduLink API",
            "docs": "http://localhost:8001/docs"}
