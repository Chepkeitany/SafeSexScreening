#!/usr/bin/env python
# -- coding: utf-8 --

import datetime as dt

from flask import session

import fhirclient.models.patient as p
from fhirclient import client

smart_settings = {
    "app_id": "ss2backend",
    "api_base": "https://apps.hdap.gatech.edu/syntheticmass/baseDstu3",
}


def get_patient_details(patient_id):
    smart = _get_smart()
    patient = p.Patient.read(patient_id, smart.server)

    # calculate patient age, if "birthDate" is present
    age = None

    if patient.birthDate is not None:
        dob = dt.datetime.strptime(patient.birthDate.as_json(), "%Y-%m-%d")
        today = dt.date.today()
        age = int((today - dob.date()).days / 365.0)

    # reset SMART handler and return response
    _reset()

    return {
        "id": patient_id,
        "name": smart.human_name(patient.name[0]),
        "gender": patient.gender,
        "age": age,
    }


def _get_smart():
    state = session.get("state")

    if state:
        return client.FHIRClient(state=state, save_func=_save_state)

    return client.FHIRClient(settings=smart_settings, save_func=_save_state)


def _reset():
    if "state" in session:
        smart = _get_smart()
        smart.reset_patient()
        del session["state"]


def _save_state(state):
    session["state"] = state
