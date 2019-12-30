#!/usr/bin/env python
# -- coding: utf-8 --

from flask import Flask
from config import config
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from app import models


def create_app(config_name):
    #  create app
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    # initialize database
    db.init_app(app)

    # register REST API endpoints
    from .api import api as api_blueprint

    app.register_blueprint(api_blueprint, url_prefix="/api/v1")

    return app
