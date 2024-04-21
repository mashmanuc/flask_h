from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length



class NameForm(FlaskForm):

    name = StringField("Введіть прізвище та ім'я", validators=[DataRequired(), Length(min=1, max=255)])
    submit=SubmitField('Надіслати')
