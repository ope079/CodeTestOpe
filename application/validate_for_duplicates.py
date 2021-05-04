from sqlalchemy import and_, select, delete
from sqlalchemy.orm import aliased

from application.models import Headr, Consu
from application import db
from sqlalchemy import func

def validate_meter_number_and_date_time(meter_number, measurement_date_time):
    if db.session.query(func.count(Consu.id)).filter(Consu.measurement_date_time == measurement_date_time and Consu.meter_number ==meter_number)\
                .group_by(Consu.meter_number, Consu.measurement_date_time).having(Consu.measurement_date_time < func.max(Consu.measurement_date_time)).count() > 1:

        db.session.execute(f'DELETE FROM Consu INNER JOIN (Select Consu.measurement_date_time, Consu.meter_number, count(*) '
                           'from Consu WHERE Consu.measurement_date_time = \'{measurement_date_time}\' AND Consu.meter_number = \'{meter_number}\' GROUP BY Consu.meter_number, '
                           'Consu.measurement_date_time HAVING Consu.measurement_date_time < Max(Consu.measurement_date_time)'
                           ') as subqry on subqry.measurement_date_time = \'{measurement_date_time}\' and subqry.meter_number = \'{meter_number}\''
                           )