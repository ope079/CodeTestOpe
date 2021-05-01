from application import app, db
from application.forms import Form
from application.models import Headr, Consu
from flask import render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import pandas as pd
#import sqlite3


@app.route('/', methods=["POST", "GET"])
@app.route('/home', methods=["POST", "GET"])
def home():
    form = Form()

    if form.validate_on_submit():
        filename = secure_filename(form.file.data.filename)
        form.file.data.save('SMRT/' + filename)
        df = pd.read_csv(f'SMRT/{filename}', header=None)

        #conn = sqlite3.connect('testdb1.db')
        head = df.iloc[0, :]
        cons = df.iloc[1:, :]

        if "HEADR" in head[0] and "TRAIL" in cons.iloc[-1, 0]:

            head = head.tolist()
            new_headr = Headr(file_type=head[1], company_id=head[2], fileCreation_date=head[3],
                              fileCreation_time=head[4],
                              file_number=head[5])
            db.session.add(new_headr)

            sep = '.'
            file_number = filename.split(sep, 1)[0]

            for j, i in cons.iterrows():
                new_consu = Consu(meter_number=i[1], measurement_date=i[2], measurement_time = i[3],
                                  consumption=i[4], file_number=file_number)
                db.session.add(new_consu)
                db.session.commit()
            return redirect(url_for('home'))

    return render_template('index.html', form=form)


@app.route('/metrics', methods=["POST", "GET"])
def getMetrics():
    form = Form()
    count_meters = Consu.query.group_by(Consu.meter_number).distinct().count()
    count_files = Headr.query.order_by(Headr.file_number).distinct().count()
    last_file = Headr.query.order_by(Headr.fileReception_time.desc()).first().file_number
    return render_template("metrics.html", count_meters=count_meters, count_files=count_files, last_file=last_file)

