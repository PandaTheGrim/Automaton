from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, PasswordField, FieldList, TextField, TextAreaField, SelectField, validators, FileField
from wtforms.validators import DataRequired, Length, URL, EqualTo, Email

class ReleaseCreateForm(FlaskForm):
    name = TextField('Name:', validators=[DataRequired(), validators.Length(min=3, max=20)])
    description = TextField('Description:', validators=[DataRequired(), validators.Length(min=0, max=180)])
#    xml = TextField('Description:', validators=[DataRequired(), validators.Length(min=0, max=180)])
#    status = TextField('Description:', validators=[DataRequired(), validators.Length(min=0, max=12)])