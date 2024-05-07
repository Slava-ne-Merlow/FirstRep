from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, EmailField
from wtforms.validators import DataRequired


class ForwarderForm(FlaskForm):

    name = StringField('Имя представителя', validators=[DataRequired()])
    email = EmailField('Электронная почта', validators=[DataRequired()])
    company = StringField('Компания', validators=[DataRequired()])
    submit = SubmitField('Применить')
