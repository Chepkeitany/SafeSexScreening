#!/usr/bin/env python
# -- coding: utf-8 --

import unittest

from flask import json

from app import db
from app.models import User
from test_base import BaseTestCase


class UsersTestCase(BaseTestCase):
    def add_user(self):
        u = User(
            id="patient-id",
            username="fciner",
            email="gigahead_5@hotmail.com",
            password="crankyeuler",
        )
        db.session.add(u)
        db.session.commit()

    def test_create_user(self):
        json_user = json.dumps(
            {
                "username": "fciner",
                "email": "gigahead_5@hotmail.com",
                "password": "crankyeuler",
            }
        )

        resp = self.client.post(
            "api/v1/users", data=json_user, content_type="application/json"
        )

        self.assertEqual(resp.status_code, 200)

        user = resp.json["user"]

        self.assertEqual(user["username"], "fciner")
        self.assertEqual(user["email"], "gigahead_5@hotmail.com")
        self.assertEqual(user["password"], "crankyeuler")

    def test_get_user(self):
        self.add_user()

        username = "fciner"
        resp = self.client.get(f"api/v1/users/{username}")

        self.assertEqual(resp.status_code, 200)

        body = resp.json

        self.assertEqual(body["username"], username)

    def test_get_invalid_user(self):
        username = "bobby_tables"

        resp = self.client.get(f"api/v1/users/{username}")
        self.assertEqual(resp.status_code, 404)

        body = resp.json

        self.assertEqual(body["error"], "User bobby_tables does not exist.")

    def test_delete_user(self):
        self.add_user()

        username = "fciner"
        resp = self.client.delete(f"api/v1/users/{username}")

        self.assertEqual(resp.status_code, 200)

        body = resp.json

        self.assertEqual(body["status"], "User fciner successfully deleted.")


if __name__ == "__main__":
    unittest.main()
