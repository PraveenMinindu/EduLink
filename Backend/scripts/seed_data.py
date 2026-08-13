# =============================================================
# EduLink — Admin Panel Seed Script
# =============================================================
# Usage:
#   python seed_data.py --seed    Insert data only if empty
#   python seed_data.py --reset   Delete all + re-insert
#
# Run from Backend/ directory:
#   cd C:\Users\Praveen\Desktop\EduLink\Backend
#   python scripts/seed_data.py --seed
# =============================================================

import sys
import os
import argparse
from datetime import datetime

# ── Resolve Backend root so serviceAccountKey.json is found ──
BACKEND_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BACKEND_DIR)

import firebase_admin
from firebase_admin import credentials, firestore

# ── Init Firebase (reuse same pattern as firebase_bridge.py) ─
def init_firebase():
    if not firebase_admin._apps:
        key_path = os.path.join(BACKEND_DIR, "serviceAccountKey.json")
        if not os.path.exists(key_path):
            print(f"ERROR: serviceAccountKey.json not found at {key_path}")
            sys.exit(1)
        cred = credentials.Certificate(key_path)
        firebase_admin.initialize_app(cred)

def get_db():
    init_firebase()
    return firestore.client()

# =============================================================
# SEED DATA — Real Sri Lankan IT Universities
# =============================================================

NOW = datetime.utcnow().isoformat()
CREATED_BY = "seed_script"

UNIVERSITIES = [
    {
        "name": "University of Moratuwa",
        "type": "State",
        "location": "Moratuwa, Western Province",
        "website": "https://uom.lk",
        "shortDescription": "Sri Lanka's premier technological university, established in 1978.",
        "fullDescription": (
            "The University of Moratuwa is Sri Lanka's leading technological university, "
            "offering undergraduate and postgraduate programs in engineering, architecture, "
            "information technology, and business. It is recognised by the University Grants "
            "Commission and is consistently ranked as one of the top universities in Sri Lanka."
        ),
        "logoUrl": "https://uom.lk/images/logo.png",
        "status": "Active",
        "createdAt": NOW,
        "updatedAt": NOW,
        "createdBy": CREATED_BY,
        "updatedBy": CREATED_BY,
    },
    {
        "name": "Sri Lanka Institute of Information Technology (SLIIT)",
        "type": "Private",
        "location": "Malabe, Western Province",
        "website": "https://sliit.lk",
        "shortDescription": "Sri Lanka's largest private IT university with over 15,000 students.",
        "fullDescription": (
            "SLIIT is Sri Lanka's largest non-state institute dedicated to information technology "
            "and engineering education. Founded in 1999, it offers a wide range of undergraduate "
            "and postgraduate programs. SLIIT is accredited by the Institution of Engineers "
            "Sri Lanka (IESL) and the British Computer Society (BCS)."
        ),
        "logoUrl": "https://sliit.lk/wp-content/uploads/2019/08/SLIIT-logo.png",
        "status": "Active",
        "createdAt": NOW,
        "updatedAt": NOW,
        "createdBy": CREATED_BY,
        "updatedBy": CREATED_BY,
    },
    {
        "name": "NSBM Green University",
        "type": "Private",
        "location": "Pitipana, Homagama, Western Province",
        "website": "https://nsbm.ac.lk",
        "shortDescription": "Sri Lanka's first and only green university campus.",
        "fullDescription": (
            "NSBM Green University is a state-approved private degree-awarding institution "
            "in Sri Lanka. It offers degree programs in partnership with the University of "
            "Plymouth, UK. The university is known for its modern green campus and strong "
            "emphasis on computing, business, and engineering disciplines."
        ),
        "logoUrl": "https://nsbm.ac.lk/wp-content/uploads/2020/01/nsbm-logo.png",
        "status": "Active",
        "createdAt": NOW,
        "updatedAt": NOW,
        "createdBy": CREATED_BY,
        "updatedBy": CREATED_BY,
    },
    {
        "name": "APIIT Sri Lanka",
        "type": "Private",
        "location": "Colombo 03, Western Province",
        "website": "https://apiit.lk",
        "shortDescription": "Asia Pacific Institute of Information Technology — Staffordshire University partnership.",
        "fullDescription": (
            "APIIT Sri Lanka is a leading private higher education institution offering "
            "British degree programs in partnership with Staffordshire University, UK. "
            "It specialises in computing, engineering, and business programs. Graduates "
            "receive both a local and a UK degree upon completion."
        ),
        "logoUrl": "https://apiit.lk/wp-content/uploads/2021/03/APIIT-Logo.png",
        "status": "Active",
        "createdAt": NOW,
        "updatedAt": NOW,
        "createdBy": CREATED_BY,
        "updatedBy": CREATED_BY,
    },
    {
        "name": "University of Colombo School of Computing (UCSC)",
        "type": "State",
        "location": "Colombo 07, Western Province",
        "website": "https://ucsc.cmb.ac.lk",
        "shortDescription": "The dedicated computing faculty of the University of Colombo.",
        "fullDescription": (
            "The University of Colombo School of Computing is the dedicated computing "
            "faculty of the University of Colombo, established in 2002. It offers "
            "undergraduate and postgraduate programs in computer science and information "
            "systems, and is known for producing high-quality software engineering graduates."
        ),
        "logoUrl": "https://ucsc.cmb.ac.lk/wp-content/uploads/2020/01/ucsc-logo.png",
        "status": "Active",
        "createdAt": NOW,
        "updatedAt": NOW,
        "createdBy": CREATED_BY,
        "updatedBy": CREATED_BY,
    },
]


def build_programs(uni_map: dict) -> list:
    """
    Build degree_programs list using university IDs from uni_map.
    uni_map = { university_name: firestore_doc_id }
    """
    uom_id   = uni_map.get("University of Moratuwa", "")
    sliit_id = uni_map.get("Sri Lanka Institute of Information Technology (SLIIT)", "")
    nsbm_id  = uni_map.get("NSBM Green University", "")
    apiit_id = uni_map.get("APIIT Sri Lanka", "")
    ucsc_id  = uni_map.get("University of Colombo School of Computing (UCSC)", "")

    programs = [

        # ── University of Moratuwa ───────────────────────────
        {
            "_doc_id":        "uom_bsc_cse",  # seed-only — popped before Firestore write
            "universityId":   uom_id,
            "universityName": "University of Moratuwa",
            "degreeName":     "BSc (Hons) in Computer Science and Engineering",
            "faculty":        "Faculty of Engineering",
            "shortDescription": "A four-year honours degree in computer science and software engineering.",
            "fullDescription": (
                "This program provides a strong foundation in algorithms, data structures, "
                "operating systems, software engineering, and artificial intelligence. "
                "Students undertake an industry-based final year project."
            ),
            "duration":       "4 Years",
            "durationMonths": 48,
            "studyMode":      "Full-time",
            "medium":         "English",
            "qualification":  "BSc (Hons)",
            "entryRequirements": (
                "3 passes at A/L including Combined Mathematics. "
                "Z-score cutoff applies for state university admission."
            ),
            "feeType":        "Free",
            "tuitionFee":     0,
            "currency":       "LKR",
            "registrationFee": 0,
            "installmentAvailable": False,
            "campusName":     "Main Campus",
            "address":        "Moratuwa 10400, Sri Lanka",
            "latitude":       6.6508,
            "longitude":      79.9729,
            "nextIntake":     "October 2026",
            "applicationStatus": "Coming Soon",
            "applicationDeadline": "",
            "phone":          "+94 11 265 0301",
            "email":          "info@uom.lk",
            "officialWebsite": "https://uom.lk",
            "degreePageUrl":  "https://uom.lk/cse",
            "applyNowUrl":    "https://ugc.ac.lk",
            "ugcRecognized":  True,
            "ministryRecognized": True,
            "accreditation":  "IESL, BCS",
            "scholarships":   "Mahapola and Bursary scholarships available for eligible students.",
            "financialAid":   "Government-funded university. No tuition fees for qualified students.",
            "paymentPlans":   "Not applicable",
            "logoUrl":        "https://uom.lk/images/logo.png",
            "campusImageUrl": "",
            "virtualTourUrl": "",
            "brochureUrl":    "",
            "status":         "Active",
            "createdAt":      NOW,
            "updatedAt":      NOW,
            "createdBy":      CREATED_BY,
            "updatedBy":      CREATED_BY,
        },
        {
            "_doc_id":        "uom_bsc_it",  # seed-only — popped before Firestore write
            "universityId":   uom_id,
            "universityName": "University of Moratuwa",
            "degreeName":     "BSc (Hons) in Information Technology",
            "faculty":        "Faculty of Information Technology",
            "shortDescription": "A four-year IT degree focused on systems, networking, and software development.",
            "fullDescription": (
                "Covers information systems, database management, networking, web technologies, "
                "and IT project management. Designed to produce well-rounded IT professionals "
                "ready for the Sri Lankan and global technology industry."
            ),
            "duration":       "4 Years",
            "durationMonths": 48,
            "studyMode":      "Full-time",
            "medium":         "English",
            "qualification":  "BSc (Hons)",
            "entryRequirements": "3 passes at A/L. Z-score cutoff applies.",
            "feeType":        "Free",
            "tuitionFee":     0,
            "currency":       "LKR",
            "registrationFee": 0,
            "installmentAvailable": False,
            "campusName":     "Main Campus",
            "address":        "Moratuwa 10400, Sri Lanka",
            "latitude":       6.6508,
            "longitude":      79.9729,
            "nextIntake":     "October 2026",
            "applicationStatus": "Coming Soon",
            "applicationDeadline": "",
            "phone":          "+94 11 265 0301",
            "email":          "info@uom.lk",
            "officialWebsite": "https://uom.lk",
            "degreePageUrl":  "https://uom.lk/it",
            "applyNowUrl":    "https://ugc.ac.lk",
            "ugcRecognized":  True,
            "ministryRecognized": True,
            "accreditation":  "IESL",
            "scholarships":   "Mahapola and Bursary scholarships available.",
            "financialAid":   "Government-funded. No tuition fees.",
            "paymentPlans":   "Not applicable",
            "logoUrl":        "https://uom.lk/images/logo.png",
            "campusImageUrl": "",
            "virtualTourUrl": "",
            "brochureUrl":    "",
            "status":         "Active",
            "createdAt":      NOW,
            "updatedAt":      NOW,
            "createdBy":      CREATED_BY,
            "updatedBy":      CREATED_BY,
        },

        # ── SLIIT ─────────────────────────────────────────────
        {
            "_doc_id":        "sliit_bsc_it",  # seed-only — popped before Firestore write
            "universityId":   sliit_id,
            "universityName": "Sri Lanka Institute of Information Technology (SLIIT)",
            "degreeName":     "BSc (Hons) in Information Technology",
            "faculty":        "Faculty of Computing",
            "shortDescription": "A four-year IT program with specialisations in software engineering, data science, and cybersecurity.",
            "fullDescription": (
                "SLIIT's flagship IT degree allows students to specialise in one of several "
                "streams including Software Engineering, Data Science, Cybersecurity, "
                "and Information Systems. The program is accredited by BCS and IESL."
            ),
            "duration":       "4 Years",
            "durationMonths": 48,
            "studyMode":      "Full-time",
            "medium":         "English",
            "qualification":  "BSc (Hons)",
            "entryRequirements": (
                "3 passes at A/L or equivalent qualification. "
                "English proficiency required."
            ),
            "feeType":        "Paid",
            "tuitionFee":     375000,
            "currency":       "LKR",
            "registrationFee": 25000,
            "installmentAvailable": True,
            "campusName":     "Main Campus — Malabe",
            "address":        "New Kandy Road, Malabe 10115, Sri Lanka",
            "latitude":       6.9147,
            "longitude":      79.9731,
            "nextIntake":     "September 2026",
            "applicationStatus": "Open",
            "applicationDeadline": "2026-08-31",
            "phone":          "+94 11 754 4801",
            "email":          "info@sliit.lk",
            "officialWebsite": "https://sliit.lk",
            "degreePageUrl":  "https://sliit.lk/faculty-of-computing",
            "applyNowUrl":    "https://sliit.lk/apply",
            "ugcRecognized":  True,
            "ministryRecognized": True,
            "accreditation":  "BCS, IESL",
            "scholarships":   "Merit scholarships up to 50% fee waiver for A/L high achievers.",
            "financialAid":   "Student loan facility through partner banks available.",
            "paymentPlans":   "Semester-based installment payment plans available.",
            "logoUrl":        "https://sliit.lk/wp-content/uploads/2019/08/SLIIT-logo.png",
            "campusImageUrl": "",
            "virtualTourUrl": "",
            "brochureUrl":    "",
            "status":         "Active",
            "createdAt":      NOW,
            "updatedAt":      NOW,
            "createdBy":      CREATED_BY,
            "updatedBy":      CREATED_BY,
        },
        {
            "_doc_id":        "sliit_bsc_se",  # seed-only — popped before Firestore write
            "universityId":   sliit_id,
            "universityName": "Sri Lanka Institute of Information Technology (SLIIT)",
            "degreeName":     "BSc (Hons) in Software Engineering",
            "faculty":        "Faculty of Computing",
            "shortDescription": "A specialised software engineering degree with strong industry connections.",
            "fullDescription": (
                "Focused specifically on software development methodologies, agile practices, "
                "software architecture, and quality assurance. Students complete a major "
                "industry internship as part of the final year."
            ),
            "duration":       "4 Years",
            "durationMonths": 48,
            "studyMode":      "Full-time",
            "medium":         "English",
            "qualification":  "BSc (Hons)",
            "entryRequirements": "3 passes at A/L. English proficiency required.",
            "feeType":        "Paid",
            "tuitionFee":     390000,
            "currency":       "LKR",
            "registrationFee": 25000,
            "installmentAvailable": True,
            "campusName":     "Main Campus — Malabe",
            "address":        "New Kandy Road, Malabe 10115, Sri Lanka",
            "latitude":       6.9147,
            "longitude":      79.9731,
            "nextIntake":     "September 2026",
            "applicationStatus": "Open",
            "applicationDeadline": "2026-08-31",
            "phone":          "+94 11 754 4801",
            "email":          "info@sliit.lk",
            "officialWebsite": "https://sliit.lk",
            "degreePageUrl":  "https://sliit.lk/faculty-of-computing/software-engineering",
            "applyNowUrl":    "https://sliit.lk/apply",
            "ugcRecognized":  True,
            "ministryRecognized": True,
            "accreditation":  "BCS, IESL",
            "scholarships":   "Merit scholarships available for high achievers.",
            "financialAid":   "Student loan facility available through partner banks.",
            "paymentPlans":   "Semester-based installment payment plans available.",
            "logoUrl":        "https://sliit.lk/wp-content/uploads/2019/08/SLIIT-logo.png",
            "campusImageUrl": "",
            "virtualTourUrl": "",
            "brochureUrl":    "",
            "status":         "Active",
            "createdAt":      NOW,
            "updatedAt":      NOW,
            "createdBy":      CREATED_BY,
            "updatedBy":      CREATED_BY,
        },

        # ── NSBM ─────────────────────────────────────────────
        {
            "_doc_id":        "nsbm_bsc_computing",  # seed-only — popped before Firestore write
            "universityId":   nsbm_id,
            "universityName": "NSBM Green University",
            "degreeName":     "BSc (Hons) in Computing",
            "faculty":        "Faculty of Computing",
            "shortDescription": "A British degree in computing offered in partnership with the University of Plymouth, UK.",
            "fullDescription": (
                "This program is validated by the University of Plymouth, UK, and students "
                "receive both a local NSBM degree and a University of Plymouth award upon "
                "successful completion. The curriculum covers software development, "
                "networking, databases, and emerging technologies."
            ),
            "duration":       "3 Years",
            "durationMonths": 36,
            "studyMode":      "Full-time",
            "medium":         "English",
            "qualification":  "BSc (Hons)",
            "entryRequirements": (
                "2 passes at A/L and a pass in English at O/L. "
                "Mature entry pathways available."
            ),
            "feeType":        "Paid",
            "tuitionFee":     450000,
            "currency":       "LKR",
            "registrationFee": 30000,
            "installmentAvailable": True,
            "campusName":     "NSBM Green Campus",
            "address":        "Pitipana, Homagama 10206, Sri Lanka",
            "latitude":       6.8389,
            "longitude":      80.0280,
            "nextIntake":     "February 2026",
            "applicationStatus": "Open",
            "applicationDeadline": "2026-01-31",
            "phone":          "+94 11 544 5000",
            "email":          "info@nsbm.ac.lk",
            "officialWebsite": "https://nsbm.ac.lk",
            "degreePageUrl":  "https://nsbm.ac.lk/faculties/computing",
            "applyNowUrl":    "https://nsbm.ac.lk/apply",
            "ugcRecognized":  True,
            "ministryRecognized": True,
            "accreditation":  "University of Plymouth (UK)",
            "scholarships":   "Academic excellence scholarships available. Sports and cultural scholarships also offered.",
            "financialAid":   "Bank loan facility and installment payment plans available.",
            "paymentPlans":   "Semester-based installment plans. Bank loans accepted.",
            "logoUrl":        "https://nsbm.ac.lk/wp-content/uploads/2020/01/nsbm-logo.png",
            "campusImageUrl": "",
            "virtualTourUrl": "",
            "brochureUrl":    "",
            "status":         "Active",
            "createdAt":      NOW,
            "updatedAt":      NOW,
            "createdBy":      CREATED_BY,
            "updatedBy":      CREATED_BY,
        },

        # ── APIIT ─────────────────────────────────────────────
        {
            "_doc_id":        "apiit_bsc_computing",  # seed-only — popped before Firestore write
            "universityId":   apiit_id,
            "universityName": "APIIT Sri Lanka",
            "degreeName":     "BSc (Hons) in Computing",
            "faculty":        "School of Computing and Engineering",
            "shortDescription": "A Staffordshire University UK validated computing degree with dual award.",
            "fullDescription": (
                "Students earn both an APIIT Sri Lanka degree and a Staffordshire University "
                "UK degree upon completion. The program covers software development, "
                "web technologies, mobile computing, and IT project management. "
                "Strong industry connections and internship placement support provided."
            ),
            "duration":       "3 Years",
            "durationMonths": 36,
            "studyMode":      "Full-time",
            "medium":         "English",
            "qualification":  "BSc (Hons)",
            "entryRequirements": (
                "2 passes at A/L in any stream. "
                "Foundation program available for O/L leavers."
            ),
            "feeType":        "Paid",
            "tuitionFee":     520000,
            "currency":       "LKR",
            "registrationFee": 35000,
            "installmentAvailable": True,
            "campusName":     "APIIT City Campus",
            "address":        "388 Union Place, Colombo 02, Sri Lanka",
            "latitude":       6.9271,
            "longitude":      79.8612,
            "nextIntake":     "March 2026",
            "applicationStatus": "Open",
            "applicationDeadline": "2026-02-28",
            "phone":          "+94 11 267 2278",
            "email":          "info@apiit.lk",
            "officialWebsite": "https://apiit.lk",
            "degreePageUrl":  "https://apiit.lk/programs/computing",
            "applyNowUrl":    "https://apiit.lk/apply",
            "ugcRecognized":  True,
            "ministryRecognized": True,
            "accreditation":  "Staffordshire University (UK)",
            "scholarships":   "Early bird scholarships. Sibling discount available.",
            "financialAid":   "Bank loan facility available. Installment plans offered.",
            "paymentPlans":   "Flexible semester-based payment plans available.",
            "logoUrl":        "https://apiit.lk/wp-content/uploads/2021/03/APIIT-Logo.png",
            "campusImageUrl": "",
            "virtualTourUrl": "",
            "brochureUrl":    "",
            "status":         "Active",
            "createdAt":      NOW,
            "updatedAt":      NOW,
            "createdBy":      CREATED_BY,
            "updatedBy":      CREATED_BY,
        },

        # ── UCSC ─────────────────────────────────────────────
        {
            "_doc_id":        "ucsc_bsc_cs",  # seed-only — popped before Firestore write
            "universityId":   ucsc_id,
            "universityName": "University of Colombo School of Computing (UCSC)",
            "degreeName":     "BSc (Hons) in Computer Science",
            "faculty":        "School of Computing",
            "shortDescription": "A rigorous computer science degree from one of Sri Lanka's oldest universities.",
            "fullDescription": (
                "The UCSC BSc Computer Science program offers a strong theoretical and "
                "practical foundation in computing. Core modules include algorithms, "
                "data structures, software engineering, operating systems, and distributed "
                "systems. The program is fully funded by the government for eligible students."
            ),
            "duration":       "4 Years",
            "durationMonths": 48,
            "studyMode":      "Full-time",
            "medium":         "English",
            "qualification":  "BSc (Hons)",
            "entryRequirements": (
                "3 passes at A/L including Combined Mathematics or Physics with Combined Mathematics. "
                "Z-score cutoff applies."
            ),
            "feeType":        "Free",
            "tuitionFee":     0,
            "currency":       "LKR",
            "registrationFee": 0,
            "installmentAvailable": False,
            "campusName":     "UCSC Campus",
            "address":        "35 Reid Avenue, Colombo 07, Sri Lanka",
            "latitude":       6.9022,
            "longitude":      79.8607,
            "nextIntake":     "October 2026",
            "applicationStatus": "Coming Soon",
            "applicationDeadline": "",
            "phone":          "+94 11 258 9998",
            "email":          "info@ucsc.cmb.ac.lk",
            "officialWebsite": "https://ucsc.cmb.ac.lk",
            "degreePageUrl":  "https://ucsc.cmb.ac.lk/programs/bsc-cs",
            "applyNowUrl":    "https://ugc.ac.lk",
            "ugcRecognized":  True,
            "ministryRecognized": True,
            "accreditation":  "IESL, BCS",
            "scholarships":   "Mahapola and Bursary scholarships available.",
            "financialAid":   "Government-funded. No tuition fees for qualified students.",
            "paymentPlans":   "Not applicable",
            "logoUrl":        "https://ucsc.cmb.ac.lk/wp-content/uploads/2020/01/ucsc-logo.png",
            "campusImageUrl": "",
            "virtualTourUrl": "",
            "brochureUrl":    "",
            "status":         "Active",
            "createdAt":      NOW,
            "updatedAt":      NOW,
            "createdBy":      CREATED_BY,
            "updatedBy":      CREATED_BY,
        },
        {
            "_doc_id":        "ucsc_bsc_is",  # seed-only — popped before Firestore write
            "universityId":   ucsc_id,
            "universityName": "University of Colombo School of Computing (UCSC)",
            "degreeName":     "BSc (Hons) in Information Systems",
            "faculty":        "School of Computing",
            "shortDescription": "A four-year degree blending information systems, business, and technology.",
            "fullDescription": (
                "This program bridges technology and business by covering enterprise systems, "
                "database administration, business intelligence, and IT project management. "
                "Ideal for students interested in both the technical and managerial aspects "
                "of information systems in organisations."
            ),
            "duration":       "4 Years",
            "durationMonths": 48,
            "studyMode":      "Full-time",
            "medium":         "English",
            "qualification":  "BSc (Hons)",
            "entryRequirements": "3 passes at A/L. Z-score cutoff applies.",
            "feeType":        "Free",
            "tuitionFee":     0,
            "currency":       "LKR",
            "registrationFee": 0,
            "installmentAvailable": False,
            "campusName":     "UCSC Campus",
            "address":        "35 Reid Avenue, Colombo 07, Sri Lanka",
            "latitude":       6.9022,
            "longitude":      79.8607,
            "nextIntake":     "October 2026",
            "applicationStatus": "Coming Soon",
            "applicationDeadline": "",
            "phone":          "+94 11 258 9998",
            "email":          "info@ucsc.cmb.ac.lk",
            "officialWebsite": "https://ucsc.cmb.ac.lk",
            "degreePageUrl":  "https://ucsc.cmb.ac.lk/programs/bsc-is",
            "applyNowUrl":    "https://ugc.ac.lk",
            "ugcRecognized":  True,
            "ministryRecognized": True,
            "accreditation":  "IESL",
            "scholarships":   "Mahapola and Bursary scholarships available.",
            "financialAid":   "Government-funded. No tuition fees.",
            "paymentPlans":   "Not applicable",
            "logoUrl":        "https://ucsc.cmb.ac.lk/wp-content/uploads/2020/01/ucsc-logo.png",
            "campusImageUrl": "",
            "virtualTourUrl": "",
            "brochureUrl":    "",
            "status":         "Active",
            "createdAt":      NOW,
            "updatedAt":      NOW,
            "createdBy":      CREATED_BY,
            "updatedBy":      CREATED_BY,
        },
    ]

    return programs


# =============================================================
# ADMIN USER SEED
# =============================================================

ADMIN_USER = {
    "name":      "Praveen Weerakkody",
    "email":     "admin@edulink.lk",
    "role":      "admin",
    "createdAt": NOW,
    "lastLogin": NOW,
}


# =============================================================
# SEED OPERATIONS
# =============================================================

def seed(db, force: bool = False):
    """Insert data only if collections are empty.
    
    Args:
        force: If True, overwrite existing documents instead of skipping.
               Use during development when seed data fields have changed.
    """
    print("\n── Checking existing data ──────────────────────────")

    # Insert universities — always auto-ID (universities have no deterministic ID)
    uni_map = {}
    existing_unis = {d.to_dict().get("name"): d.id
                     for d in db.collection("universities").stream()}

    for uni in UNIVERSITIES:
        if uni["name"] in existing_unis:
            print(f"  SKIP  university: {uni['name']}")
            uni_map[uni["name"]] = existing_unis[uni["name"]]
        else:
            ref = db.collection("universities").document()
            ref.set(uni)
            uni_map[uni["name"]] = ref.id
            print(f"    +   university: {uni['name']}  ({ref.id})")

    # Insert programs using real university IDs
    print("\n  degree_programs → seeding...")
    programs = build_programs(uni_map)
    for prog in programs:
        # _doc_id is a seed-only field — removed before Firestore write
        doc_id = prog.pop("_doc_id")
        ref    = db.collection("degree_programs").document(doc_id)
        if not force and ref.get().exists:
            print(f"  SKIP  {doc_id}  ({prog['degreeName']})")
            prog["_doc_id"] = doc_id  # restore for idempotency on next iteration
            continue
        ref.set(prog)
        action = "FORCE" if force and ref.get().exists else "+"
        print(f"    {action}  {doc_id}  [{prog['universityName']}]")

    # Insert admin user
    print("\n  admin_users → checking...")
    existing_admin = list(db.collection("admin_users").limit(1).stream())
    if existing_admin:
        print("  admin_users    → already has data. Skipping.")
    else:
        ref = db.collection("admin_users").document()
        ref.set(ADMIN_USER)
        print(f"    + Admin user created  ({ref.id})")
        print("    NOTE: Update this document ID with your Firebase Auth UID.")

    print("\n✓ Seed complete.")
    print(f"  {len(UNIVERSITIES)} universities inserted.")
    print(f"  {len(programs)} degree programs inserted.")


def reset(db):
    """Delete all admin panel data then re-seed."""
    print("\n⚠  RESET MODE — This will DELETE all universities and programs.")
    confirm = input("   Type YES to confirm: ").strip()
    if confirm != "YES":
        print("   Reset cancelled.")
        return

    print("\n── Deleting existing data ──────────────────────────")

    # Delete universities
    docs = list(db.collection("universities").stream())
    for doc in docs:
        doc.reference.delete()
    print(f"  Deleted {len(docs)} universities.")

    # Delete degree_programs
    docs = list(db.collection("degree_programs").stream())
    for doc in docs:
        doc.reference.delete()
    print(f"  Deleted {len(docs)} degree programs.")

    # Delete admin_users
    docs = list(db.collection("admin_users").stream())
    for doc in docs:
        doc.reference.delete()
    print(f"  Deleted {len(docs)} admin users.")

    print("\n── Re-seeding ───────────────────────────────────────")
    seed(db, force=True)


# =============================================================
# ENTRY POINT
# =============================================================

def main():
    parser = argparse.ArgumentParser(
        description="EduLink Admin Panel — Firestore seed script",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            "  python scripts/seed_data.py --seed              Skip existing docs\n"
            "  python scripts/seed_data.py --seed --force      Overwrite existing docs\n"
            "  python scripts/seed_data.py --reset             Delete all + re-seed\n"
        )
    )
    parser.add_argument(
        "--seed",
        action="store_true",
        help="Insert seed data, skipping documents that already exist (idempotent)"
    )
    parser.add_argument(
        "--reset",
        action="store_true",
        help="Delete all admin panel data then re-insert fresh seed data"
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help=(
            "Used with --seed: overwrite existing documents instead of skipping. "
            "Use during development when seeded field values have changed."
        )
    )
    args = parser.parse_args()

    if not args.seed and not args.reset:
        parser.print_help()
        sys.exit(0)

    if args.seed and args.reset:
        print("ERROR: Use either --seed or --reset, not both.")
        sys.exit(1)

    if args.force and not args.seed:
        print("ERROR: --force can only be used with --seed.")
        sys.exit(1)

    db = get_db()

    if args.reset:
        reset(db)
    else:
        seed(db, force=args.force)


if __name__ == "__main__":
    main()
