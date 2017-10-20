from flask_wtf import Form
from wtforms import (
    StringField,
    TextAreaField,
)
from wtforms.validators import DataRequired

class UserLoginForm(Form):
    username = StringField(
        'Username',
        [],
        description="Username"
    )
    content = StringField(
        'Password',
        [],
        description="Password",
    )