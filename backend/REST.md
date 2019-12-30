# Resources

* Base API URL: <https://apps.hdap.gatech.edu/ss2backend/api/v1>
* FHIR API URL: <https://apps.hdap.gatech.edu/syntheticmass/baseDstu3>

## Health check

### GET /health

Retrieves application status.

Example request:

```sh
curl -X GET -k https://apps.hdap.gatech.edu/ss2backend/api/v1/health
```

Example response:

```json
{
  "status": "Application is healthy."
}
```

## Users

### POST /users

Create a new application user, given a username, email, and password.

* Consumes: `application/json`
* Produces: `application/json`

Example request:

```sh
curl -X POST -H "Content-Type: application/json" -d '{"username": "fciner", "email": "gigahead_5@hotmail.com", "password": "crankyeuler"}' -k https://apps.hdap.gatech.edu/ss2backend/api/v1/users
```

Example response:

```json
{
  "status": "User record created successfully.",
  "user":
  {
    "id": "6ea3bfd8-033e-11ea-9718-0242ac110002",
    "email": "gigahead_5@hotmail.com",
    "password": "crankyeuler",
    "username": "fciner"
  }
}
```

### GET /users/\<username\>

Retrieve a user's details based on the `username` parameter. If this parameter is omitted, a call to this endpoint retrieves a list containing all of the user records in the database.

* Consumes: `application/x-www-form-urlencoded`
* Produces: `application/json`

Example request:

```sh
curl -X GET -k https://apps.hdap.gatech.edu/ss2backend/api/v1/users/fciner
```

Example response:

```json
{
  "email": "gigahead_5@hotmail.com",
  "id": "6ea3bfd8-033e-11ea-9718-0242ac110002",
  "password": "crankyeuler",
  "username": "fciner"
}
```

### DELETE /users/\<username\>

Delete the specified user from the application database instance, given the `username` parameter.

* Consumes: `application/x-www-form-urlencoded`
* Produces: `application/json`

Example request:

```sh
curl -X DELETE -k https://apps.hdap.gatech.edu/ss2backend/api/v1/users/fciner
```

Example response:

```json
{
  "status": "User fciner successfully deleted."
}
```

## Patients

### POST /patients/\<patient_id\>

Creates a patient record using the patient's FHIR ID, which then is used as the unique `patient_id` for the patient in the application's internal database.

* Consumes: `application/x-www-form-urlencoded`
* Produces: `application/json`

Example request:

```sh
curl -X POST -k https://apps.hdap.gatech.edu/ss2backend/api/v1/patients/40f680c8-238b-426b-b1c0-1649c780ce69
```

Example response:

```json
{
  "status": "Patient record created successfully.",
  "patient":
  {
    "id": "40f680c8-238b-426b-b1c0-1649c780ce69",
    "age": 5,
    "name": "Winford Altenwerth",
    "gender": "male"
  }
}
```

### GET /patients/\<patient_id\>

* Consumes: `application/x-www-form-urlencoded`
* Produces: `application/json`

Retrieve a particular patient's details using the `patient_id` parameter, which refers to the patient's FHIR ID. If this parameter is omitted, a call to this endpoint retrieves a list containing all of the patient records in the database.

Example request:

```sh
curl -X GET -k https://apps.hdap.gatech.edu/ss2backend/api/v1/patients/40f680c8-238b-426b-b1c0-1649c780ce69
```

Example response:

```json
{
  "id": "40f680c8-238b-426b-b1c0-1649c780ce69",
  "age": 5,
  "name": "Winford Altenwerth",
  "gender": "male",
}
```

### DELETE /patients/\<patient_id\>

Delete the patient from the application database instance, given the `patient_id` parameter.

* Consumes: `application/x-www-form-urlencoded`
* Produces: `application/json`

Example request:

```sh
curl -X DELETE -k https://apps.hdap.gatech.edu/ss2backend/api/v1/patients/40f680c8-238b-426b-b1c0-1649c780ce69
```

Example response:

```json
{
  "status": "Patient 40f680c8-238b-426b-b1c0-1649c780ce69 successfully deleted."
}
```

## Recommendations

### POST /recommendations

Creates a screening recommendation record for a given patient filtered by `patient_id`.

* Consumes: `application/json`
* Produces: `application/json`

Example request body:

```json
{
  "patient_id": "3123f5a6-e224-4255-b5ba-f7238fb7d0f5",
  "last_screening": "2019-11-01",
  "num_sexual_partners": 2,
  "is_sexually_active": true,
  "is_drug_user": false,
  "is_pregnant": false,
  "is_sex_worker": false,
  "is_condom_user": false,
  "has_new_sex_partners": true,
  "has_rash": true,
  "has_fever": true,
  "has_dysuria": true,
  "has_pharyngeal_discomfort": false,
  "partner_has_std_symptoms": false
}
```

Example request:

```sh
curl -X POST -H "Content-Type: application/json" -d @request.json -k https://apps.hdap.gatech.edu/ss2backend/api/v1/recommendations
```

Example response:

```json
{
  "status": "Recommendation record created successfully.",
  "recommendation":
  {
    "id":"61b878e4-040c-11ea-8f52-0242ac110002",
    "patient_id":"3123f5a6-e224-4255-b5ba-f7238fb7d0f5",
    "age": 26,
    "days_since_last_screening": 9,
    "gender": "female",
    "has_dysuria": true,
    "has_fever": true,
    "has_new_sex_partners": true,
    "has_pharyngeal_discomfort": false,
    "has_rash": true,
    "is_condom_user":false,
    "is_drug_user": false,
    "is_pregnant": false,
    "is_sex_worker": false,
    "is_sexually_active": true,
    "last_screening": "2019-11-01",
    "num_sexual_partners": 2,
    "partner_has_std_symptoms":false,
    "screening_recommendation": "Urgently recommended",
    "create_date": "2019-11-10T22:49:41"
  }
}
```

### GET /recommendations/\<patient_id\>

* Consumes: `application/x-www-form-urlencoded`
* Produces: `application/json`

Retrieve a given patient's screening recommendation records as a list of JSON objects, using the `patient_id` parameter. If this parameter is omitted, a call to this endpoint retrieves a list containing all of the recommendation records in the database.

Example request:

```sh
curl -X GET -k https://apps.hdap.gatech.edu/ss2backend/api/v1/recommendations/3123f5a6-e224-4255-b5ba-f7238fb7d0f
```

Example response:

```json
[
  {
    "id": "18fae0ec-0416-11ea-b0f8-0242ac110002",
    "patient_id": "3123f5a6-e224-4255-b5ba-f7238fb7d0f5",
    "age": 26,
    "days_since_last_screening": 9,
    "gender": "female",
    "has_dysuria": true,
    "has_fever": true,
    "has_new_sex_partners": true,
    "has_pharyngeal_discomfort": false,
    "has_rash": true,
    "is_condom_user": false,
    "is_drug_user": false,
    "is_pregnant": false,
    "is_sex_worker": false,
    "is_sexually_active": true,
    "last_screening": "2019-11-01",
    "num_sexual_partners": 2,
    "partner_has_std_symptoms": false,
    "screening_recommendation": "Urgently recommended",
    "create_date": "2019-11-10T23:59:14"
  }
]
```
