from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, PasswordField, FieldList, TextField, TextAreaField, SelectField, validators, FileField
from wtforms.validators import DataRequired, Length, URL, EqualTo, Email

class UserLoginForm(FlaskForm):
    username = StringField('User name:', validators=[DataRequired(), validators.Length(min=3, max=12)])
    password = StringField('Password:', validators=[DataRequired(), validators.Length(min=3, max=12)])

class UserCreateForm(FlaskForm):
    username = StringField('User name:', validators=[DataRequired(), validators.Length(min=3, max=12)])
    password = StringField('Password:', validators=[DataRequired(), validators.Length(min=3, max=12)])
    email = StringField('Email:', validators=[DataRequired(), validators.Length(min=3, max=20), Email()])