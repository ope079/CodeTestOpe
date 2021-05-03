from application import app, db
from application.forms import Form
from application.models import Headr, Consu
from flask import render_template, redirect, url_for
from werkzeug.utils import secure_filename
import pandas as pd
from datetime import datetime
import os
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
            cons = df.iloc[1:, :]

            if "HEADR" in head[0] and "TRAIL" in cons.iloc[-1, 0]:
                sep = '.'

                head = head.tolist()
                new_headr = Headr(file_type=head[1], company_id=head[2], fileCreation_date_time=datetime.strptime(
                    (head[3].split(sep, 1)[0] + head[4].split(sep, 1)[0]), '%Y%m%d%H%M%S'),
                                  file_number=head[5])
                db.session.add(new_headr)
                db.session.commit()
                file_number = filename.split(sep, 1)[0]

                for j, i in cons.iterrows():
                    i = i.tolist()
                    meter_number = i[1]
                    measurement_date_time = datetime.strptime(str(i[2]+ i[3]),
                                                              '%Y%m%d%H%M')
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

