#!/usr/bin/env python
# -- coding: utf-8 --

from flask import jsonify, request
from flask_cors import cross_origin
from sqlalchemy import exc

from . import api
from .. import db
from ..models import Patient, Recommendation, User
from .fhir import get_patient_details


@api.route("/health", methods=["GET"])
@cross_origin()
def health():
    return jsonify(status="Application is healthy.")


@api.route("/users", methods=["POST"])
@cross_origin()
def add_users():
    # create User record
    content = request.json
    user = User.from_json(content)

    # add user to database, or return error if user already exists
    db.session.add(user)

    try:
        db.session.commit()
    except exc.IntegrityError as e:
        db.session.rollback()
        err_msg = e.args[0]

        if "UNIQUE constraint failed: users.username" in err_msg:
            resp = jsonify(error=f"Duplicate user: {content['username']}")
            resp.status_code = 409

            return resp

    return jsonify(
        status="User record created successfully.", user=user.to_json()
    )


@api.route("/users/<string:username>", methods=["DELETE"])
@cross_origin()
def delete_users(username):
    # if user does not exist, return "does not exist"
    user = User.query.filter(User.username == username).first()

    if user is None:
        resp = jsonify(status=f"User {username} does not exist.")
        resp.status_code = 404

        return resp

    # delete user from database
    User.query.filter(User.username == username).delete()
    db.session.commit()

    return jsonify(status=f"User {username} successfully deleted.")


@api.route("/users", defaults={"username": None}, methods=["GET"])
@api.route("/users/<string:username>")
@cross_origin()
def get_users(username):
    # filter by username
    if username is not None:
        try:
            user = User.query.filter(User.username == username).first()

            return jsonify(User.to_json(user))
        except AttributeError:
            resp = jsonify(error=f"User {username} does not exist.")
            resp.status_code = 404

            return resp

    # get all users
    users = User.query.all()

    return jsonify([User.to_json(user) for user in users])


@api.route("/patients/<string:patient_id>", methods=["POST"])
@cross_origin()
def add_patients(patient_id):
    # get patient information using FHIR API
    patient_json = None

    try:
        patient_json = get_patient_details(patient_id)
    except Exception as e:
        resp = jsonify(error=f"Error retrieving patient details: {e}")
        resp.status_code = 404

        return resp

    # create Patient record
    patient = Patient.from_json(patient_json)

    # add patient to database, or return error if patient already exists
    db.session.add(patient)

    try:
        db.session.commit()
    except exc.IntegrityError as e:
        db.session.rollback()
        err_msg = e.args[0]

        if "UNIQUE constraint failed: patients.id" in err_msg:
            resp = jsonify(error=f"Duplicate patient ID: {patient.id}")
            resp.status_code = 409

            return resp

    return jsonify(
        status="Patient record created successfully.",
        patient=patient.to_json(),
    )


@api.route("/patients/<string:patient_id>", methods=["DELETE"])
@cross_origin()
def delete_patients(patient_id):
    # if user does not exist, return "does not exist"
    patient = Patient.query.filter(Patient.id == patient_id).first()

    if patient is None:
        resp = jsonify(status=f"Patient {patient_id} does not exist.")
        resp.status_code = 404

        return resp

    # delete user from database
    Patient.query.filter(Patient.id == patient_id).delete()
    db.session.commit()

    return jsonify(status=f"Patient {patient_id} successfully deleted.")


@api.route("/patients", defaults={"patient_id": None}, methods=["GET"])
@api.route("/patients/<string:patient_id>")
@cross_origin()
def get_patients(patient_id):
    # filter by username
    if patient_id is not None:
        try:
            patient = Patient.query.filter(Patient.id == patient_id).first()

            return jsonify(Patient.to_json(patient))
        except AttributeError:
            resp = jsonify(error=f"Patient {patient_id} does not exist.")
            resp.status_code = 404

            return resp

    # get all users
    patients = Patient.query.all()

    return jsonify([Patient.to_json(patient) for patient in patients])


@api.route("/recommendations", methods=["POST"])
@cross_origin()
def add_recommendations():
    # get patient details
    content = request.json
    patient_id = content.get("patient_id")
    patient = Patient.query.filter(Patient.id == patient_id).first()

    if patient is None:
        msg = f"Patient ID {patient_id} not found."

        if patient_id is None:
            msg = "Patient ID is missing."

        resp = jsonify(error=msg)
        resp.status_code = 404

        return resp

    # create Recommendation record
    content["gender"] = patient.gender
    content["age"] = patient.age
    recommendation = Recommendation.from_json(content)

    # add recommendation to database
    db.session.add(recommendation)
    db.session.commit()

    return jsonify(
        status="Recommendation record created successfully.",
        recommendation=recommendation.to_json(),
    )


@api.route("/recommendations", defaults={"patient_id": None}, methods=["GET"])
@api.route("/recommendations/<string:patient_id>")
@cross_origin()
def get_recommendations(patient_id):
    # filter recommendations by patient
    if patient_id is not None:
        # if patient ID does not exist, return 404
        if Patient.query.filter(Patient.id == patient_id).first() is None:
            resp = jsonify(error=f"Patient {patient_id} does not exist.")
            resp.status_code = 404

            return resp

        filtered = Recommendation.query.filter(
            Recommendation.patient_id == patient_id
        )
        recs = [Recommendation.to_json(r) for r in filtered]

        # check if patient has any existing recommendation records
        if len(recs) < 1:
            resp = jsonify(
                status=f"No recommendations for patient ID {patient_id}."
            )

            return resp

        return jsonify(recs)

    # get all recommendations, if no patient ID is specified
    recs = Recommendation.query.all()

    return jsonify([Recommendation.to_json(r) for r in recs])
