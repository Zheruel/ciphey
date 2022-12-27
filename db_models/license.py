from db_models.shared import db


class License(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.String(255), unique=True, nullable=False)
    token = db.Column(db.String(255), unique=True, nullable=True)
    has_been_used = db.Column(db.Boolean, nullable=False, default=False)
    expiration_date = db.Column(db.Date, nullable=False)

    def __init__(self, value, expiration_date, has_been_used=False):
        self.value = value
        self.expiration_date = expiration_date
        self.has_been_used = has_been_used
