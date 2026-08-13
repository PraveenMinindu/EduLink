# =============================================================
# EduLink — Program Cluster Mapping
# =============================================================
# Data only. No logic. No imports. No caching.
# No Firestore references.
#
# PROGRAM_CLUSTER_MAP  : doc_id -> cluster list (canonical)
# PROGRAM_CLUSTER_FALLBACK : (universityName, degreeName) -> doc_id
#
# To add a new program from the Admin Panel:
#   1. Add its doc_id and cluster list to PROGRAM_CLUSTER_MAP.
#   2. Add its (universityName, degreeName) → doc_id entry to
#      PROGRAM_CLUSTER_FALLBACK.
# =============================================================

# ── Canonical cluster mapping — one entry per seeded program ──
# Key:   deterministic Firestore document ID (set by seed_data.py)
# Value: list of career clusters this program maps to
#        (primary cluster first)

PROGRAM_CLUSTER_MAP: dict[str, list[str]] = {
    "uom_bsc_cse":         ["Data_AI_Engineering",
                            "Software_Web_Engineering"],
    "uom_bsc_it":          ["Software_Web_Engineering",
                            "IT_Operations_QA"],
    "sliit_bsc_it":        ["Software_Web_Engineering",
                            "Data_AI_Engineering"],
    "sliit_bsc_se":        ["Software_Web_Engineering"],
    "nsbm_bsc_computing":  ["Software_Web_Engineering",
                            "Business_IT_Management"],
    "apiit_bsc_computing": ["Software_Web_Engineering",
                            "Business_IT_Management"],
    "ucsc_bsc_cs":         ["Data_AI_Engineering",
                            "Software_Web_Engineering"],
    "ucsc_bsc_is":         ["Business_IT_Management",
                            "IT_Operations_QA"],
}

# ── Temporary compatibility layer ─────────────────────────────
# Maps (universityName, degreeName) tuples to deterministic
# doc IDs for programs that do not have a known doc ID at
# lookup time (e.g. admin-created programs with auto-generated IDs).
#
# This dict can be removed once:
#   1. All active degree_programs documents use deterministic
#      document IDs set by seed_data.py or the Admin Panel, AND
#   2. _get_clusters() in education_path.py is updated to use
#      doc ID lookup only.
# ──────────────────────────────────────────────────────────────

PROGRAM_CLUSTER_FALLBACK: dict[tuple[str, str], str] = {
    ("University of Moratuwa",
     "BSc (Hons) in Computer Science and Engineering"): "uom_bsc_cse",

    ("University of Moratuwa",
     "BSc (Hons) in Information Technology"):           "uom_bsc_it",

    ("Sri Lanka Institute of Information Technology (SLIIT)",
     "BSc (Hons) in Information Technology"):           "sliit_bsc_it",

    ("Sri Lanka Institute of Information Technology (SLIIT)",
     "BSc (Hons) in Software Engineering"):             "sliit_bsc_se",

    ("NSBM Green University",
     "BSc (Hons) in Computing"):                        "nsbm_bsc_computing",

    ("APIIT Sri Lanka",
     "BSc (Hons) in Computing"):                        "apiit_bsc_computing",

    ("University of Colombo School of Computing (UCSC)",
     "BSc (Hons) in Computer Science"):                 "ucsc_bsc_cs",

    ("University of Colombo School of Computing (UCSC)",
     "BSc (Hons) in Information Systems"):              "ucsc_bsc_is",
}
