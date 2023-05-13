from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Enum, Text
from src.shared.enum_types import DocumentType, Schools, Faculties


Base = declarative_base()

class UserModel(Base):
    __tablename__ = 'user'
    user_id = Column(Integer, primary_key=True)
    user_uuid = Column(String(36), unique=True, nullable=False)
    user_email = Column(String(255), unique=True, nullable=False)
    user_password_hash = Column(String(255), nullable=False)
    user_first_name = Column(String(255), nullable=False)
    user_middle_name = Column(String(255), nullable=False)
    user_last_name = Column(String(255), nullable=False)
    user_phone_number = Column(String(255), nullable=False)
    user_creation_timestamp = Column(DateTime, nullable=False)
    documents = relationship('Document', cascade='all, delete-orphan', backref='document_owner', lazy='joined')
class DocumentModel(Base):
    __tablename__ = 'document'
    document_id = Column(Integer, primary_key=True)
    document_uuid = Column(String(36), unique=True, nullable=False)
    document_original_base_name = Column(String(255), nullable=False)
    document_base_name = Column(String(255), nullable=False)
    document_hash = Column(String(255), nullable=False)
    document_type = Column(Enum(DocumentType), nullable=False)
    document_campus = Column(Enum(Schools), nullable=False)
    document_faculty = Column(Enum(Faculties), nullable=False)
    document_description = Column(Text, nullable=False)
    document_uploader_id = Column(Integer, ForeignKey('user.user_id'), nullable=False)
    document_uploader = relationship('User', backref='user_documents')
    document_title = Column(String(255), nullable=False)
    document_creation_timestamp = Column(DateTime, nullable=False)
