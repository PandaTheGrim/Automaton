from flask_wtf import Form
from wtforms import (
    StringField,
    TextAreaField,
)
from wtforms.validators import DataRequired

class ReleaseCreateForm(Form):
    name = StringField(
        'Name',
        [],
        description="name"
    )
    description = StringField(
        'Description',
        [],
        description="description",
    )