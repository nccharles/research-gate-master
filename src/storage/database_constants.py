"""
Contains database constants used project wide.
"""
__author__ = "Sylivie"
__copyright__ = "Copyright 2023, AUCA Research Gate"


class DatabaseConstants:
    class GeneralConstants:
        """General constants used by the database."""
        PASSWORD_HASHING_METHOD = 'sha256'
        ID_MAX_LENGTH = 64
        UUID_MAX_LENGTH = 128
        NAME_MAX_LENGTH = 32
        EMAIL_MAX_LENGTH = 32
        PASSWORD_HASH_MAX_LENGTH = 128
        PHONE_NUMBER_MAX_LENGTH = 16
        FILE_NAME_MAX_LENGTH = 32
        DOCUMENT_HASH = 128
