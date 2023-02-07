"""
Contains document management endpoints and corresponding methods.
"""

__author__ = "Sylivie"
__copyright__ = "Copyright 2023, AUCA Research Gate"

from src.storage.database_client import DocumentClient, UserClient
from src.storage.database_records import Document, User
from src.shared.server_routes import ServerRoutes
from src.shared.server_utils import ServerUtils
from src.shared.md5_hash import MD5Hash
from src.shared.enum_types import DocumentType, Colleges, Schools, Faculties
from flask_api import status
from flask import Flask, request, session, jsonify
from typing import Dict, List


class DocumentManagement:
    def __init__(self, flask_app: Flask = None):
        self.flask_app = flask_app
        self.attach_endpoints()

    def attach_endpoints(self):
        self.flask_app.add_url_rule(
            ServerRoutes.DocumentManagementRoutes.CREATE_DOCUMENT_RECORD,
            endpoint="upload_new_document",
            view_func=self.upload_new_document,
            methods=['POST'])

        self.flask_app.add_url_rule(
            ServerRoutes.DocumentManagementRoutes.UPDATE_DOCUMENT_RECORD,
            endpoint="update_document",
            view_func=self.update_document,
            methods=['PATCH'])

        self.flask_app.add_url_rule(
            ServerRoutes.DocumentManagementRoutes.RETRIEVE_ALL_DOCUMENTS,
            endpoint="retrieve_all_documents",
            view_func=self.retrieve_all_documents,
            methods=['GET'])

        self.flask_app.add_url_rule(
            ServerRoutes.DocumentManagementRoutes.RETRIEVE_COLLEGE_DOCUMENTS + '/<college_name>',
            endpoint="retrieve_college_documents",
            view_func=self.retrieve_college_documents,
            methods=['GET'])

        self.flask_app.add_url_rule(
            ServerRoutes.DocumentManagementRoutes.RETRIEVE_SCHOOL_DOCUMENTS + '/<school_name>',
            endpoint="retrieve_school_documents",
            view_func=self.retrieve_school_documents,
            methods=['GET'])

        self.flask_app.add_url_rule(
            ServerRoutes.DocumentManagementRoutes.RETRIEVE_FACULTY_DOCUMENTS + '/<faculty_name>',
            endpoint="retrieve_faculty_documents",
            view_func=self.retrieve_faculty_documents,
            methods=['GET'])

        self.flask_app.add_url_rule(
            ServerRoutes.DocumentManagementRoutes.RETRIEVE_DOCUMENTS_BY_DOCUMENT_TYPE + '/<document_type>',
            endpoint="retrieve_documents_by_document_type",
            view_func=self.retrieve_documents_by_document_type,
            methods=['GET'])

        self.flask_app.add_url_rule(
            ServerRoutes.DocumentManagementRoutes.RETRIEVE_UPLOADER_DOCUMENTS + '/<uploader_uuid>',
            endpoint="retrieve_uploader_documents",
            view_func=self.retrieve_uploader_documents,
            methods=['GET'])

    @ServerUtils.login_required
    def upload_new_document(self):
        request_data = request.form.to_dict()
        document_file = request.files.get('file')
        document_description: str = request_data.get('document_description')
        document_type: str = request_data.get('document_type')
        document_college: str = request_data.get('document_college')
        document_school: str = request_data.get('document_school')
        document_faculty: str = request_data.get('document_faculty')
        document_title: str = request_data.get('document_title')

        if list(filter(lambda x: not(x),
                       [document_file, document_description, document_type,
                        document_college, document_school, document_faculty, document_title])):
            return ServerUtils.http_response(
                response_message='Missing required arguments.',
                response_status_code=status.HTTP_400_BAD_REQUEST)

        if not ServerUtils.check_enum_has_key(DocumentType, document_type):
            return ServerUtils.http_response(
                response_message="Invalid document type name: {0}.".format(document_type),
                response_status_code=status.HTTP_400_BAD_REQUEST)

        if not ServerUtils.check_enum_has_key(Colleges, document_college):
            return ServerUtils.http_response(
                response_message="Invalid college name: {0}.".format(document_college),
                response_status_code=status.HTTP_400_BAD_REQUEST)

        if not ServerUtils.check_enum_has_key(Schools, document_school):
            return ServerUtils.http_response(
                response_message="Invalid school name: {0}.".format(document_school),
                response_status_code=status.HTTP_400_BAD_REQUEST)

        if not ServerUtils.check_enum_has_key(Faculties, document_faculty):
            return ServerUtils.http_response(
                response_message="Invalid faculty name: {0}.".format(document_faculty),
                response_status_code=status.HTTP_400_BAD_REQUEST)

        # check document hash.
        document_hash: str = MD5Hash.compute_hash(file=document_file)
        if DocumentClient.document_hash_exists(document_hash=document_hash):
            return ServerUtils.http_response(
                response_message="This file already exists in the system, Add a new one.",
                response_status_code=status.HTTP_400_BAD_REQUEST)

        # Store the file in the file system.
        document_storing_dict: Dict[str, str] = ServerUtils.store_document_file(file=document_file)

        new_document: Document = DocumentClient.create_and_store_new_document_record(
            document_original_base_name=document_storing_dict['document_original_base_name'],
            document_base_name=document_storing_dict['document_base_name'],
            document_hash=document_storing_dict['document_hash'],
            document_type=document_type, document_college=document_college,
            document_school=document_school, document_faculty=document_faculty,
            document_description=document_description,
            document_uploader_id=session['user_id'],
            document_title=document_title)

        return jsonify(new_document.to_json_dict())

    @ServerUtils.login_required
    def update_document(self):
        request_data = request.form.to_dict()
        document_id: str = request_data.get('document_id')
        document_title: str = request_data.get('document_title')
        document_description: str = request_data.get('document_description')
        document_type: str = request_data.get('document_type')
        document_college: str = request_data.get('document_college')
        document_school: str = request_data.get('document_school')
        document_faculty: str = request_data.get('document_faculty')

        if list(filter(lambda x: not(x),
                       [document_id, document_description, document_type,
                        document_college, document_school, document_faculty, document_title])):
            return ServerUtils.http_response(
                response_message='Missing required arguments.',
                response_status_code=status.HTTP_400_BAD_REQUEST)

        document_record: Document = DocumentClient.retrieve_document_by_document_id(
            document_id=document_id)

        if not session['user_id'] == document_record.document_uploader_id:
            return ServerUtils.http_response(
                response_message='Not allowed to delete this document.',
                response_status_code=status.HTTP_403_FORBIDDEN)

        updated_document_record: Document = DocumentClient.update_document_record(
            document_type=document_type, document_college=document_college,
            document_school=document_school, document_faculty=document_faculty,
            document_description=document_description, document_id=document_id,
            document_title=document_title)
        return jsonify(updated_document_record.to_json_dict())

    @ServerUtils.login_required
    def retrieve_all_documents(self):
        all_documents: List[Document] = DocumentClient.retrieve_all_documents()
        return jsonify([document.to_json_dict() for document in all_documents])

    @ServerUtils.login_required
    def retrieve_college_documents(self, college_name):
        if not ServerUtils.check_enum_has_key(Colleges, college_name):
            return ServerUtils.http_response(
                response_message="Invalid college name: {0}.".format(college_name),
                response_status_code=status.HTTP_400_BAD_REQUEST)

        college_documents: List[Document] = DocumentClient.retrieve_college_documents(
            document_college=college_name)
        return jsonify([college_document.to_json_dict() for college_document in college_documents])

    @ServerUtils.login_required
    def retrieve_school_documents(self, school_name):
        if not ServerUtils.check_enum_has_key(Schools, school_name):
            return ServerUtils.http_response(
                response_message="Invalid school name: {0}.".format(school_name),
                response_status_code=status.HTTP_400_BAD_REQUEST)

        school_documents: List[Document] = DocumentClient.retrieve_school_documents(
            document_school=school_name)
        return jsonify([school_document.to_json_dict() for school_document in school_documents])

    @ServerUtils.login_required
    def retrieve_faculty_documents(self, faculty_name):
        if not ServerUtils.check_enum_has_key(Faculties, faculty_name):
            return ServerUtils.http_response(
                response_message="Invalid faculty name: {0}.".format(faculty_name),
                response_status_code=status.HTTP_400_BAD_REQUEST)

        faculty_documents: List[Document] = DocumentClient.retrieve_faculty_documents(
            document_faculty=faculty_name)
        return jsonify([faculty_document.to_json_dict() for faculty_document in faculty_documents])

    @ServerUtils.login_required
    def retrieve_documents_by_document_type(self, document_type):
        if not ServerUtils.check_enum_has_key(DocumentType, document_type):
            return ServerUtils.http_response(
                response_message="Invalid document type name: {0}.".format(document_type),
                response_status_code=status.HTTP_400_BAD_REQUEST)

        documents_of_type: List[Document] = DocumentClient.retrieve_documents_by_document_type(
            document_type=document_type)
        return jsonify([document.to_json_dict() for document in documents_of_type])

    @ServerUtils.login_required
    def retrieve_uploader_documents(self, uploader_uuid: str = None):
        user_record: User = UserClient.retrieve_user_by_uuid(user_uuid=uploader_uuid)
        if not user_record:
            return ServerUtils.http_response(
                response_message='User with uuid {} is not found.'.format(uploader_uuid),
                response_status_code=status.HTTP_404_NOT_FOUND)

        if not user_record.documents:
            return ServerUtils.http_response(
                response_message='User with uuid {} has not uploaded documents yet!'.format(uploader_uuid),
                response_status_code=status.HTTP_404_NOT_FOUND)

        return jsonify([document.to_json_dict() for document in user_record.documents])
