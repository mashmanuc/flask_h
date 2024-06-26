from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import DataRequired, EqualTo, Length

# Set your classes here.


class RegisterForm(Form):
    username = StringField(
        'Username', validators=[DataRequired(), Length(min=5, max=25)]
    )
    email = StringField(
        'Email', validators=[DataRequired(), Length(min=6, max=40)]
    )
    password = PasswordField(
        'Password', validators=[DataRequired(), Length(min=6, max=40)]
    )
    confirm = PasswordField(
        'Repeat Password',
        [DataRequired(),
        EqualTo('password', message='Passwords must match')]
    )

class LoginForm(Form):
    username = StringField('Username', [DataRequired()])
    password = PasswordField('Password', [DataRequired()])
    remember = BooleanField('Remember me')

class ForgotForm(Form):
    email = StringField(
        'Email', validators=[DataRequired(), Length(min=6, max=40)]
    )
