"""
Defines different enums used within the application.
"""

from enum import Enum, unique


@unique
class DocumentType(Enum):
    UNKNOWN = 0
    CAT = 1
    EXAM = 2
    ASSIGNMENT = 3
    FINAL_YEAR_RESEARCH = 4


@unique
class Schools(Enum):
    UNKNOWN = 0
    GISHUSHU = 1
    MASORO = 2
    KIBUYE = 3



@unique
class Faculties(Enum):
    UNKNOWN = 0
    IT = 1
    BUSINESS = 2
    MEDECINE = 3
