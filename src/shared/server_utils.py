"""
Methods to be used frequently in the server.
"""

__author__ = "Sylivie"
__copyright__ = "Copyright 2023, AUCA Research Gate"

from storage.database_client import DocumentClient
from base_constants import BaseDirectoryConstants
from flask import jsonify, session
from flask_api import status
from werkzeug.datastructures import FileStorage
from shared.md5_hash import MD5Hash
from shared.file_name_generator import FileNameGenerator
from typing import Callable, Any, Dict
import os


class ServerUtils:
    @staticmethod
    def http_response(response_keyword: str = 'message', response_message: str = None,
                      response_status_code: int = status.HTTP_200_OK):
        return jsonify({response_keyword: response_message}), response_status_code

    def login_required(func: Callable):
        """
        Checks if user id is stored in the session.
        """
        def wrapper(self, *args, **kwargs):
            if not session.get('user_id'):
                return ServerUtils.http_response(
                    response_message="Login is required.",
                    response_status_code=status.HTTP_403_FORBIDDEN)

            func_result: Any = func(self, *args, **kwargs)
            return func_result
        return wrapper

    @staticmethod
    def check_enum_has_key(enum: object, key: str = None):
        """
        Checks if an enum class has a given key.
        """
        return any(member for member in enum if member.name == key)

    @staticmethod
    def store_document_file(file: FileStorage = None):
        """
        Stores the document file.
        """
        original_filename: str = file.filename
        extension_component: bool = original_filename.split(".")[1:]
        extension: str = extension_component[0] if extension_component else ""
        file_hash: str = MD5Hash.compute_hash(file=file)

        random_base_name: str = FileNameGenerator.generate_file_name(
            base_string_length=16, extension=extension)

        while DocumentClient.document_base_name_is_taken(file_name=random_base_name + extension):
            random_base_name: str = FileNameGenerator.generate_file_name(
                base_string_length=16, extension=extension)

        granted_path_name: str = os.path.join(BaseDirectoryConstants.DOCUMENTS_DIRECTORY_PATH, random_base_name)
        file.save(granted_path_name)
        result_dict: Dict[str, str] = {
            'document_hash': file_hash,
            'document_original_base_name': original_filename,
            'document_base_name': random_base_name
        }
        return result_dict
