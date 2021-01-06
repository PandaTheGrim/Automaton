from flask_wtf import FlaskForm
from wtforms import TextField, validators
from wtforms.validators import DataRequired


class TestPlanCreateForm(FlaskForm):
    name = TextField('Name:', validators=[DataRequired(), validators.Length(min=3, max=180)])
    description = TextField('Description:',
                            validators=[DataRequired(), validators.Length(min=0, max=180)])
