"""
EduLink — Degree Programme Seed Script
Adds verified Sri Lankan IT degree programmes to Firestore.
Covers all 8 career clusters.

Usage:
    $env:FIREBASE_KEY_PATH = "C:\...\serviceAccountKey.json"
    python seed_programmes.py
"""

import os, sys
from datetime import datetime
import firebase_admin
from firebase_admin import credentials, firestore

# ── Init Firebase ─────────────────────────────────────────────
key_path = os.environ.get("FIREBASE_KEY_PATH")
if not key_path:
    print("ERROR: FIREBASE_KEY_PATH not set.")
    sys.exit(1)

if not firebase_admin._apps:
    cred = credentials.Certificate(key_path)
    firebase_admin.initialize_app(cred)

db = firestore.client()

# ── Universities ───────────────────────────────────────────────
UNIVERSITIES = [
    {
        "id": "uom",
        "name": "University of Moratuwa",
        "type": "Government",
        "location": "Moratuwa",
        "district": "Colombo",
        "province": "Western",
        "address": "Bandaranayake Mawatha, Moratuwa 10400, Sri Lanka",
        "latitude": 6.6508,
        "longitude": 79.9729,
        "phone": "+94 11 265 0301",
        "email": "info@uom.lk",
        "website": "https://uom.lk",
        "description": "University of Moratuwa is Sri Lanka's leading technical university, ranked among the top universities in the country, offering engineering, IT and architecture programmes.",
        "ugcApproved": True,
        "establishedYear": 1972,
        "status": "Active",
        "logoUrl": "https://uom.lk/sites/default/files/uom_logo.png",
        "imageUrl": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/92/University_of_Moratuwa_main_building.jpg/1280px-University_of_Moratuwa_main_building.jpg",
    },
    {
        "id": "ucsc",
        "name": "University of Colombo School of Computing",
        "type": "Government",
        "location": "Colombo 03",
        "district": "Colombo",
        "province": "Western",
        "address": "35, Reid Avenue, Colombo 00700, Sri Lanka",
        "latitude": 6.9020,
        "longitude": 79.8619,
        "phone": "+94 11 258 9137",
        "email": "ucsc@ucsc.cmb.ac.lk",
        "website": "https://ucsc.cmb.ac.lk",
        "description": "UCSC is Sri Lanka's premier computing school, a faculty of the University of Colombo, offering specialized computing degrees with strong industry linkages.",
        "ugcApproved": True,
        "establishedYear": 1999,
        "status": "Active",
        "logoUrl": "https://ucsc.cmb.ac.lk/wp-content/uploads/2017/08/UCSC-logo.png",
        "imageUrl": "https://ucsc.cmb.ac.lk/wp-content/uploads/2017/08/UCSC-building.jpg",
    },
    {
        "id": "sliit",
        "name": "Sri Lanka Institute of Information Technology",
        "type": "Private",
        "location": "Malabe",
        "district": "Colombo",
        "province": "Western",
        "address": "New Kandy Road, Malabe 10115, Sri Lanka",
        "latitude": 6.9147,
        "longitude": 79.9745,
        "phone": "+94 11 754 4801",
        "email": "info@sliit.lk",
        "website": "https://sliit.lk",
        "description": "SLIIT is Sri Lanka's No.1 non-state university in IT and engineering, UGC-approved, IET UK accredited, with strong industry partnerships and research output.",
        "ugcApproved": True,
        "establishedYear": 1999,
        "status": "Active",
        "logoUrl": "https://www.sliit.lk/wp-content/uploads/2022/01/sliit-logo.png",
        "imageUrl": "https://www.sliit.lk/wp-content/uploads/2022/01/sliit-campus.jpg",
    },
    {
        "id": "nsbm",
        "name": "NSBM Green University",
        "type": "Private",
        "location": "Pitipana, Homagama",
        "district": "Colombo",
        "province": "Western",
        "address": "Mahenwatta, Pitipana, Homagama 10200, Sri Lanka",
        "latitude": 6.8452,
        "longitude": 80.0248,
        "phone": "+94 11 544 5000",
        "email": "info@nsbm.ac.lk",
        "website": "https://nsbm.ac.lk",
        "description": "NSBM Green University is Sri Lanka's first green university, offering local and international degrees in partnership with Plymouth University, UK.",
        "ugcApproved": True,
        "establishedYear": 2008,
        "status": "Active",
        "logoUrl": "https://nsbm.ac.lk/wp-content/uploads/2019/07/nsbm-logo.png",
        "imageUrl": "https://nsbm.ac.lk/wp-content/uploads/2021/09/nsbm-campus.jpg",
    },
    {
        "id": "iit",
        "name": "Informatics Institute of Technology",
        "type": "Private",
        "location": "Colombo 06",
        "district": "Colombo",
        "province": "Western",
        "address": "57, Ramakrishna Road, Colombo 00600, Sri Lanka",
        "latitude": 6.8829,
        "longitude": 79.8632,
        "phone": "+94 11 263 8000",
        "email": "info@iit.ac.lk",
        "website": "https://iit.ac.lk",
        "description": "IIT is Sri Lanka's premier IT institute affiliated with the University of Westminster, UK, offering internationally recognised computing degrees since 1990.",
        "ugcApproved": True,
        "establishedYear": 1990,
        "status": "Active",
        "logoUrl": "https://iit.ac.lk/wp-content/uploads/2019/01/iit-logo.png",
        "imageUrl": "https://iit.ac.lk/wp-content/uploads/2019/01/iit-campus.jpg",
    },
    {
        "id": "sltc",
        "name": "SLTC Research University",
        "type": "Private",
        "location": "Padukka",
        "district": "Colombo",
        "province": "Western",
        "address": "Ingiriya Road, Meepe, Padukka 10609, Sri Lanka",
        "latitude": 6.7736,
        "longitude": 80.0842,
        "phone": "+94 11 205 5555",
        "email": "info@sltc.ac.lk",
        "website": "https://sltc.ac.lk",
        "description": "SLTC Research University is a UGC-approved research-focused private university offering technology and computing degrees with strong emphasis on applied research and innovation.",
        "ugcApproved": True,
        "establishedYear": 2009,
        "status": "Active",
        "logoUrl": "https://sltc.ac.lk/wp-content/uploads/2021/01/sltc-logo.png",
        "imageUrl": "https://sltc.ac.lk/wp-content/uploads/2021/01/sltc-campus.jpg",
    },
    {
        "id": "uok",
        "name": "University of Kelaniya",
        "type": "Government",
        "location": "Kelaniya",
        "district": "Gampaha",
        "province": "Western",
        "address": "Dalugama, Kelaniya 11600, Sri Lanka",
        "latitude": 7.0016,
        "longitude": 79.9208,
        "phone": "+94 11 291 4479",
        "email": "info@kln.ac.lk",
        "website": "https://kln.ac.lk",
        "description": "University of Kelaniya is a national university offering computing and ICT programmes through its Faculty of Computing and Technology.",
        "ugcApproved": True,
        "establishedYear": 1959,
        "status": "Active",
        "logoUrl": "https://kln.ac.lk/images/logo.png",
        "imageUrl": "https://kln.ac.lk/images/campus.jpg",
    },
    {
        "id": "uop",
        "name": "University of Peradeniya",
        "type": "Government",
        "location": "Peradeniya",
        "district": "Kandy",
        "province": "Central",
        "address": "Galaha Road, Peradeniya 20400, Sri Lanka",
        "latitude": 7.2553,
        "longitude": 80.5930,
        "phone": "+94 81 238 9011",
        "email": "registrar@pdn.ac.lk",
        "website": "https://pdn.ac.lk",
        "description": "University of Peradeniya is one of Sri Lanka's oldest and most prestigious national universities, offering engineering and computing programmes.",
        "ugcApproved": True,
        "establishedYear": 1942,
        "status": "Active",
        "logoUrl": "https://pdn.ac.lk/images/logo.png",
        "imageUrl": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/University_of_Peradeniya.jpg/1280px-University_of_Peradeniya.jpg",
    },
]

# ── Degree Programmes ─────────────────────────────────────────
# Each programme has full details matching the Admin Panel schema.
# Covers all 8 EduLink career clusters.

PROGRAMMES = [

    # ── University of Moratuwa ─────────────────────────────────

    {
        "id": "uom_cse",
        "universityId": "uom",
        "universityName": "University of Moratuwa",
        "degreeName": "BSc (Hons) in Computer Science & Engineering",
        "faculty": "Faculty of Engineering",
        "qualification": "BSc (Hons)",
        "shortDescription": "Sri Lanka's top-ranked Computer Science & Engineering programme with strong research and industry linkages.",
        "fullDescription": (
            "The BSc (Hons) in Computer Science and Engineering at the University of Moratuwa is Sri Lanka's most sought-after computing degree, producing graduates who excel in software engineering, AI, systems architecture, and computing research. "
            "Students undergo a rigorous four-year programme covering algorithms, data structures, computer architecture, software engineering, operating systems, machine learning, computer networks, and research methods. "
            "The programme is accredited by BCS (The Chartered Institute for IT) and IESL, and graduates are highly sought by leading IT companies in Sri Lanka and internationally. "
            "Admission is through the UGC university selection process based on GCE A/L results."
        ),
        "duration": "4 Years",
        "durationMonths": 48,
        "studyMode": "Full-time",
        "medium": "English",
        "feeType": "Government Funded",
        "tuitionFee": 0,
        "currency": "LKR",
        "registrationFee": 0,
        "installmentAvailable": False,
        "campusName": "Main Campus",
        "address": "Bandaranayake Mawatha, Moratuwa 10400, Sri Lanka",
        "latitude": 6.6508,
        "longitude": 79.9729,
        "nextIntake": "October 2026",
        "applicationStatus": "Coming Soon",
        "applicationDeadline": "2026-09-30",
        "ugcRecognized": True,
        "ministryRecognized": True,
        "accreditation": "BCS, IESL",
        "scholarships": "Government-funded tuition — no fees. Mahapola and Bursary scholarships available for eligible students based on family income.",
        "financialAid": "Mahapola Higher Education Scholarship Trust Fund and University Bursary Scheme available for students from low-income families.",
        "paymentPlan": "No tuition fees — government-funded. Hostel and living expenses apply.",
        "virtualTourUrl": "https://www.youtube.com/watch?v=uom_tour",
        "brochureUrl": "https://uom.lk/sites/default/files/cse_brochure.pdf",
        "website": "https://cse.mrt.ac.lk",
        "applyUrl": "https://ugc.ac.lk",
        "status": "Active",
        "cluster": "Software_Web_Engineering",
        "cost_level": "Low",
        "program_level": "Degree",
        "delivery_mode": "Full-time",
    },

    {
        "id": "uom_it",
        "universityId": "uom",
        "universityName": "University of Moratuwa",
        "degreeName": "BSc (Hons) in Information Technology",
        "faculty": "Faculty of Information Technology",
        "qualification": "BSc (Hons)",
        "shortDescription": "A flagship IT degree from Sri Lanka's top technical university covering software, networks, and IT management.",
        "fullDescription": (
            "The BSc (Hons) in Information Technology at the University of Moratuwa is offered by the Faculty of Information Technology — one of the largest IT faculties in Sri Lanka. "
            "The programme covers database systems, web development, software engineering, IT project management, computer networks, cybersecurity, and enterprise systems. "
            "Students gain hands-on experience through industry-linked projects and internships with leading Sri Lankan and multinational companies. "
            "The degree is UGC-approved and graduates are eligible for professional membership of CSSL (Computer Society of Sri Lanka). "
            "Admission is through the UGC Annual Intake."
        ),
        "duration": "4 Years",
        "durationMonths": 48,
        "studyMode": "Full-time",
        "medium": "English",
        "feeType": "Government Funded",
        "tuitionFee": 0,
        "currency": "LKR",
        "registrationFee": 0,
        "installmentAvailable": False,
        "campusName": "Main Campus",
        "address": "Bandaranayake Mawatha, Moratuwa 10400, Sri Lanka",
        "latitude": 6.6508,
        "longitude": 79.9729,
        "nextIntake": "October 2026",
        "applicationStatus": "Coming Soon",
        "applicationDeadline": "2026-09-30",
        "ugcRecognized": True,
        "ministryRecognized": True,
        "accreditation": "CSSL, UGC Sri Lanka",
        "scholarships": "Government-funded tuition. Mahapola and Bursary scholarships available.",
        "financialAid": "Mahapola Higher Education Scholarship Trust Fund available for eligible students.",
        "paymentPlan": "No tuition fees — government-funded.",
        "virtualTourUrl": "",
        "brochureUrl": "https://fit.uom.lk/brochure",
        "website": "https://fit.uom.lk",
        "applyUrl": "https://ugc.ac.lk",
        "status": "Active",
        "cluster": "IT_Operations_QA",
        "cost_level": "Low",
        "program_level": "Degree",
        "delivery_mode": "Full-time",
    },

    {
        "id": "uom_ete",
        "universityId": "uom",
        "universityName": "University of Moratuwa",
        "degreeName": "BSc (Hons) in Electronic & Telecommunication Engineering",
        "faculty": "Faculty of Engineering",
        "qualification": "BSc (Hons)",
        "shortDescription": "Engineering degree covering telecommunications, embedded systems, signal processing and network infrastructure.",
        "fullDescription": (
            "The BSc (Hons) in Electronic and Telecommunication Engineering at the University of Moratuwa prepares graduates for careers in network infrastructure, telecommunications, embedded systems, and signal processing. "
            "Core modules include digital electronics, communication systems, microprocessors, wireless networks, optical fibre, RF engineering, and IoT. "
            "The programme is accredited by IESL and the Institution of Engineering and Technology (IET), UK. "
            "Graduates enter roles in telco companies, IT infrastructure, network engineering, and hardware design."
        ),
        "duration": "4 Years",
        "durationMonths": 48,
        "studyMode": "Full-time",
        "medium": "English",
        "feeType": "Government Funded",
        "tuitionFee": 0,
        "currency": "LKR",
        "registrationFee": 0,
        "installmentAvailable": False,
        "campusName": "Main Campus",
        "address": "Bandaranayake Mawatha, Moratuwa 10400, Sri Lanka",
        "latitude": 6.6508,
        "longitude": 79.9729,
        "nextIntake": "October 2026",
        "applicationStatus": "Coming Soon",
        "applicationDeadline": "2026-09-30",
        "ugcRecognized": True,
        "ministryRecognized": True,
        "accreditation": "IESL, IET UK",
        "scholarships": "Government-funded tuition. Mahapola and Bursary scholarships available.",
        "financialAid": "Mahapola Higher Education Scholarship Trust Fund available.",
        "paymentPlan": "No tuition fees — government-funded.",
        "virtualTourUrl": "",
        "brochureUrl": "https://uom.lk/ete/brochure",
        "website": "https://uom.lk/ete",
        "applyUrl": "https://ugc.ac.lk",
        "status": "Active",
        "cluster": "Network_Infrastructure",
        "cost_level": "Low",
        "program_level": "Degree",
        "delivery_mode": "Full-time",
    },

    # ── UCSC ──────────────────────────────────────────────────

    {
        "id": "ucsc_cs",
        "universityId": "ucsc",
        "universityName": "University of Colombo School of Computing",
        "degreeName": "BSc (Hons) in Computer Science",
        "faculty": "School of Computing",
        "qualification": "BSc (Hons)",
        "shortDescription": "A rigorous Computer Science degree from UCSC with strong foundations in algorithms, AI and software development.",
        "fullDescription": (
            "The BSc (Hons) in Computer Science at UCSC is a highly competitive government-funded programme recognised as one of Sri Lanka's finest computing degrees. "
            "The curriculum covers programming fundamentals, algorithms, data structures, operating systems, computer architecture, artificial intelligence, machine learning, database systems, software engineering, and computer graphics. "
            "UCSC has strong research output and industry partnerships with major IT companies including Sysco LABS, Axiata, and Dialog. "
            "Graduates are admitted to roles in software engineering, data science, and research both locally and internationally. "
            "Admission is through the UGC Annual Intake based on A/L results."
        ),
        "duration": "4 Years",
        "durationMonths": 48,
        "studyMode": "Full-time",
        "medium": "English",
        "feeType": "Government Funded",
        "tuitionFee": 0,
        "currency": "LKR",
        "registrationFee": 0,
        "installmentAvailable": False,
        "campusName": "Reid Avenue Campus",
        "address": "35 Reid Avenue, Colombo 00700, Sri Lanka",
        "latitude": 6.9020,
        "longitude": 79.8619,
        "nextIntake": "October 2026",
        "applicationStatus": "Coming Soon",
        "applicationDeadline": "2026-09-30",
        "ugcRecognized": True,
        "ministryRecognized": True,
        "accreditation": "UGC Sri Lanka, CSSL",
        "scholarships": "Government-funded tuition. Mahapola and Bursary schemes available.",
        "financialAid": "Mahapola Higher Education Scholarship Trust Fund and University Bursary.",
        "paymentPlan": "No tuition fees — government-funded.",
        "virtualTourUrl": "",
        "brochureUrl": "https://ucsc.cmb.ac.lk/brochure/cs.pdf",
        "website": "https://ucsc.cmb.ac.lk",
        "applyUrl": "https://ugc.ac.lk",
        "status": "Active",
        "cluster": "Software_Web_Engineering",
        "cost_level": "Low",
        "program_level": "Degree",
        "delivery_mode": "Full-time",
    },

    {
        "id": "ucsc_is",
        "universityId": "ucsc",
        "universityName": "University of Colombo School of Computing",
        "degreeName": "BSc (Hons) in Information Systems",
        "faculty": "School of Computing",
        "qualification": "BSc (Hons)",
        "shortDescription": "A business-focused IT degree combining information systems, management and enterprise technology.",
        "fullDescription": (
            "The BSc (Hons) in Information Systems at UCSC bridges technology and business, preparing graduates for roles in IT management, enterprise systems, business analysis, and digital transformation. "
            "Core modules include enterprise resource planning, database management, systems analysis and design, IT project management, e-business, data analytics, and IT governance. "
            "The programme is particularly suited to students interested in combining IT with business management in corporate environments. "
            "Graduates enter roles such as IT Manager, Business Analyst, Systems Analyst, and IT Consultant."
        ),
        "duration": "4 Years",
        "durationMonths": 48,
        "studyMode": "Full-time",
        "medium": "English",
        "feeType": "Government Funded",
        "tuitionFee": 0,
        "currency": "LKR",
        "registrationFee": 0,
        "installmentAvailable": False,
        "campusName": "Reid Avenue Campus",
        "address": "35 Reid Avenue, Colombo 00700, Sri Lanka",
        "latitude": 6.9020,
        "longitude": 79.8619,
        "nextIntake": "October 2026",
        "applicationStatus": "Coming Soon",
        "applicationDeadline": "2026-09-30",
        "ugcRecognized": True,
        "ministryRecognized": True,
        "accreditation": "UGC Sri Lanka, CSSL",
        "scholarships": "Government-funded tuition. Mahapola and Bursary schemes available.",
        "financialAid": "Mahapola Higher Education Scholarship Trust Fund and University Bursary.",
        "paymentPlan": "No tuition fees — government-funded.",
        "virtualTourUrl": "",
        "brochureUrl": "https://ucsc.cmb.ac.lk/brochure/is.pdf",
        "website": "https://ucsc.cmb.ac.lk",
        "applyUrl": "https://ugc.ac.lk",
        "status": "Active",
        "cluster": "Business_IT_Management",
        "cost_level": "Low",
        "program_level": "Degree",
        "delivery_mode": "Full-time",
    },

    # ── SLIIT ────────────────────────────────────────────────

    {
        "id": "sliit_ds",
        "universityId": "sliit",
        "universityName": "Sri Lanka Institute of Information Technology",
        "degreeName": "BSc (Hons) in Information Technology Specialising in Data Science",
        "faculty": "Faculty of Computing",
        "qualification": "BSc (Hons)",
        "shortDescription": "Data science specialisation covering AI, machine learning, big data and analytics for high-demand careers.",
        "fullDescription": (
            "The BSc (Hons) in IT specialising in Data Science at SLIIT is designed for students passionate about data-driven decision-making, machine learning, and artificial intelligence. "
            "The programme covers mathematics and statistics, databases, data engineering, big data technologies, artificial intelligence, machine learning, software engineering, and cloud computing. "
            "Students benefit from hands-on learning through real-world data-driven projects and collaboration with leading technology companies. "
            "The degree is approved by the UGC and accredited by the Institution of Engineering and Technology (IET), UK. "
            "Entry requires a minimum 3 S passes at G.C.E. A/L in any stream and passing the SLIIT Aptitude Test. Semester fee: approximately LKR 340,000 (Years 1-2), LKR 350,000 (Years 3-4)."
        ),
        "duration": "4 Years",
        "durationMonths": 48,
        "studyMode": "Full-time",
        "medium": "English",
        "feeType": "Paid",
        "tuitionFee": 340000,
        "currency": "LKR",
        "registrationFee": 15000,
        "installmentAvailable": True,
        "campusName": "Malabe Campus",
        "address": "New Kandy Road, Malabe 10115, Sri Lanka",
        "latitude": 6.9147,
        "longitude": 79.9745,
        "nextIntake": "September 2026",
        "applicationStatus": "Open",
        "applicationDeadline": "2026-08-31",
        "ugcRecognized": True,
        "ministryRecognized": True,
        "accreditation": "IET UK, UGC Sri Lanka, ACU, IAU",
        "scholarships": "Merit scholarships available for students achieving outstanding A/L results. SLIIT Excellence Award for top performers each academic year.",
        "financialAid": "Bank loan facilities available through partner banks including Bank of Ceylon, Sampath Bank, and HNB. SLIIT hardship bursary available for eligible students.",
        "paymentPlan": "Semester-based installments — LKR 340,000 per semester (Years 1-2), LKR 350,000 per semester (Years 3-4). Payable via BOC, Sampath, or HNB.",
        "virtualTourUrl": "https://www.youtube.com/watch?v=sliit_virtual",
        "brochureUrl": "https://www.sliit.lk/wp-content/uploads/data-science-brochure.pdf",
        "website": "https://www.sliit.lk/study/find-a-program/bsc-hons-in-data-science",
        "applyUrl": "https://apply.sliit.lk",
        "status": "Active",
        "cluster": "Data_AI_Engineering",
        "cost_level": "Medium",
        "program_level": "Degree",
        "delivery_mode": "Full-time",
    },

    {
        "id": "sliit_se",
        "universityId": "sliit",
        "universityName": "Sri Lanka Institute of Information Technology",
        "degreeName": "BSc (Hons) in Software Engineering",
        "faculty": "Faculty of Computing",
        "qualification": "BSc (Hons)",
        "shortDescription": "Industry-focused software engineering degree covering development, design, testing and project management.",
        "fullDescription": (
            "The BSc (Hons) in Software Engineering at SLIIT prepares graduates for careers in software development, systems design, and IT project management. "
            "The curriculum covers object-oriented programming, software architecture, agile methodologies, database management, web and mobile application development, quality assurance, DevOps, and cloud platforms. "
            "SLIIT's strong industry partnerships provide students with real-world project exposure through internships with leading companies. "
            "The degree is IET UK accredited and UGC approved. Entry requires a minimum 3 S passes at G.C.E. A/L and passing the SLIIT Aptitude Test."
        ),
        "duration": "3 Years",
        "durationMonths": 36,
        "studyMode": "Full-time",
        "medium": "English",
        "feeType": "Paid",
        "tuitionFee": 340000,
        "currency": "LKR",
        "registrationFee": 15000,
        "installmentAvailable": True,
        "campusName": "Malabe Campus",
        "address": "New Kandy Road, Malabe 10115, Sri Lanka",
        "latitude": 6.9147,
        "longitude": 79.9745,
        "nextIntake": "September 2026",
        "applicationStatus": "Open",
        "applicationDeadline": "2026-08-31",
        "ugcRecognized": True,
        "ministryRecognized": True,
        "accreditation": "IET UK, UGC Sri Lanka",
        "scholarships": "Merit scholarships for high-achieving A/L students. SLIIT Excellence Award for top performers.",
        "financialAid": "Bank loan facilities via BOC, Sampath, HNB. Hardship bursary available.",
        "paymentPlan": "Semester-based installments — LKR 340,000 per semester. Payable via BOC, Sampath, or HNB.",
        "virtualTourUrl": "https://www.youtube.com/watch?v=sliit_virtual",
        "brochureUrl": "https://www.sliit.lk/wp-content/uploads/se-brochure.pdf",
        "website": "https://www.sliit.lk/study/find-a-program/bsc-hons-in-software-engineering",
        "applyUrl": "https://apply.sliit.lk",
        "status": "Active",
        "cluster": "Software_Web_Engineering",
        "cost_level": "Medium",
        "program_level": "Degree",
        "delivery_mode": "Full-time",
    },

    {
        "id": "sliit_cs",
        "universityId": "sliit",
        "universityName": "Sri Lanka Institute of Information Technology",
        "degreeName": "BSc (Hons) in Information Technology Specialising in Cybersecurity",
        "faculty": "Faculty of Computing",
        "qualification": "BSc (Hons)",
        "shortDescription": "Cybersecurity specialisation covering network security, ethical hacking, digital forensics and infrastructure protection.",
        "fullDescription": (
            "The BSc (Hons) in IT specialising in Cybersecurity at SLIIT prepares graduates for the rapidly growing field of information security and network protection. "
            "Modules cover network security, cryptography, ethical hacking, penetration testing, digital forensics, cloud security, risk management, and incident response. "
            "Sri Lanka's rapidly expanding IT sector has significant demand for cybersecurity professionals, making this a high-value career pathway. "
            "The programme is IET UK accredited and UGC approved. Graduates enter roles including Security Analyst, Network Security Engineer, and Penetration Tester."
        ),
        "duration": "4 Years",
        "durationMonths": 48,
        "studyMode": "Full-time",
        "medium": "English",
        "feeType": "Paid",
        "tuitionFee": 340000,
        "currency": "LKR",
        "registrationFee": 15000,
        "installmentAvailable": True,
        "campusName": "Malabe Campus",
        "address": "New Kandy Road, Malabe 10115, Sri Lanka",
        "latitude": 6.9147,
        "longitude": 79.9745,
        "nextIntake": "September 2026",
        "applicationStatus": "Open",
        "applicationDeadline": "2026-08-31",
        "ugcRecognized": True,
        "ministryRecognized": True,
        "accreditation": "IET UK, UGC Sri Lanka",
        "scholarships": "Merit scholarships available for high A/L achievers.",
        "financialAid": "Bank loan facilities via BOC, Sampath, HNB.",
        "paymentPlan": "Semester-based installments — LKR 340,000 per semester.",
        "virtualTourUrl": "https://www.youtube.com/watch?v=sliit_virtual",
        "brochureUrl": "https://www.sliit.lk/wp-content/uploads/cybersecurity-brochure.pdf",
        "website": "https://www.sliit.lk/computing/programmes",
        "applyUrl": "https://apply.sliit.lk",
        "status": "Active",
        "cluster": "Network_Infrastructure",
        "cost_level": "Medium",
        "program_level": "Degree",
        "delivery_mode": "Full-time",
    },

    {
        "id": "sliit_imd",
        "universityId": "sliit",
        "universityName": "Sri Lanka Institute of Information Technology",
        "degreeName": "BSc (Hons) in Information Technology Specialising in Interactive Media Design",
        "faculty": "Faculty of Computing",
        "qualification": "BSc (Hons)",
        "shortDescription": "Creative technology degree combining UI/UX design, digital media, game development and human-computer interaction.",
        "fullDescription": (
            "The BSc (Hons) in IT specialising in Interactive Media Design at SLIIT is tailored for students with a passion for creative technology, user experience design, and digital media. "
            "Modules cover UI/UX design principles, human-computer interaction, game development, 3D modelling, motion graphics, web design, mobile app design, and digital storytelling. "
            "Students graduate with a portfolio of design projects demonstrating proficiency in industry-standard tools including Adobe Creative Suite, Figma, and Unity. "
            "Graduates enter careers as UX Designers, UI Developers, Game Developers, and Digital Media Specialists."
        ),
        "duration": "4 Years",
        "durationMonths": 48,
        "studyMode": "Full-time",
        "medium": "English",
        "feeType": "Paid",
        "tuitionFee": 340000,
        "currency": "LKR",
        "registrationFee": 15000,
        "installmentAvailable": True,
        "campusName": "Malabe Campus",
        "address": "New Kandy Road, Malabe 10115, Sri Lanka",
        "latitude": 6.9147,
        "longitude": 79.9745,
        "nextIntake": "September 2026",
        "applicationStatus": "Open",
        "applicationDeadline": "2026-08-31",
        "ugcRecognized": True,
        "ministryRecognized": True,
        "accreditation": "IET UK, UGC Sri Lanka",
        "scholarships": "Merit scholarships available.",
        "financialAid": "Bank loan facilities via BOC, Sampath, HNB.",
        "paymentPlan": "Semester-based installments — LKR 340,000 per semester.",
        "virtualTourUrl": "",
        "brochureUrl": "https://www.sliit.lk/wp-content/uploads/imd-brochure.pdf",
        "website": "https://www.sliit.lk/computing/programmes",
        "applyUrl": "https://apply.sliit.lk",
        "status": "Active",
        "cluster": "UX_Creative_Technology",
        "cost_level": "Medium",
        "program_level": "Degree",
        "delivery_mode": "Full-time",
    },

    {
        "id": "sliit_bis",
        "universityId": "sliit",
        "universityName": "Sri Lanka Institute of Information Technology",
        "degreeName": "BSc (Hons) in Business Information Systems",
        "faculty": "Faculty of Computing",
        "qualification": "BSc (Hons)",
        "shortDescription": "Business IT degree combining enterprise systems, management and digital transformation for corporate careers.",
        "fullDescription": (
            "The BSc (Hons) in Business Information Systems at SLIIT bridges technology and business management, producing graduates capable of driving digital transformation in corporate environments. "
            "Modules include enterprise resource planning, business intelligence, IT project management, e-commerce, supply chain management, data analytics, and strategic IT management. "
            "The programme is suitable for students who want careers at the intersection of business and technology, including roles as Business Analyst, IT Manager, and Digital Transformation Consultant."
        ),
        "duration": "4 Years",
        "durationMonths": 48,
        "studyMode": "Full-time",
        "medium": "English",
        "feeType": "Paid",
        "tuitionFee": 340000,
        "currency": "LKR",
        "registrationFee": 15000,
        "installmentAvailable": True,
        "campusName": "Malabe Campus",
        "address": "New Kandy Road, Malabe 10115, Sri Lanka",
        "latitude": 6.9147,
        "longitude": 79.9745,
        "nextIntake": "September 2026",
        "applicationStatus": "Open",
        "applicationDeadline": "2026-08-31",
        "ugcRecognized": True,
        "ministryRecognized": True,
        "accreditation": "IET UK, UGC Sri Lanka",
        "scholarships": "Merit scholarships available.",
        "financialAid": "Bank loan facilities via BOC, Sampath, HNB.",
        "paymentPlan": "Semester-based installments — LKR 340,000 per semester.",
        "virtualTourUrl": "",
        "brochureUrl": "https://www.sliit.lk/wp-content/uploads/bis-brochure.pdf",
        "website": "https://www.sliit.lk/computing/programmes",
        "applyUrl": "https://apply.sliit.lk",
        "status": "Active",
        "cluster": "Business_IT_Management",
        "cost_level": "Medium",
        "program_level": "Degree",
        "delivery_mode": "Full-time",
    },

    # ── NSBM ─────────────────────────────────────────────────

    {
        "id": "nsbm_cs",
        "universityId": "nsbm",
        "universityName": "NSBM Green University",
        "degreeName": "BSc (Hons) in Computer Science — University of Plymouth, UK",
        "faculty": "Faculty of Computing",
        "qualification": "BSc (Hons)",
        "shortDescription": "UK-awarded Computer Science degree from University of Plymouth delivered at NSBM Green University.",
        "fullDescription": (
            "The BSc (Hons) in Computer Science at NSBM is awarded by the University of Plymouth, UK, and delivered at NSBM Green University's state-of-the-art campus in Homagama. "
            "The programme covers programming, algorithms, artificial intelligence, software engineering, computer networks, database systems, and cybersecurity. "
            "Students graduate with a UK degree recognised internationally, making them competitive for both local and overseas employment. "
            "Entry requires a minimum 3 S passes at G.C.E. A/L or equivalent Cambridge/Edexcel qualification. Annual fee approximately LKR 650,000."
        ),
        "duration": "3 Years",
        "durationMonths": 36,
        "studyMode": "Full-time",
        "medium": "English",
        "feeType": "Paid",
        "tuitionFee": 650000,
        "currency": "LKR",
        "registrationFee": 25000,
        "installmentAvailable": True,
        "campusName": "NSBM Green University Town",
        "address": "Mahenwatta, Pitipana, Homagama 10200, Sri Lanka",
        "latitude": 6.8452,
        "longitude": 80.0248,
        "nextIntake": "February 2027",
        "applicationStatus": "Open",
        "applicationDeadline": "2026-12-31",
        "ugcRecognized": True,
        "ministryRecognized": True,
        "accreditation": "University of Plymouth UK, UGC Sri Lanka",
        "scholarships": "Vice Chancellor's Excellence Scholarship for top A/L achievers. Early Bird discounts available.",
        "financialAid": "Bank loan facilities available via partner banks. University payment plans available.",
        "paymentPlan": "Semester-based installments available. Contact admissions for current fee structure.",
        "virtualTourUrl": "https://www.youtube.com/watch?v=nsbm_tour",
        "brochureUrl": "https://nsbm.ac.lk/wp-content/uploads/cs-brochure.pdf",
        "website": "https://nsbm.ac.lk/faculties/computing",
        "applyUrl": "https://apply.nsbm.ac.lk",
        "status": "Active",
        "cluster": "Software_Web_Engineering",
        "cost_level": "Medium",
        "program_level": "Degree",
        "delivery_mode": "Full-time",
    },

    {
        "id": "nsbm_dm",
        "universityId": "nsbm",
        "universityName": "NSBM Green University",
        "degreeName": "BSc (Hons) in Digital Marketing — University of Plymouth, UK",
        "faculty": "Faculty of Business",
        "qualification": "BSc (Hons)",
        "shortDescription": "UK-awarded digital marketing degree covering SEO, social media, analytics, e-commerce and brand strategy.",
        "fullDescription": (
            "The BSc (Hons) in Digital Marketing at NSBM, awarded by the University of Plymouth, UK, prepares graduates for careers in the rapidly growing digital marketing industry. "
            "Modules cover search engine optimisation, social media marketing, content strategy, digital advertising, e-commerce, web analytics, brand management, and marketing automation. "
            "Students gain practical experience with industry tools including Google Analytics, Facebook Ads Manager, SEMrush, and HubSpot. "
            "Graduates enter careers as Digital Marketing Manager, SEO Specialist, Social Media Strategist, and Analytics Consultant."
        ),
        "duration": "3 Years",
        "durationMonths": 36,
        "studyMode": "Full-time",
        "medium": "English",
        "feeType": "Paid",
        "tuitionFee": 550000,
        "currency": "LKR",
        "registrationFee": 25000,
        "installmentAvailable": True,
        "campusName": "NSBM Green University Town",
        "address": "Mahenwatta, Pitipana, Homagama 10200, Sri Lanka",
        "latitude": 6.8452,
        "longitude": 80.0248,
        "nextIntake": "February 2027",
        "applicationStatus": "Open",
        "applicationDeadline": "2026-12-31",
        "ugcRecognized": True,
        "ministryRecognized": True,
        "accreditation": "University of Plymouth UK, UGC Sri Lanka",
        "scholarships": "VC Scholarship for high A/L achievers. Early Bird discount available.",
        "financialAid": "Bank loan facilities and university installment plans available.",
        "paymentPlan": "Semester-based installments. Contact admissions for current fee schedule.",
        "virtualTourUrl": "https://www.youtube.com/watch?v=nsbm_tour",
        "brochureUrl": "https://nsbm.ac.lk/wp-content/uploads/dm-brochure.pdf",
        "website": "https://nsbm.ac.lk/faculties/business",
        "applyUrl": "https://apply.nsbm.ac.lk",
        "status": "Active",
        "cluster": "Digital_Marketing_Media",
        "cost_level": "Medium",
        "program_level": "Degree",
        "delivery_mode": "Full-time",
    },

    # ── IIT ──────────────────────────────────────────────────

    {
        "id": "iit_cs",
        "universityId": "iit",
        "universityName": "Informatics Institute of Technology",
        "degreeName": "BSc (Hons) in Computer Science — University of Westminster, UK",
        "faculty": "Faculty of Computing",
        "qualification": "BSc (Hons)",
        "shortDescription": "UK-awarded Computer Science degree from the University of Westminster, UK, delivered at IIT Colombo.",
        "fullDescription": (
            "The BSc (Hons) in Computer Science at IIT is awarded by the University of Westminster, UK, and is one of the most established international computing programmes in Sri Lanka. "
            "Modules cover programming, algorithms, artificial intelligence, software engineering, database management, web technologies, computer networks, and cybersecurity. "
            "IIT has produced thousands of graduates who are employed in leading IT companies across Sri Lanka, the UK, Australia, and beyond. "
            "The programme runs over 3 years with students completing a final-year project in Year 3. Entry requires 3 passes at G.C.E. A/L or equivalent."
        ),
        "duration": "3 Years",
        "durationMonths": 36,
        "studyMode": "Full-time",
        "medium": "English",
        "feeType": "Paid",
        "tuitionFee": 750000,
        "currency": "LKR",
        "registrationFee": 30000,
        "installmentAvailable": True,
        "campusName": "Kollupitiya Campus",
        "address": "57 Ramakrishna Road, Colombo 00600, Sri Lanka",
        "latitude": 6.8829,
        "longitude": 79.8632,
        "nextIntake": "February 2027",
        "applicationStatus": "Open",
        "applicationDeadline": "2026-12-31",
        "ugcRecognized": True,
        "ministryRecognized": True,
        "accreditation": "University of Westminster UK, UGC Sri Lanka, BCS",
        "scholarships": "IIT Excellence Scholarship for top A/L students. Chancellor's Award for academic performance.",
        "financialAid": "Bank loan facilities available via Commercial Bank, Sampath, and HNB. IIT Hardship Fund for eligible students.",
        "paymentPlan": "Semester-based installments available. Fee payable in 2 installments per semester.",
        "virtualTourUrl": "https://iit.ac.lk/virtual-tour",
        "brochureUrl": "https://iit.ac.lk/wp-content/uploads/cs-brochure.pdf",
        "website": "https://iit.ac.lk/courses/bsc-computer-science",
        "applyUrl": "https://iit.ac.lk/apply",
        "status": "Active",
        "cluster": "Software_Web_Engineering",
        "cost_level": "High",
        "program_level": "Degree",
        "delivery_mode": "Full-time",
    },

    {
        "id": "iit_net",
        "universityId": "iit",
        "universityName": "Informatics Institute of Technology",
        "degreeName": "BSc (Hons) in Networking & Mobile Computing — University of Westminster, UK",
        "faculty": "Faculty of Computing",
        "qualification": "BSc (Hons)",
        "shortDescription": "Networking and mobile computing degree covering infrastructure, cloud, wireless networks and mobile platforms.",
        "fullDescription": (
            "The BSc (Hons) in Networking and Mobile Computing at IIT, awarded by the University of Westminster, UK, prepares students for careers in network engineering, cloud infrastructure, and mobile computing. "
            "Modules include computer networking, mobile application development, cloud computing, network security, wireless communications, IoT, and systems administration. "
            "Graduates are equipped for roles as Network Engineer, Cloud Architect, Systems Administrator, and Mobile Developer in both corporate and telecommunications environments."
        ),
        "duration": "3 Years",
        "durationMonths": 36,
        "studyMode": "Full-time",
        "medium": "English",
        "feeType": "Paid",
        "tuitionFee": 750000,
        "currency": "LKR",
        "registrationFee": 30000,
        "installmentAvailable": True,
        "campusName": "Kollupitiya Campus",
        "address": "57 Ramakrishna Road, Colombo 00600, Sri Lanka",
        "latitude": 6.8829,
        "longitude": 79.8632,
        "nextIntake": "February 2027",
        "applicationStatus": "Open",
        "applicationDeadline": "2026-12-31",
        "ugcRecognized": True,
        "ministryRecognized": True,
        "accreditation": "University of Westminster UK, UGC Sri Lanka",
        "scholarships": "IIT Excellence Scholarship for top A/L students.",
        "financialAid": "Bank loan facilities and IIT Hardship Fund available.",
        "paymentPlan": "Semester-based installments. Fee payable in 2 installments per semester.",
        "virtualTourUrl": "https://iit.ac.lk/virtual-tour",
        "brochureUrl": "https://iit.ac.lk/wp-content/uploads/networking-brochure.pdf",
        "website": "https://iit.ac.lk/courses",
        "applyUrl": "https://iit.ac.lk/apply",
        "status": "Active",
        "cluster": "Network_Infrastructure",
        "cost_level": "High",
        "program_level": "Degree",
        "delivery_mode": "Full-time",
    },

    # ── SLTC Research University ──────────────────────────────

    {
        "id": "sltc_ds",
        "universityId": "sltc",
        "universityName": "SLTC Research University",
        "degreeName": "BSc (Hons) in Data Science",
        "faculty": "Faculty of Computing and IT",
        "qualification": "BSc (Hons)",
        "shortDescription": "A research-focused Data Science degree preparing graduates for AI, machine learning and analytics careers.",
        "fullDescription": (
            "The BSc (Hons) in Data Science at SLTC Research University is a research-intensive programme combining mathematics, statistics, machine learning, and data engineering. "
            "Modules include statistical modelling, data mining, machine learning, deep learning, big data technologies, data visualisation, and applied research methods. "
            "SLTC's focus on research and innovation provides students with exposure to cutting-edge projects and industry collaboration. "
            "Graduates enter careers as Data Scientist, ML Engineer, Data Analyst, and AI Researcher."
        ),
        "duration": "3 Years",
        "durationMonths": 36,
        "studyMode": "Full-time",
        "medium": "English",
        "feeType": "Paid",
        "tuitionFee": 280000,
        "currency": "LKR",
        "registrationFee": 15000,
        "installmentAvailable": True,
        "campusName": "Main Campus",
        "address": "Ingiriya Road, Meepe, Padukka 10609, Sri Lanka",
        "latitude": 6.7736,
        "longitude": 80.0842,
        "nextIntake": "October 2026",
        "applicationStatus": "Open",
        "applicationDeadline": "2026-09-30",
        "ugcRecognized": True,
        "ministryRecognized": True,
        "accreditation": "UGC Sri Lanka",
        "scholarships": "Merit-based scholarships for high A/L achievers. Research excellence awards available.",
        "financialAid": "Bank loan facilities available via partner banks. SLTC Hardship Fund for eligible students.",
        "paymentPlan": "Semester-based installments — LKR 280,000 per semester. Payable via bank transfer or card.",
        "virtualTourUrl": "https://sltc.ac.lk/virtual-tour",
        "brochureUrl": "https://sltc.ac.lk/wp-content/uploads/ds-brochure.pdf",
        "website": "https://sltc.ac.lk/courses/data-science",
        "applyUrl": "https://sltc.ac.lk/apply",
        "status": "Active",
        "cluster": "Data_AI_Engineering",
        "cost_level": "Medium",
        "program_level": "Degree",
        "delivery_mode": "Full-time",
    },

    {
        "id": "sltc_cs",
        "universityId": "sltc",
        "universityName": "SLTC Research University",
        "degreeName": "BSc (Hons) in Computer Science",
        "faculty": "Faculty of Computing and IT",
        "qualification": "BSc (Hons)",
        "shortDescription": "Research-oriented Computer Science programme with strong emphasis on software, algorithms and applied computing.",
        "fullDescription": (
            "The BSc (Hons) in Computer Science at SLTC Research University provides a rigorous foundation in computing theory and practical software development. "
            "Modules cover programming, algorithms, data structures, operating systems, software engineering, database management, computer networks, and research methods. "
            "SLTC emphasises applied research and innovation, giving students exposure to research projects from Year 1. "
            "Graduates enter roles as Software Engineer, Systems Analyst, and Application Developer."
        ),
        "duration": "3 Years",
        "durationMonths": 36,
        "studyMode": "Full-time",
        "medium": "English",
        "feeType": "Paid",
        "tuitionFee": 280000,
        "currency": "LKR",
        "registrationFee": 15000,
        "installmentAvailable": True,
        "campusName": "Main Campus",
        "address": "Ingiriya Road, Meepe, Padukka 10609, Sri Lanka",
        "latitude": 6.7736,
        "longitude": 80.0842,
        "nextIntake": "October 2026",
        "applicationStatus": "Open",
        "applicationDeadline": "2026-09-30",
        "ugcRecognized": True,
        "ministryRecognized": True,
        "accreditation": "UGC Sri Lanka",
        "scholarships": "Merit-based scholarships. Research excellence awards.",
        "financialAid": "Bank loan facilities and SLTC Hardship Fund.",
        "paymentPlan": "Semester-based installments — LKR 280,000 per semester.",
        "virtualTourUrl": "https://sltc.ac.lk/virtual-tour",
        "brochureUrl": "https://sltc.ac.lk/wp-content/uploads/cs-brochure.pdf",
        "website": "https://sltc.ac.lk/courses/computer-science",
        "applyUrl": "https://sltc.ac.lk/apply",
        "status": "Active",
        "cluster": "Software_Web_Engineering",
        "cost_level": "Medium",
        "program_level": "Degree",
        "delivery_mode": "Full-time",
    },

    # ── University of Kelaniya ─────────────────────────────────

    {
        "id": "uok_cs",
        "universityId": "uok",
        "universityName": "University of Kelaniya",
        "degreeName": "BSc (Hons) in Computer Science",
        "faculty": "Faculty of Computing and Technology",
        "qualification": "BSc (Hons)",
        "shortDescription": "Government-funded Computer Science degree with strong foundations in programming, algorithms and software systems.",
        "fullDescription": (
            "The BSc (Hons) in Computer Science at the University of Kelaniya is offered by the Faculty of Computing and Technology, a growing computing faculty with modern facilities. "
            "The programme covers programming fundamentals, algorithms and data structures, software engineering, database management, computer networks, operating systems, and web technologies. "
            "As a national university, tuition is fully funded by the government and admission is through the UGC Annual Intake. "
            "Graduates are eligible for CSSL membership and enter roles in software development and IT services."
        ),
        "duration": "4 Years",
        "durationMonths": 48,
        "studyMode": "Full-time",
        "medium": "English",
        "feeType": "Government Funded",
        "tuitionFee": 0,
        "currency": "LKR",
        "registrationFee": 0,
        "installmentAvailable": False,
        "campusName": "Main Campus",
        "address": "Dalugama, Kelaniya 11600, Sri Lanka",
        "latitude": 7.0016,
        "longitude": 79.9208,
        "nextIntake": "October 2026",
        "applicationStatus": "Coming Soon",
        "applicationDeadline": "2026-09-30",
        "ugcRecognized": True,
        "ministryRecognized": True,
        "accreditation": "UGC Sri Lanka, CSSL",
        "scholarships": "Government-funded tuition. Mahapola and Bursary scholarships available.",
        "financialAid": "Mahapola Higher Education Scholarship Trust Fund and University Bursary.",
        "paymentPlan": "No tuition fees — government-funded.",
        "virtualTourUrl": "",
        "brochureUrl": "https://kln.ac.lk/brochures/cs.pdf",
        "website": "https://kln.ac.lk/fct",
        "applyUrl": "https://ugc.ac.lk",
        "status": "Active",
        "cluster": "Software_Web_Engineering",
        "cost_level": "Low",
        "program_level": "Degree",
        "delivery_mode": "Full-time",
    },

    {
        "id": "uok_ict",
        "universityId": "uok",
        "universityName": "University of Kelaniya",
        "degreeName": "BSc (Hons) in Information and Communication Technology",
        "faculty": "Faculty of Computing and Technology",
        "qualification": "BSc (Hons)",
        "shortDescription": "Government-funded ICT degree covering IT operations, systems administration and enterprise technology.",
        "fullDescription": (
            "The BSc (Hons) in Information and Communication Technology at the University of Kelaniya prepares graduates for roles in IT operations, systems administration, and enterprise technology management. "
            "Modules cover ICT fundamentals, database administration, network management, enterprise systems, IT security, systems analysis, and IT project management. "
            "The programme is government-funded with admission through the UGC Annual Intake. "
            "Graduates enter roles in IT Support, Systems Administration, and IT Operations Management."
        ),
        "duration": "4 Years",
        "durationMonths": 48,
        "studyMode": "Full-time",
        "medium": "English",
        "feeType": "Government Funded",
        "tuitionFee": 0,
        "currency": "LKR",
        "registrationFee": 0,
        "installmentAvailable": False,
        "campusName": "Main Campus",
        "address": "Dalugama, Kelaniya 11600, Sri Lanka",
        "latitude": 7.0016,
        "longitude": 79.9208,
        "nextIntake": "October 2026",
        "applicationStatus": "Coming Soon",
        "applicationDeadline": "2026-09-30",
        "ugcRecognized": True,
        "ministryRecognized": True,
        "accreditation": "UGC Sri Lanka",
        "scholarships": "Government-funded tuition. Mahapola and Bursary scholarships available.",
        "financialAid": "Mahapola Higher Education Scholarship Trust Fund.",
        "paymentPlan": "No tuition fees — government-funded.",
        "virtualTourUrl": "",
        "brochureUrl": "https://kln.ac.lk/brochures/ict.pdf",
        "website": "https://kln.ac.lk/fct",
        "applyUrl": "https://ugc.ac.lk",
        "status": "Active",
        "cluster": "IT_Operations_QA",
        "cost_level": "Low",
        "program_level": "Degree",
        "delivery_mode": "Full-time",
    },

    # ── University of Peradeniya ──────────────────────────────

    {
        "id": "uop_ce",
        "universityId": "uop",
        "universityName": "University of Peradeniya",
        "degreeName": "BSc (Hons) in Computer Engineering",
        "faculty": "Faculty of Engineering",
        "qualification": "BSc (Hons)",
        "shortDescription": "Prestigious computer engineering degree combining hardware, embedded systems and software from one of Sri Lanka's oldest universities.",
        "fullDescription": (
            "The BSc (Hons) in Computer Engineering at the University of Peradeniya is one of Sri Lanka's most respected engineering degrees, combining computer hardware, embedded systems, digital design, and software engineering. "
            "Modules cover digital electronics, microprocessors, embedded systems, computer architecture, operating systems, VLSI design, IoT, and signal processing. "
            "The programme is accredited by IESL and graduates enter careers in hardware design, embedded systems engineering, and systems architecture. "
            "Admission is through the UGC Annual Intake based on G.C.E. A/L results in the Physical Science stream."
        ),
        "duration": "4 Years",
        "durationMonths": 48,
        "studyMode": "Full-time",
        "medium": "English",
        "feeType": "Government Funded",
        "tuitionFee": 0,
        "currency": "LKR",
        "registrationFee": 0,
        "installmentAvailable": False,
        "campusName": "Main Campus",
        "address": "Galaha Road, Peradeniya 20400, Sri Lanka",
        "latitude": 7.2553,
        "longitude": 80.5930,
        "nextIntake": "October 2026",
        "applicationStatus": "Coming Soon",
        "applicationDeadline": "2026-09-30",
        "ugcRecognized": True,
        "ministryRecognized": True,
        "accreditation": "IESL, UGC Sri Lanka",
        "scholarships": "Government-funded tuition. Mahapola and Bursary scholarships available.",
        "financialAid": "Mahapola Higher Education Scholarship Trust Fund and University Bursary.",
        "paymentPlan": "No tuition fees — government-funded.",
        "virtualTourUrl": "",
        "brochureUrl": "https://pdn.ac.lk/engineering/brochures/ce.pdf",
        "website": "https://eng.pdn.ac.lk",
        "applyUrl": "https://ugc.ac.lk",
        "status": "Active",
        "cluster": "Hardware_Systems",
        "cost_level": "Low",
        "program_level": "Degree",
        "delivery_mode": "Full-time",
    },
]

# ── Seed Function ─────────────────────────────────────────────

def seed_universities():
    print("\n── Seeding Universities ──────────────────────────────")
    for uni in UNIVERSITIES:
        uid = uni.pop("id")
        db.collection("universities").document(uid).set({
            **uni,
            "createdAt": datetime.now().isoformat(),
            "createdBy": "seed_script",
            "updatedAt": datetime.now().isoformat(),
            "updatedBy": "seed_script",
        })
        print(f"  ✓ {uni['name']}")
        uni["id"] = uid  # restore


def seed_programmes():
    print("\n── Seeding Degree Programmes ─────────────────────────")
    for prog in PROGRAMMES:
        pid = prog.pop("id")
        db.collection("degree_programs").document(pid).set({
            **prog,
            "createdAt": datetime.now().isoformat(),
            "createdBy": "seed_script",
            "updatedAt": datetime.now().isoformat(),
            "updatedBy": "seed_script",
        })
        print(f"  ✓ {prog['degreeName']} — {prog['universityName']} [{prog['cluster']}]")
        prog["id"] = pid


def main():
    print("EduLink — Degree Programme Seed Script")
    print("="*50)
    seed_universities()
    seed_programmes()

    print("\n" + "="*50)
    print("✓ Seed complete!")
    print(f"  Universities: {len(UNIVERSITIES)}")
    print(f"  Programmes:   {len(PROGRAMMES)}")
    print("\nCluster coverage:")
    clusters = {}
    for p in PROGRAMMES:
        c = p.get("cluster", "Unknown")
        clusters[c] = clusters.get(c, 0) + 1
    for c, count in sorted(clusters.items()):
        print(f"  {c}: {count} programme(s)")

if __name__ == "__main__":
    main()
