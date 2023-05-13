"""
Contains document management endpoints and corresponding methods.
"""

__author__ = "Sylvie"
__copyright__ = "Copyright 2023, AUCA Research Gate"

from storage.database_client import DocumentClient, UserClient
from storage.database_records import Document, User
from shared.server_routes import ServerRoutes
from shared.server_utils import ServerUtils
from shared.md5_hash import MD5Hash
from shared.enum_types import DocumentType, Schools, Faculties
from flask_api import status
from flask import Flask, request,jsonify
from typing import Dict, List


class DocumentManagement:
    def __init__(self, flask_app: Flask = None):
        self.flask_app = flask_app
        self.attach_endpoints()
        self.decode_token = ServerUtils.decode_token

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
        """
        Uploads a new document to the database.
        :return: HTTP response.
        """
        request_data = request.form.to_dict()
        document_file = request.files.get('file')
        document_description: str = request_data.get('document_description')
        document_type: str = request_data.get('document_type')
        document_campus: str = request_data.get('document_campus')
        document_faculty: str = request_data.get('document_faculty')
        document_title: str = request_data.get('document_title')
        if list(filter(lambda x: not(x),
                       [document_file, document_description, document_type, document_campus, document_faculty, document_title])):
            return ServerUtils.http_response(
                response_message='Missing required arguments.',
                response_status_code=status.HTTP_400_BAD_REQUEST)
        if not ServerUtils.check_enum_has_key(DocumentType, document_type):
            return ServerUtils.http_response(
                response_message="Invalid document type name: {0}.".format(document_type),
                response_status_code=status.HTTP_400_BAD_REQUEST)

        if not ServerUtils.check_enum_has_key(Schools, document_campus):
            return ServerUtils.http_response(
                response_message="Invalid school name: {0}.".format(document_campus),
                response_status_code=status.HTTP_400_BAD_REQUEST)

        if not ServerUtils.check_enum_has_key(Faculties, document_faculty):
            return ServerUtils.http_response(
                response_message="Invalid faculty name: {0}.".format(document_faculty),
                response_status_code=status.HTTP_400_BAD_REQUEST)
        # check document hash.
        document_hash: str = MD5Hash.compute_hash(file=document_file)
        if DocumentClient.document_hash_exists(document_hash=document_hash):
            return ServerUtils.http_response(
                response_message="Document Already Exists in the system.",
                response_status_code=status.HTTP_400_BAD_REQUEST)
        else:
            # get document base name.
            all_documents: List[Document] = DocumentClient.retrieve_all_documents()
            # compare document file and document base name.
            parcentage: float =MD5Hash.compare_hash(file=document_file, all_documents=all_documents)
            if parcentage >= 60:
                return ServerUtils.http_response(
                    response_message="Document has similar content {0}%, of document Already Exists in the system.".format(parcentage),
                    response_status_code=status.HTTP_400_BAD_REQUEST)
            elif parcentage==-1:
                return ServerUtils.http_response(
                    response_message="Error in comparing document.",
                    response_status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
            else:
                # Store the file in the file system.
                document_storing_dict: Dict[str, str] = ServerUtils.store_document_file(file=document_file)

                new_document: Document = DocumentClient.create_and_store_new_document_record(
                    document_original_base_name=document_storing_dict['document_original_base_name'],
                    document_base_name=document_storing_dict['document_base_name'],
                    document_hash=document_storing_dict['document_hash'],
                    document_type=document_type,
                    document_campus=document_campus, document_faculty=document_faculty,
                    document_description=document_description,
                    document_uploader_id=self.decode_token()['user_id'],
                    document_title=document_title)

                return jsonify(new_document.to_json_dict())

    @ServerUtils.login_required
    def update_document(self):
        request_data = request.form.to_dict()
        document_id: str = request_data.get('document_id')
        document_title: str = request_data.get('document_title')
        document_description: str = request_data.get('document_description')
        document_type: str = request_data.get('document_type')
        document_campus: str = request_data.get('document_campus')
        document_faculty: str = request_data.get('document_faculty')

        if list(filter(lambda x: not(x),
                       [document_id, document_description, document_type,document_campus, document_faculty, document_title])):
            return ServerUtils.http_response(
                response_message='Missing required arguments.',
                response_status_code=status.HTTP_400_BAD_REQUEST)

        document_record: Document = DocumentClient.retrieve_document_by_document_id(
            document_id=document_id)

        if not self.decode_token()["user_id"] == document_record.document_uploader_id:
            return ServerUtils.http_response(
                response_message='Not allowed to delete this document.',
                response_status_code=status.HTTP_403_FORBIDDEN)

        updated_document_record: Document = DocumentClient.update_document_record(
            document_campus=document_campus, document_faculty=document_faculty,
            document_description=document_description, document_id=document_id,
            document_title=document_title)
        return jsonify(updated_document_record.to_json_dict())

    @ServerUtils.login_required
    def retrieve_all_documents(self):
        all_documents: List[Document] = DocumentClient.retrieve_all_documents()
        return jsonify([document.to_json_dict() for document in all_documents])

    @ServerUtils.login_required
    def retrieve_school_documents(self, school_name):
        if not ServerUtils.check_enum_has_key(Schools, school_name):
            return ServerUtils.http_response(
                response_message="Invalid school name: {0}.".format(school_name),
                response_status_code=status.HTTP_400_BAD_REQUEST)

        school_documents: List[Document] = DocumentClient.retrieve_school_documents(
            document_campus=school_name)
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
