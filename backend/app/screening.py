#!/usr/bin/env python
# -- coding: utf-8 --


def female_has_symptoms(patient):
    if patient.has_pharyngeal_discomfort and (
        patient.has_fever or patient.has_rash
    ):
        return True
    if patient.has_dysuria and (patient.has_fever or patient.has_rash):
        return True
    if patient.has_dysuria and patient.has_pharyngeal_discomfort:
        return True

    return False


def male_has_symptoms(patient):
    if patient.has_dysuria and (patient.has_fever or patient.has_rash):
        return True

    return False


def get_screening_recommendation(patient):
    recommendations = {
        1: "Not required",
        2: "Optional",
        3: "Highly recommended",
        4: "Urgently recommended",
    }

    # if patient is not sexually active, screening is not required
    if not patient.is_sexually_active:
        return recommendations[1]
    # if patient is aged under 14
    if patient.age <= 14:
        return recommendations[1]

    if patient.gender == "female":
        # if the patient has chlamydia or gonorrhea symptoms, screening is
        # urgently recommended
        if female_has_symptoms(patient):
            return recommendations[4]

        # if the patient had a sexual relationship with a partner that had
        # STD or STD symptoms, screening is urgently recommended
        if patient.partner_has_std_symptoms:
            return recommendations[4]

        # if the patient is a sex worker or use drugs or may have
        # exchanged sex for drugs
        if patient.is_sex_worker or patient.is_drug_user:
            # if the patient did not do screening for a year, screening is
            # urgently recommended
            if patient.days_since_last_screening > 365:
                return recommendations[4]

            if patient.days_since_last_screening > 90:
                # if the patient did not do screening for 3 months, but had a
                # screening in the last year then screening is recommended
                return recommendations[3]

            else:
                # if the patient had a screening in the last 3 months then
                # screening is optional
                return recommendations[2]

        # if patient age is under 25
        if patient.age <= 25:
            # patient did not have a screening for a year
            if patient.days_since_last_screening > 365:
                # routine annual screening is recommended
                return recommendations[3]

        # if the patient had multiple sex partners in the last period
        if patient.num_sexual_partners >= 2:
            # if the patient had new sex partners in that period
            if patient.has_new_sex_partners:
                # if the patient did not have any screening in the last 3
                # months
                if patient.days_since_last_screening > 90:
                    # if the patient always uses condoms then screening is
                    # optional and not urgent unless the clinitian thinks
                    # otherwise
                    if patient.is_condom_user:
                        return recommendations[2]
                    # if the patient do not use condoms then screening is
                    # highly recommended
                    else:
                        return recommendations[3]
                # if the patient had a screening in the last 3 months,
                # then screening is optional and not urgent unless the
                # clinician thinks otherwise
                else:
                    return recommendations[2]
            else:
                return recommendations[1]

        # if the patient had only 1 sexual partner
        if patient.num_sexual_partners == 1:
            # if the patient had new sexual partner(s) recently
            if patient.has_new_sex_partners:
                # if the patient did not have any screening in the last 3
                # months
                if patient.days_since_last_screening > 90:
                    # if the patient is pregnant then screening is recommended
                    if patient.is_pregnant:
                        return recommendations[3]
                    # if the patient is not pregnant then screening is optional
                    else:
                        return recommendations[2]

        return recommendations[1]

    if patient.gender == "male":
        # if the patient has chlamydia or gonorrhea symptoms, screening is
        # urgently recommended
        if male_has_symptoms(patient):
            return recommendations[4]

        # if the patient had a sexual relationship with a partner that had STD
        # or STD symptoms, screening is urgently recommended
        if patient.partner_has_std_symptoms:
            return recommendations[4]

        # if the patient is a sex worker or uses drugs or may have exchanged
        # sex for drugs
        if patient.is_sex_worker or patient.is_drug_user:
            # if the patient did not do screening for a year, then screening
            # is recommended
            if patient.days_since_last_screening > 365:
                return recommendations[3]
            # if the patient had a screening in the last 3 months, then
            # screening is optional
            else:
                return recommendations[2]

        return recommendations[1]
