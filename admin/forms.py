from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length



class TestForm(FlaskForm):

    num_quest = StringField('Номер питання', validators=[DataRequired(), Length(min=1, max=255)])
    quest_img = StringField('Зображення', validators=[DataRequired(), Length(min=1, max=255)])
    quest_text = TextAreaField('Текст питання', validators=[DataRequired(), Length(min=1, max=255)])
    ans_data = TextAreaField('Відповідь', validators=[DataRequired(), Length(min=1, max=255)])
    vidpov = StringField('Правильна відповідь', validators=[DataRequired(), Length(min=1, max=255)])
    submit=SubmitField('Зберегти')
