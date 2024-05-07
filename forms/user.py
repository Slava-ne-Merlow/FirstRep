from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, EmailField, BooleanField, RadioField
from wtforms.validators import DataRequired
from sqlalchemy import orm


class RegisterForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    name = StringField('Имя пользователя', validators=[DataRequired()])
    about = TextAreaField("Немного о себе")
    user_type = RadioField(
        'label', choices=[('Мэнеджер', 'Мэнеджер'),
                          ('Админ', 'Админ')])
    code = StringField('Для регистрации нового Администратора необходио ввести код доступа', validators=[DataRequired()])
    submit = SubmitField('Войти')
    user = orm.relationship('Order')

class LoginForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Войти')
