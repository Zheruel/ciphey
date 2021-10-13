from flask import Flask
from flask_migrate import Migrate
from db_models.shared import db
from controllers.license_controller import license_controller

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.register_blueprint(license_controller)

with app.app_context():
    db.init_app(app)
    db.create_all()

migrate = Migrate(app, db)

if __name__ == '__main__':
    app.run(debug=True)
