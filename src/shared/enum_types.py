"""
Defines different enums used within the application.
"""

from enum import Enum, unique


@unique
class DocumentType(Enum):
    UNKNOWN = "Unknown"
    CAT = "Cat"
    EXAM = "Exam"
    ASSIGNMENT = "Assignment"
    FINAL_YEAR_RESEARCH = "Final Year Research"


@unique
class Schools(Enum):
    UNKNOWN = "Unknown"
    GISHUSHU = "Gishushu"
    MASORO = "Masoro"
    KIBUYE = "Kibuye"



@unique
class Faculties(Enum):
    UNKNOWN = "Unknown"
    IT = "IT"
    BUSINESS = "Business"
    MEDECINE = "Medecine"
