"""
Contains constants used project wide.
"""
__author__ = "Sylivie"
__copyright__ = "Copyright 2023, AUCA Research Gate"

import os


class BaseDirectoryConstants:
    BASE_DIRECTORY_PATH = os.path.abspath(os.path.dirname(__file__))
    SERVER_DIRECTORY_PATH = os.path.join(BASE_DIRECTORY_PATH, 'server')

    STORAGE_DIRECTORY_PATH = os.path.join(BASE_DIRECTORY_PATH, 'storage')
    DB_STORAGE_PATH = os.path.join(STORAGE_DIRECTORY_PATH, 'db')

    DOCUMENTS_DIRECTORY_PATH = os.path.join(BASE_DIRECTORY_PATH, 'documents')
    DOCUMENTS_TEMP_PATH = os.path.join(BASE_DIRECTORY_PATH, 'documents', 'temp')
