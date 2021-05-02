from sqlalchemy.orm import session
from sqlalchemy import and_
from application.models import Headr, Consu
from application import db
from sqlalchemy import func

def validate_meter_number_and_date_time(meter_number, measurement_date_time):
    if Consu.query.filter(and_(Consu.meter_number==meter_number, Consu.measurement_date_time==measurement_date_time)).distinct().count() > 1:
        subq = db.session.query(Consu.measurement_date_time).filter(and_(Consu.meter_number==meter_number, Consu.measurement_date_time==measurement_date_time)).order_by(Consu.measurement_date_time.desc()).limit(1).subquery()
        Consu.query.filter(Consu.meter_number==meter_number and Consu.measurement_date_time and Consu.measurement_date_time.notin_(subq)).delete(synchronize_session=False)
