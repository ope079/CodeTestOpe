from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import IntegerField, SubmitField


class Form(FlaskForm):
    file = FileField()
    submit = SubmitField('Add the file')

class Meter_Form(FlaskForm):
    meter_number = IntegerField('Enter meter number')
    submit = SubmitField('Enter the Meter number')

