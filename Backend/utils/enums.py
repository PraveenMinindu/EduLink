# =============================================================
# EduLink — Shared Enums
# Used across admin route models for type safety
# =============================================================

from enum import Enum


class UniversityType(str, Enum):
    state   = "State"
    private = "Private"


class RecordStatus(str, Enum):
    active   = "Active"
    inactive = "Inactive"


class FeeType(str, Enum):
    free = "Free"
    paid = "Paid"


class StudyMode(str, Enum):
    full_time = "Full-time"
    part_time = "Part-time"
    online    = "Online"
    mixed     = "Mixed"


class ApplicationStatus(str, Enum):
    open        = "Open"
    closed      = "Closed"
    coming_soon = "Coming Soon"


class Currency(str, Enum):
    lkr = "LKR"
    usd = "USD"
