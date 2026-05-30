# ============================================================
# EduLink — FastAPI Main Application
# ============================================================

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import student, mcq, writing, report

app = FastAPI(
    title="EduLink API",
    description="AI-Driven Career Guidance System for Sri Lankan IT Students",
    version="1.0.0"
)

# Allow Flutter app to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register all routes
app.include_router(student.router, prefix="/student", tags=["Student"])
app.include_router(mcq.router,     prefix="/student", tags=["MCQ"])
app.include_router(writing.router, prefix="/student", tags=["Writing"])
app.include_router(report.router,  prefix="/student", tags=["Report"])

@app.get("/ping", tags=["Health"])
def ping():
    return {
        "status":  "EduLink API is running",
        "version": "1.0.0"
    }

@app.get("/", tags=["Health"])
def root():
    return {
        "message": "Welcome to EduLink API",
        "docs":    "http://localhost:8000/docs"
    }