from sqlalchemy import UniqueConstraint

from application import db
from datetime import datetime


class Headr(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    file_type = db.Column(db.String(10))
    company_id = db.Column(db.String(10))
    fileCreation_date_time = db.Column(db.DateTime)
    file_number = db.Column(db.String(20))
    fileReception_time = db.Column(db.DateTime,  default=datetime.utcnow)
    #__table_args__ = (UniqueConstraint('file_number', name='_file_uc'),)


class Consu(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    meter_number = db.Column(db.String(20))
    measurement_date_time = db.Column(db.DateTime)
    consumption = db.Column(db.Float)
    file_number = db.Column(db.String(20))

