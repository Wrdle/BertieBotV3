from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Length, Email
import json
import bot
import extraFunctions

class AutoRole(FlaskForm):
    role = SelectField('Role', )

    submit = SubmitField('Save')