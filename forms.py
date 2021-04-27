from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import EqualTo, InputRequired, Email 



class signUpForm(FlaskForm):
    fullName = StringField("Full Name",validators=[InputRequired()])
    email = StringField("Email",validators=[InputRequired(),Email()])
    password = PasswordField("Password",validators=[InputRequired(),EqualTo("confirm",message="Passwords must match")])
    confirm = PasswordField("Confirm Password",validators=[InputRequired()])
    submit = SubmitField("Sign Up")


class loginForm(FlaskForm):
    email = StringField("Email",validators=[InputRequired(),Email()])
    password = PasswordField("Password",validators=[InputRequired()])
    submit = SubmitField("Log In")