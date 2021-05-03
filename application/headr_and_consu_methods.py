from sqlalchemy.orm import session
from sqlalchemy import and_
from application.models import Headr, Consu
from application import db
from sqlalchemy import func

def validate_meter_number_and_date_time(meter_number, measurement_date_time):
    if db.session.query(Consu.meter_number==meter_number, Consu.measurement_date_time==measurement_date_time, func.count()).group_by(Consu.meter_number, Consu.measurement_date_time).having(func.count() > 1).count() > 1:
        subq = db.session.query(Consu.measurement_date_time==measurement_date_time, Consu.meter_number==meter_number).group_by(Consu.measurement_date_time, Consu.meter_number).having(func.count() > 1).order_by(Consu.measurement_date_time.desc()).limit(1).subquery()
        Consu.query.filter(Consu.meter_number==meter_number and Consu.measurement_date_time and Consu.measurement_date_time.notin_(subq)).delete(synchronize_session=False)
