#!/usr/bin/env python
# -- coding: utf-8 --

import unittest

from flask import json

from app import db
from app.models import Patient
from test_base import BaseTestCase


class PatientsTestCase(BaseTestCase):
    def add_patient(self):
        p = Patient(
            id="40f680c8-238b-426b-b1c0-1649c780ce69",
            age=5,
            name="Winford Altenwerth",
            gender="male",
        )
        db.session.add(p)
        db.session.commit()

    def test_create_patient(self):
        patient_id = "40f680c8-238b-426b-b1c0-1649c780ce69"
        resp = self.client.post(f"api/v1/patients/{patient_id}")

        self.assertEqual(resp.status_code, 200)

        data = json.loads(resp.data)
        expected = {
            "status": "Patient record created successfully.",
            "patient": {
                "id": "40f680c8-238b-426b-b1c0-1649c780ce69",
                "age": 5,
                "name": "Winford Altenwerth",
                "gender": "male",
            },
        }

        self.assertEqual(data, expected)

    def test_get_patient(self):
        self.add_patient()

        patient_id = "40f680c8-238b-426b-b1c0-1649c780ce69"
        resp = self.client.get(f"api/v1/patients/{patient_id}")

        self.assertEqual(resp.status_code, 200)

        data = json.loads(resp.data)
        expected = {
            "id": "40f680c8-238b-426b-b1c0-1649c780ce69",
            "age": 5,
            "name": "Winford Altenwerth",
            "gender": "male",
        }

        self.assertEqual(data, expected)

    def test_delete_patient(self):
        self.add_patient()

        patient_id = "40f680c8-238b-426b-b1c0-1649c780ce69"
        resp = self.client.delete(f"api/v1/patients/{patient_id}")
        self.assertEqual(resp.status_code, 200)

        body = resp.json
        self.assertEqual(
            body["status"], f"Patient {patient_id} successfully deleted."
        )

    def test_get_invalid_patient(self):
        patient_id = "missing-id"
        resp = self.client.get(f"api/v1/patients/{patient_id}")
        body = resp.json

        self.assertEqual(resp.status_code, 404)
        self.assertEqual(body["error"], "Patient missing-id does not exist.")


if __name__ == "__main__":
    unittest.main()
