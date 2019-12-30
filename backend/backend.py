#!/usr/bin/env python
# -- coding: utf-8 --

from app import create_app, db
from flask_migrate import Migrate, upgrade

# create Flask server and migration context
app = create_app("production")
migrate = Migrate(app, db)


def init_db():
    # migrate database to the latest version
    upgrade()


@app.cli.command("init_db")
def initdb_command():
    # initialize database
    init_db()

    print("Database initialized.")
