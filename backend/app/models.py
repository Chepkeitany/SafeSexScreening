#!/usr/bin/env python
# -- coding: utf-8 --

import datetime as dt
import uuid

from sqlalchemy.types import Boolean, DateTime, Integer, String

from app import db

from .screening import get_screening_recommendation


class Patient(db.Model):
    __tablename__ = "patients"
    id = db.Column(String(128), primary_key=True)
    age = db.Column(Integer)
    name = db.Column(String(256))
    gender = db.Column(String(128))

    def __repr__(self):
        return f"<User {self.name}>"

    def to_json(self):
        json_patient = {
            "id": self.id,
            "age": self.age,
            "name": self.name,
            "gender": self.gender,
        }

        return json_patient

    @staticmethod
    def from_json(json_patient):
        return Patient(
            id=json_patient["id"],
            age=json_patient["age"],
            name=json_patient["name"],
            gender=json_patient["gender"],
        )


class Recommendation(db.Model):
    __tablename__ = "recommendations"
    id = db.Column(String(128), primary_key=True)
    patient_id = db.Column(String(128), index=True)
    age = db.Column(Integer)
    gender = db.Column(String(128))
    last_screening = db.Column(String(64))
    days_since_last_screening = db.Column(Integer)
    num_sexual_partners = db.Column(Integer)
    is_sexually_active = db.Column(Boolean, default=False)
    is_drug_user = db.Column(Boolean, default=False)
    is_pregnant = db.Column(Boolean, default=False)
    is_sex_worker = db.Column(Boolean, default=False)
    is_condom_user = db.Column(Boolean, default=False)
    has_new_sex_partners = db.Column(Boolean, default=False)
    has_rash = db.Column(Boolean, default=False)
    has_fever = db.Column(Boolean, default=False)
    has_dysuria = db.Column(Boolean, default=False)
    has_pharyngeal_discomfort = db.Column(Boolean, default=False)
    partner_has_std_symptoms = db.Column(Boolean, default=False)
    screening_recommendation = db.Column(String(128), nullable=True)
    create_date = db.Column(DateTime, server_default=db.func.now())

    def to_json(self):
        json_recomm = {
            "id": self.id,
            "patient_id": self.patient_id,
            "age": self.age,
            "gender": self.gender,
            "last_screening": self.last_screening,
            "days_since_last_screening": self.days_since_last_screening,
            "num_sexual_partners": self.num_sexual_partners,
            "is_sexually_active": self.is_sexually_active,
            "is_drug_user": self.is_drug_user,
            "is_pregnant": self.is_pregnant,
            "is_sex_worker": self.is_sex_worker,
            "is_condom_user": self.is_condom_user,
            "has_new_sex_partners": self.has_new_sex_partners,
            "has_rash": self.has_rash,
            "has_fever": self.has_fever,
            "has_dysuria": self.has_dysuria,
            "has_pharyngeal_discomfort": self.has_pharyngeal_discomfort,
            "partner_has_std_symptoms": self.partner_has_std_symptoms,
            "screening_recommendation": self.screening_recommendation,
            "create_date": self.create_date.isoformat(),
        }

        return json_recomm

    @staticmethod
    def day_counter_today(d):
        today = dt.date.today()
        past_date = dt.datetime.strptime(d, "%Y-%m-%d")

        return int((today - past_date.date()).days)

    @staticmethod
    def from_json(recomm_json):
        # calculate days since last screening
        days_since_last_screening = Recommendation.day_counter_today(
            recomm_json["last_screening"]
        )

        # generate initial Recommendation record with required details
        recommendation = Recommendation(
            id=str(uuid.uuid1()),
            patient_id=recomm_json["patient_id"],
            age=recomm_json["age"],
            gender=recomm_json["gender"],
            last_screening=recomm_json["last_screening"],
            days_since_last_screening=days_since_last_screening,
            num_sexual_partners=recomm_json["num_sexual_partners"],
            is_sexually_active=recomm_json["is_sexually_active"],
            is_drug_user=recomm_json["is_drug_user"],
            is_pregnant=recomm_json["is_pregnant"],
            is_sex_worker=recomm_json["is_sex_worker"],
            is_condom_user=recomm_json["is_condom_user"],
            has_new_sex_partners=recomm_json["has_new_sex_partners"],
            has_rash=recomm_json["has_rash"],
            has_fever=recomm_json["has_fever"],
            has_dysuria=recomm_json["has_dysuria"],
            has_pharyngeal_discomfort=recomm_json["has_pharyngeal_discomfort"],
            partner_has_std_symptoms=recomm_json["partner_has_std_symptoms"],
        )

        # generate screening recommendation
        screening = get_screening_recommendation(recommendation)
        recommendation.screening_recommendation = screening

        return recommendation


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(String(128), primary_key=True)
    username = db.Column(String(64), index=True, unique=True)
    email = db.Column(String(128), index=True)
    password = db.Column(String(128))

    def __repr__(self):
        return f"<User {self.username}>"

    def to_json(self):
        json_user = {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "password": self.password,
        }

        return json_user

    @staticmethod
    def from_json(json_user):
        return User(
            id=str(uuid.uuid1()),
            username=json_user["username"],
            email=json_user["email"],
            password=json_user["password"],
        )
