from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import StringField, SubmitField


class Form(FlaskForm):
    file = FileField()
    submit = SubmitField('Add the file')

