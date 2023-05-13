__author__ = "Sylvie"
__copyright__ = "Copyright 2023, AUCA Research Gate"

from server.app import create_app
from server.user_management.user_management import UserManagement
from server.document_management.document_management import DocumentManagement
from server.file_server.file_server import FileServer
from flask import Flask

class ResearchGateServer:
    def __init__(self, port: int = None):
        self.flask_app: Flask = create_app()
        self.port: int = port
        self.intiate_servers()
        
    def intiate_servers(self):
        UserManagement(flask_app=self.flask_app)
        DocumentManagement(flask_app=self.flask_app)

    def start(self, debug: bool = False):
        self.flask_app.run(host="0.0.0.0", debug=debug, port=self.port)
