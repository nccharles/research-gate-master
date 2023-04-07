"""
Contains user management endpoints and corresponding methods.
"""

__author__ = "Sylvie"
__copyright__ = "Copyright 2023, AUCA Research Gate"

from storage.database_client import UserClient
from storage.database_records import User
from storage.database_constants import DatabaseConstants
from shared.server_routes import ServerRoutes
from shared.server_utils import ServerUtils
from werkzeug.security import generate_password_hash
from flask_api import status
from flask import request, jsonify, session, Flask
from typing import Dict


class UserManagement:
    def __init__(self, flask_app: Flask = None):
        self.flask_app = flask_app
        self.attach_endpoints()

    def attach_endpoints(self):
        self.flask_app.add_url_rule(
            ServerRoutes.UserManagementRoutes.CREATE_USER_RECORD,
            endpoint="create_user_record",
            view_func=self.create_user_record,
            methods=['POST'])

        self.flask_app.add_url_rule(
            ServerRoutes.UserManagementRoutes.USER_LOGIN,
            endpoint="user_login",
            view_func=self.user_login,
            methods=['POST'])

        self.flask_app.add_url_rule(
            ServerRoutes.UserManagementRoutes.USER_LOGOUT,
            endpoint="user_logout",
            view_func=self.user_logout,
            methods=['DELETE'])

    def create_user_record(self):
        request_data: Dict[str, str] = request.get_json()
        user_first_name: str = request_data.get('user_first_name')
        user_middle_name: str = request_data.get('user_middle_name')
        user_last_name: str = request_data.get('user_last_name')
        user_email: str = request_data.get('user_email')
        user_password: str = request_data.get('user_password')
        user_phone_number: str = request_data.get('user_phone_number')

        if list(filter(lambda x: not(x),
                       [user_first_name, user_last_name, user_email,
                        user_password, user_phone_number])):
            return ServerUtils.http_response(
                response_message='Missing required arguments.',
                response_status_code=status.HTTP_400_BAD_REQUEST)

        user_email_exists: bool = UserClient.user_email_exists(user_email=user_email)
        if user_email_exists:
            return ServerUtils.http_response(
                response_message='Email {} already exists.'.format(user_email),
                response_status_code=status.HTTP_400_BAD_REQUEST)

        # Generate password hash.
        user_password_hash: str = generate_password_hash(
            password=user_password, method=DatabaseConstants.GeneralConstants.PASSWORD_HASHING_METHOD)

        new_user_record: User = UserClient.create_and_store_new_user_record(
            user_first_name=user_first_name, user_middle_name=user_middle_name, user_last_name=user_last_name,
            user_email=user_email, user_password_hash=user_password_hash, user_phone_number=user_phone_number)
        token: str = ServerUtils.generate_token(user_id=new_user_record.user_id)
        # merge user record and token
        obj = {**new_user_record.to_json_dict(), **{'user_token': token}}
        return jsonify(obj) 

    def user_login(self):
        request_data: Dict[str, str] = request.get_json()
        user_email: str = request_data.get('user_email')
        user_password: str = request_data.get('user_password')
        if list(filter(lambda x: not(x), [user_email, user_password])):
            return ServerUtils.http_response(
                response_message='Missing required arguments.',
                response_status_code=status.HTTP_400_BAD_REQUEST)

        user_email_exists: bool = UserClient.user_email_exists(user_email=user_email)
        if not user_email_exists:
            return ServerUtils.http_response(
                response_message='Email {} does not exist.'.format(user_email))

        user_record: User = UserClient.retrieve_user_given_password_hash(user_email=user_email, user_password=user_password)

        if not user_record:
            return ServerUtils.http_response(
                response_message='Password mismatch.',
                response_status_code=status.HTTP_403_FORBIDDEN)

        token: str = ServerUtils.generate_token(user_id=user_record.user_id)
        # merge user record and token
        obj = {**user_record.to_json_dict(), **{'user_token': token}}
        return jsonify(obj)

    def user_logout(self):
        if 'user_id' in session:
            del session['user_id']
            return ServerUtils.http_response(response_message='Logged out.')
        return ServerUtils.http_response(response_message='There is no logged in user.')
