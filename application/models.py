from application import db
from datetime import datetime


class Headr(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    file_type = db.Column(db.String(10))
    company_id = db.Column(db.String(10))
    fileCreation_date = db.Column(db.String(30))
    fileCreation_time = db.Column(db.String(30))
    file_number = db.Column(db.String(20))
    fileReception_time = db.Column(db.DateTime,  default=datetime.utcnow)



class Consu(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    meter_number = db.Column(db.String(20))
    measurement_date = db.Column(db.String(20))
    measurement_time = db.Column(db.String(10))
    consumption = db.Column(db.Integer)
    file_number = db.Column(db.String(20))

