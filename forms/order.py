from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms import SubmitField, IntegerField
from wtforms.validators import DataRequired
from sqlalchemy import orm


class OrderForm(FlaskForm):
    invoice_numbers = StringField('Номер поставки', validators=[DataRequired()])

    start_address = StringField('Адресс отгрузки', validators=[DataRequired()])
    end_address = StringField('Адресс доставки', validators=[DataRequired()])
    weight = IntegerField('Вес груза в килограммах', validators=[DataRequired()])
    dimensions = StringField('Обьём в формате: 100x100x100', validators=[DataRequired()])
    quantity = IntegerField('Количество мест', validators=[DataRequired()])
    content = TextAreaField("Коментарии")
    submit = SubmitField('Применить')
    user = orm.relationship('User')