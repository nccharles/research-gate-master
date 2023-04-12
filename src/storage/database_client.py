"""
Contains functionality for storing and retrieving records from the database.
"""
__author__ = "Sylvie"
__copyright__ = "Copyright 2023, AUCA Research Gate"

from storage.database_records import User, Document
from storage.database_provider import db_provider
from werkzeug.security import check_password_hash
from sqlalchemy_utils import database_exists, create_database
from shared.enum_types import DocumentType, Colleges, Schools, Faculties
from flask import Flask

db = db_provider.db


class DatabaseCreator:
    @staticmethod
    def create_diagnostics_database_if_not_exists(flask_app: Flask = None):
        """
        Create database at the SQLALCHEMY_DATABASE_URI if database doesn't exist.
        """
        if not database_exists(flask_app.config['SQLALCHEMY_DATABASE_URI']):
            create_database(flask_app.config['SQLALCHEMY_DATABASE_URI'])


class DatabaseStorageClient:
    @staticmethod
    def store_and_refresh_new_record(record: db.Model):
        db.session.add(record)
        db.session.commit()
        db.session.refresh(record)

    @staticmethod
    def update_and_refresh_new_record(record: db.Model):
        """
        Commit changes and refresh updated record.
        """
        db.session.commit()
        db.session.refresh(record)


class UserClient:
    """
    Holds methods to interact with the User database table.
    """
    @staticmethod
    def create_and_store_new_user_record(
            user_first_name: str = None, user_middle_name: str = None,
            user_last_name: str = None, user_email: str = None, user_password_hash: str = None,
            user_phone_number: str = None):

        new_user_record: User = User(
            user_first_name=user_first_name, user_middle_name=user_middle_name, user_last_name=user_last_name,
            user_email=user_email, user_password_hash=user_password_hash, user_phone_number=user_phone_number)

        DatabaseStorageClient.store_and_refresh_new_record(record=new_user_record)
        return new_user_record

    @staticmethod
    def user_email_exists(user_email: str = None):
        return db.session.query(User).filter(User.user_email == user_email).scalar() is not None

    @staticmethod
    def retrieve_user_given_password_hash(user_email: str = None, user_password: str = None):
        user_record: User = db.session.query(User).filter(User.user_email == user_email).one_or_none()
        if user_record and check_password_hash(pwhash=user_record.user_password_hash, password=user_password):
            return user_record
        return None

    @staticmethod
    def retrieve_user_by_uuid(user_uuid: str = None):
        return db.session.query(User).filter(User.user_uuid == user_uuid).one_or_none()


class DocumentClient:
    """
    Holds methods to interact with the Document database table.
    """
    @staticmethod
    def create_and_store_new_document_record(
            document_original_base_name: str = None, document_base_name: str = None, document_hash: str = None,
            document_type: DocumentType = None, document_college: Colleges = None, document_school: Schools = None,
            document_faculty: Faculties = None, document_description: str = None, document_uploader_id: int = None,
            document_title: str = None):

        new_document_record: Document = Document(
            document_original_base_name=document_original_base_name, document_base_name=document_base_name,
            document_hash=document_hash, document_type=document_type, document_college=document_college,
            document_school=document_school, document_faculty=document_faculty, document_description=document_description,
            document_uploader_id=document_uploader_id, document_title=document_title)
        DatabaseStorageClient.store_and_refresh_new_record(record=new_document_record)
        return new_document_record

    @staticmethod
    def document_hash_exists(document_hash: str = None):
        return db.session.query(Document).filter(Document.document_hash == document_hash).scalar() is not None
      
    @staticmethod
    def document_base_name_is_taken(file_name: str = None):
        matching_entry: bool = db.session.query(Document).filter(
            Document.document_base_name == file_name).scalar() is not None
        return matching_entry

    @staticmethod
    def update_document_record(
            document_type: DocumentType = None, document_college: Colleges = None, document_school: Schools = None,
            document_faculty: Faculties = None, document_description: str = None, document_id: int = None,
            document_title: str = None):

        document_record: Document = db.session.query(Document).filter(Document.document_id == document_id).one_or_none()
        if document_record:
            document_record.document_title = document_title
            document_record.document_type = document_type
            document_record.document_college = document_college
            document_record.document_school = document_school
            document_record.document_faculty = document_faculty
            document_record.document_description = document_description

            DatabaseStorageClient.update_and_refresh_new_record(record=document_record)

        return document_record

    @staticmethod
    def retrieve_all_documents():
        return db.session.query(Document).all()

    @staticmethod
    def retrieve_document_by_document_id(document_id: int = None):
        return db.session.query(Document).filter(Document.document_id == document_id).one_or_none()

    @staticmethod
    def retrieve_document_by_document_uuid(document_uuid: int = None):
        return db.session.query(Document).filter(Document.document_uuid == document_uuid).one_or_none()

    @staticmethod
    def retrieve_college_documents(document_college: Colleges = None):
        return db.session.query(Document).filter(
            Document.document_college == document_college).all()

    @staticmethod
    def retrieve_school_documents(document_school: Schools = None):
        return db.session.query(Document).filter(
            Document.document_school == document_school).all()

    @staticmethod
    def retrieve_faculty_documents(document_faculty: Faculties = None):
        return db.session.query(Document).filter(
            Document.document_faculty == document_faculty).all()

    @staticmethod
    def retrieve_documents_by_document_type(document_type: DocumentType = None):
        return db.session.query(Document).filter(
            Document.document_type == document_type).all()
    @staticmethod
    def retrieve_document_by_hash(document_hash: str = None):
        return db.session.query(Document).filter(Document.document_hash == document_hash).one_or_none()
    @staticmethod
    def retrieve_documents_by_uploader_id():
        pass
