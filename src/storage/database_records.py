"""
Contains database model instances used project wide.
"""
__author__ = "Sylvie"
__copyright__ = "Copyright 2023, AUCA Research Gate"

from storage.database_provider import db_provider
from storage.database_constants import DatabaseConstants
from shared.enum_types import DocumentType, Colleges, Schools, Faculties
import datetime
import uuid
from flask_sqlalchemy import SQLAlchemy

db: SQLAlchemy = db_provider.db


class User(db.Model):
    """
    Represents user record.
    """
    user_id = db.Column(db.BigInteger().with_variant(db.Integer, "sqlite"),
                        primary_key=True)
    user_uuid = db.Column(db.String(DatabaseConstants.GeneralConstants.UUID_MAX_LENGTH),
                          unique=True,
                          index=True)
    user_first_name = db.Column(db.String(DatabaseConstants.GeneralConstants.NAME_MAX_LENGTH), nullable=False)
    user_middle_name = db.Column(db.String(DatabaseConstants.GeneralConstants.NAME_MAX_LENGTH), nullable=False)
    user_last_name = db.Column(db.String(DatabaseConstants.GeneralConstants.NAME_MAX_LENGTH), nullable=False)
    user_email = db.Column(db.String(DatabaseConstants.GeneralConstants.EMAIL_MAX_LENGTH), nullable=False)
    user_password_hash = db.Column(db.String(DatabaseConstants.GeneralConstants.PASSWORD_HASH_MAX_LENGTH), nullable=False)
    user_phone_number = db.Column(db.String(DatabaseConstants.GeneralConstants.PHONE_NUMBER_MAX_LENGTH), nullable=False)
    user_creation_timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow, nullable=False)

    documents = db.relationship(
        'Document', cascade='all, delete-orphan', backref='document_owner', lazy='joined')

    def __init__(
            self, user_first_name: str = None, user_middle_name: str = None,
            user_last_name: str = None, user_email: str = None, user_password_hash: str = None,
            user_phone_number: str = None):

        self.user_uuid = str(uuid.uuid4())
        self.user_first_name = user_first_name
        self.user_middle_name = user_middle_name
        self.user_last_name = user_last_name
        self.user_email = user_email
        self.user_password_hash = user_password_hash
        self.user_phone_number = user_phone_number

    def __repr__(self):
        return "<User: {0} {1}>".format(self.user_first_name, self.user_email)

    def to_json_dict(self):
        return {
            "user_id": self.user_id,
            "user_uuid": self.user_uuid,
            "user_first_name": self.user_first_name,
            "user_middle_name": self.user_middle_name,
            "user_last_name": self.user_last_name,
            "user_email": self.user_email,
            "user_phone_number": self.user_phone_number,
            "user_creation_timestamp": self.user_creation_timestamp
        }


class Document(db.Model):
    """
    Represents Document record.
    """
    document_id = db.Column(db.BigInteger().with_variant(db.Integer, "sqlite"),
                            primary_key=True)
    document_uuid = db.Column(db.String(DatabaseConstants.GeneralConstants.UUID_MAX_LENGTH),
                              unique=True,
                              index=True)
    document_original_base_name = db.Column(
        db.String(DatabaseConstants.GeneralConstants.FILE_NAME_MAX_LENGTH), nullable=True)
    document_base_name = db.Column(
        db.String(DatabaseConstants.GeneralConstants.FILE_NAME_MAX_LENGTH), nullable=False, unique=True)

    document_hash = db.Column(db.String(DatabaseConstants.GeneralConstants.DOCUMENT_HASH), nullable=False, unique=True)
    document_title = db.Column(db.Text(), nullable=False)
    document_type = db.Column(db.Enum(DocumentType), nullable=False, default=DocumentType.UNKNOWN)
    document_college = db.Column(db.Enum(Colleges), nullable=False, default=Colleges.UNKNOWN)
    document_school = db.Column(db.Enum(Schools), nullable=False, default=Schools.UNKNOWN)
    document_faculty = db.Column(db.Enum(Faculties), nullable=False, default=Faculties.UNKNOWN)
    document_description = db.Column(db.Text(), nullable=False)

    document_uploader_id = db.Column(
        db.BigInteger().with_variant(db.Integer, "sqlite"),
        db.ForeignKey('user.user_id', onupdate='CASCADE', ondelete='RESTRICT'), nullable=False)
    document_uploader = db.relationship('User', uselist=False, lazy='joined')
    document_creation_timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow, nullable=False)

    def __init__(
            self, document_original_base_name: str = None, document_base_name: str = None, document_hash: str = None,
            document_type: DocumentType = None, document_college: Colleges = None, document_school: Schools = None,
            document_faculty: Faculties = None, document_description: str = None, document_uploader_id: int = None,
            document_title: str = None):

        self.document_uuid = str(uuid.uuid4())
        self.document_original_base_name = document_original_base_name
        self.document_base_name = document_base_name
        self.document_hash = document_hash
        self.document_title = document_title
        self.document_type = document_type
        self.document_college = document_college
        self.document_school = document_school
        self.document_faculty = document_faculty
        self.document_description = document_description
        self.document_uploader_id = document_uploader_id

    def __repr__(self):
        return "<Document: ID: {0} Type: {1}>".format(self.document_id, self.document_type.name)

    def to_json_dict(self):
        return {
            "document_id": self.document_id,
            "document_uuid": self.document_uuid,
            "document_original_base_name": self.document_original_base_name,
            "document_base_name": self.document_base_name,
            "document_hash": self.document_hash,
            "document_title": self.document_title,
            "document_type": self.document_type.name,
            "document_college": self.document_college.name,
            "document_school": self.document_school.name,
            "document_faculty": self.document_faculty.name,
            "document_description": self.document_description,
            "document_uploader": self.document_uploader.to_json_dict(),
            "document_creation_timestamp": self.document_creation_timestamp
        }
