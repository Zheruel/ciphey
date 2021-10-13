# Ciphey

Licence generation & validation using a simple Flask web application.

![](example_use_case.jpeg)

## Database setup:

To use a proper database:

First you will need to set the correct database URI in `main.py` under:
`app.config["SQLALCHEMY_DATABASE_URI"]`

Then you will need to apply the migrations on a fresh db by using:

`flask db upgrade`

## Setup

Requirements are listed in `requirements.txt`

This application can easily be modified or extended to fit any personal needs.
All controllers in `/controllers` can be registered in `main` as a blueprint by simply
following the same method used to create the initial `license_controller.py`.

Models are easily added or modified in the `models` folder. They should all use a shared
`db` object from the `shared.py` module. If you modify any models or create new ones you will
need to create and run new migrations.

## Endpoints

A postman collection is included with the project under `/postman`. This gives you an example
for accessing the endpoints and how the requests towards them should be constructed
