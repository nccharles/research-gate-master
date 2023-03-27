"""
Contains all endpoints in their respective classes, Theses are the endpoints
used to interact with the application.
"""

__author__ = "Sylvie"
__copyright__ = "Copyright 2023, AUCA Research Gate"


class ServerRoutes:
    class UserManagementRoutes:
        CREATE_USER_RECORD = "/create/user/record"
        USER_LOGIN = "/user/login"
        USER_LOGOUT = "/user/logout"

    class DocumentManagementRoutes:
        CREATE_DOCUMENT_RECORD = "/create/document/record"
        UPDATE_DOCUMENT_RECORD = "/update/document/record"

        RETRIEVE_ALL_DOCUMENTS = "/retrieve/all/documents"
        RETRIEVE_COLLEGE_DOCUMENTS = "/retrieve/college/documents"
        RETRIEVE_SCHOOL_DOCUMENTS = "/retrieve/school/documents"
        RETRIEVE_FACULTY_DOCUMENTS = "/retrieve/faculty/documents"
        RETRIEVE_DOCUMENTS_BY_DOCUMENT_TYPE = "/retrieve/documents/by/document/type"
        RETRIEVE_UPLOADER_DOCUMENTS = "/retrieve/uploader/documents"

    class FileServerRoutes:
        UPLOADED_FILES_ROOT = "/files/uploaded"
