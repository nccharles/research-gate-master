"""
Creates the flask app used project wide.
"""
__author__ = "Sylvie"
__copyright__ = "Copyright 2023, AUCA Research Gate"

from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from base_constants import BaseDirectoryConstants
from storage.database_provider import db_provider
import os


def create_app():
    # TODO: Configure templates directories and static folder directories.
    app = Flask(__name__, template_folder=None, static_folder=None)
    CORS(app, resources={r"/*": {"origins": "http://localhost:4200", "supports_credentials": True}})
    app.config['SECRET_KEY'] = "dhj3_&^%$#jdksj"
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + \
        os.path.join(BaseDirectoryConstants.DB_STORAGE_PATH, 'local_db.sqlite')

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db_provider.db.init_app(app)
    Migrate(app, db_provider.db)
    return app
