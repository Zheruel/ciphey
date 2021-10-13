from flask import Flask
from flask_migrate import Migrate
from db_models.shared import db
from controllers.license_controller import license_controller

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:@localhost/ciphey"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.register_blueprint(license_controller)

db.init_app(app)

migrate = Migrate(app, db)

if __name__ == '__main__':
    app.run(debug=True)
