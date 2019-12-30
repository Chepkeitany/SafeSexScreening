#!/usr/bin/env python
# -- coding: utf-8 --

import unittest

from flask import json

from app import db
from app.models import Patient
from test_base import BaseTestCase


class RecommendationsTestCase(BaseTestCase):
    def add_patient(self):
        p = Patient(
            id="3123f5a6-e224-4255-b5ba-f7238fb7d0f5",
            age=26,
            name="Mimi Altenwerth",
            gender="female",
        )
        db.session.add(p)
        db.session.commit()

    def request_body(self):
        return json.dumps(
            {
                "patient_id": "3123f5a6-e224-4255-b5ba-f7238fb7d0f5",
                "last_screening": "2019-11-01",
                "num_sexual_partners": 2,
                "is_sexually_active": True,
                "is_drug_user": False,
                "is_pregnant": False,
                "is_sex_worker": False,
                "is_condom_user": False,
                "has_new_sex_partners": True,
                "has_rash": True,
                "has_fever": True,
                "has_dysuria": True,
                "has_pharyngeal_discomfort": False,
                "partner_has_std_symptoms": False,
            }
        )

    def test_create_recommendation(self):
        self.add_patient()

        resp = self.client.post(
            f"api/v1/recommendations",
            data=self.request_body(),
            content_type="application/json",
        )

        self.assertEqual(resp.status_code, 200)

        data = json.loads(resp.data)

        self.assertEqual(
            data["status"], "Recommendation record created successfully."
        )
        self.assertEqual(
            data["recommendation"]["screening_recommendation"],
            "Urgently recommended",
        )

    def test_get_recommendation(self):
        self.add_patient()
        self.client.post(
            f"api/v1/recommendations",
            data=self.request_body(),
            content_type="application/json",
        )

        patient_id = "3123f5a6-e224-4255-b5ba-f7238fb7d0f5"
        resp = self.client.get(f"api/v1/recommendations/{patient_id}")

        self.assertEqual(resp.status_code, 200)

        rec = json.loads(resp.data)[0]

        self.assertEqual(rec["patient_id"], patient_id)
        self.assertEqual(
            rec["screening_recommendation"], "Urgently recommended"
        )

    def test_get_no_recommendations(self):
        self.add_patient()
        patient_id = "3123f5a6-e224-4255-b5ba-f7238fb7d0f5"
        resp = self.client.get(f"api/v1/recommendations/{patient_id}")

        self.assertEqual(resp.status_code, 200)

        data = json.loads(resp.data)
        self.assertEqual(
            data["status"], f"No recommendations for patient ID {patient_id}."
        )


if __name__ == "__main__":
    unittest.main()
