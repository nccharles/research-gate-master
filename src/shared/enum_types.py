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
    RESEARCH = 4


@unique
class Colleges(Enum):
    UNKNOWN = 0
    COLLEGE_OF_SCIENCE_AND_TECHNOLOGY = 1
    COLLEGE_OF_BANKING_AND_ECONOMICS = 2


@unique
class Schools(Enum):
    UNKNOWN = 0
    SCHOOL_OF_ICT = 1
    SCHOOL_OF_ENGINEERING = 2


@unique
class Faculties(Enum):
    UNKNOWN = 0
    COMPUTER_SCIENCE = 1
    COMPUTER_ENGINEERING = 2

    CIVIL_ENGINEERING = 3
