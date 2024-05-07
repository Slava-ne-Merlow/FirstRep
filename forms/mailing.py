from flask_wtf import FlaskForm
from sqlalchemy import orm
from wtforms import StringField, TextAreaField, widgets
from wtforms import SubmitField
from wtforms.validators import DataRequired
from wtforms_alchemy import QuerySelectMultipleField


class QuerySelectMultipleFieldWithCheckBoxes(QuerySelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class MailForm(FlaskForm):
    choices = QuerySelectMultipleFieldWithCheckBoxes('Choices')
    mail_theme = StringField('Тема письма', validators=[DataRequired()])

    mail_text = TextAreaField("Текст письма", render_kw={'rows': '10'})
    submit = SubmitField('Отправить')
    user = orm.relationship('User')


