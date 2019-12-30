#!/usr/bin/env python
# -- coding: utf-8 --

import unittest

from app import create_app, db


class BaseTestCase(unittest.TestCase):
    def setUp(self):
        # use "testing" configuration
        self.app = create_app("testing")
        self.app_context = self.app.app_context()
        self.app_context.push()

        # setup database schema and tables
        db.create_all()

        # create test client
        self.client = self.app.test_client()

    def tearDown(self):
        # remove database session and clear schema and tables
        db.session.remove()
        db.drop_all()

        # remove app context
        self.app_context.pop()
