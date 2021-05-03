from application import app, db
from application.forms import Form
from application.models import Headr, Consu
from flask import render_template, redirect, url_for
from werkzeug.utils import secure_filename
import pandas as pd
from datetime import datetime
import os
import re
from application.validate_for_duplicates import validate_meter_number_and_date_time


@app.route('/', methods=["POST", "GET"])
@app.route('/home', methods=["POST", "GET"])
def home():
    form = Form()

    if form.validate_on_submit():
        filename = secure_filename(form.file.data.filename)
        path = 'SMRT/' + filename

        if not os.path.exists(path):
            form.file.data.save(path)
            df = pd.read_csv(f'SMRT/{filename}', header=None, dtype=str)
            head = df.iloc[0, :]
            cons = df.iloc[1: , :]

            def validate1(date_text, time_text):
                try:
                    datetime.strptime(date_text, '%Y%m%d')
                    datetime.strptime(time_text, '%H%M%S')
                    correctDate = True
                except ValueError:
                    correctDate = False
                return correctDate

            if "HEADR" == head[0] and "TRAIL" == cons.iloc[-1, 0] and "SMRT" == head[1] and type(head[2]) == str and validate1(head[3], head[4]) ==  True and re.match("[A-Z][A-Z][0-9][0-9]+", head[5]):
                sep = '.'

                head = head.tolist()
                new_headr = Headr(file_type=head[1], company_id=head[2], fileCreation_date_time=datetime.strptime(
                    (head[3].split(sep, 1)[0] + head[4].split(sep, 1)[0]), '%Y%m%d%H%M%S'),
                                  file_number=head[5])
                db.session.add(new_headr)
                db.session.commit()
                file_number = filename.split(sep, 1)[0]

                cons = cons.iloc[:-1,:]

                def validate(date_text, time_text):
                    try:
                        datetime.strptime(date_text, '%Y%m%d')
                        datetime.strptime(time_text, '%H%M')
                        correctDate = True
                    except ValueError:
                        correctDate = False
                    return correctDate

                for j, i in cons.iterrows():
                    i = i.tolist()
                    if "CONSU" == i[0] and isinstance(i[1], int) == True and validate(i[2], i[3])==True and isinstance(i[4], float) == True:

                        meter_number = i[1]
                        measurement_date_time = datetime.strptime((str(i[2]).split(sep, 1)[0] + str(i[3]).split(sep, 1)[0]), '%Y%m%d%H%M')
                        consumption = i[4]
                        file_number = file_number

                        new_consu = Consu(meter_number=meter_number, measurement_date_time=measurement_date_time,
                                          consumption=consumption, file_number=file_number)
                        db.session.add(new_consu)
                        validate_meter_number_and_date_time(meter_number, measurement_date_time)
                        db.session.commit()
                    return redirect(url_for('home'))

    return render_template('index.html', form=form)


@app.route('/metrics', methods=["POST", "GET"])
def getMetrics():
    count_meters = Consu.query.group_by(Consu.meter_number).distinct().count()
    count_files = Headr.query.order_by(Headr.file_number).distinct().count()
    last_file = Headr.query.order_by(Headr.fileReception_time.desc()).first().file_number
    return render_template("metrics.html", count_meters=count_meters, count_files=count_files,
                           last_file=last_file)

