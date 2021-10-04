from flask_wtf import FlaskForm
from flask_wtf.recaptcha import validators
from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo

class RegistrationForm(FlaskForm):
    username = StringField(label='Username', validators=[DataRequired(), Length(min=3, max=20)])
    email = StringField(label='Email', validators=[DataRequired(), Email()])
    password = PasswordField(label='Password', validators=[DataRequired(), Length(min=6, max=16)])
    confirm_password = PasswordField(label='Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
    username = StringField(label='Username', validators=[DataRequired(), Length(min=3, max=20)])
    password = PasswordField(label='Password', validators=[DataRequired(), Length(min=6, max=16)])
    submit = SubmitField('Login')