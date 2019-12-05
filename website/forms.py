from flask_wtf import FlaskForm
from wtforms.fields import TextAreaField,SubmitField, StringField, PasswordField, IntegerField, SelectField
from wtforms.validators import InputRequired, Length, Email, EqualTo, Regexp
from flask_wtf.file import FileField, FileRequired, FileAllowed


#creates the login information
class LoginForm(FlaskForm):
    username = StringField("User Name", validators=[InputRequired('Enter user name')])
    password = PasswordField("Password", validators=[InputRequired('Enter user password')])
    submit = SubmitField("Login")