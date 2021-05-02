from sqlalchemy.orm import session
from sqlalchemy import and_
from application.models import Headr, Consu
from application import db
from sqlalchemy import func

def validate_meter_number_and_date_time(meter_number, measurement_date_time):
    if Consu.query.filter(and_(Consu.meter_number==meter_number, Consu.measurement_date_time==measurement_date_time)).count() > 1:
        subq = db.session.query(Consu.measurement_date_time).filter(and_(Consu.meter_number==meter_number,
                                                                         Consu.measurement_date_time==measurement_date_time,
                                                                         )).subquery('measurement_date_time')
        subq2 = db.session.query(Consu).filter(Consu.measurement_date_time.in_.subq).filter(Consu.measurement_date_time < func.max(Consu.measurement_date_time)).subquery()
        Consu.query.filter(Consu.measurement_date_time.in_(subq2)).delete(synchronize_session=False)