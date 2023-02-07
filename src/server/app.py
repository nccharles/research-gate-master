"""
Creates the flask app used project wide.
"""
__author__ = "Sylivie"
__copyright__ = "Copyright 2023, AUCA Research Gate"

from flask import Flask
from flask_migrate import Migrate
from src.base_constants import BaseDirectoryConstants
from src.storage.database_provider import db_provider
import os


def create_app():
    # TODO: Configure templates directories and static folder directories.
    app = Flask(__name__, template_folder=None, static_folder=None)

    # TODO: Implement an algorithm to generate app secret key
    app.secret_key = "Inyange"
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + \
        os.path.join(BaseDirectoryConstants.DB_STORAGE_PATH, 'local_db.sqlite')

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db_provider.db.init_app(app)
    Migrate(app, db_provider.db)
    return app
