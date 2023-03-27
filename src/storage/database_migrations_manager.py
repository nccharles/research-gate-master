"""
Contains database migration manager.
"""
__author__ = "Sylvie"
__copyright__ = "Copyright 2023, AUCA Research Gate"

from flask_migrate import stamp, migrate, upgrade
from flask import Flask


class MigrationManager():
    @staticmethod
    def upgrade_database(app: Flask):
        # upgrade all database schema
        with app.app_context():
            stamp()
            migrate()
            upgrade()
