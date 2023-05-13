"""
Contains file management endpoints and corresponding methods.
"""

__author__ = "Sylvie"
__copyright__ = "Copyright 2023, AUCA Research Gate"

from base_constants import BaseDirectoryConstants
from shared.server_routes import ServerRoutes
from flask import Flask, send_from_directory


class FileServer:
    def __init__(self, flask_app: Flask = None):
        self.flask_app = flask_app
        self.attach_endpoints()

    def attach_endpoints(self):
        self.flask_app.add_url_rule(
            ServerRoutes.FileServerRoutes.UPLOADED_FILES_ROOT + "/<uploaded_file_name>",
            "serve_uploaded_file", self.serve_uploaded_file, methods=["GET"])

    def serve_uploaded_file(self, uploaded_file_name):
        return send_from_directory(BaseDirectoryConstants.DOCUMENTS_DIRECTORY_PATH, uploaded_file_name)
