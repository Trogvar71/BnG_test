from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField
from wtforms import BooleanField, SubmitField
from wtforms.validators import DataRequired


class JobsForm(FlaskForm):
    title = StringField('Заголовок', validators=[DataRequired()])
    type = SelectField('Категория', choices=[('Дорожные проблемы', 'Дорожные проблемы'),
                                             ('Мусор', 'Мусор'),
                                             ('Разные проблемы', 'Разные проблемы')])
    content = TextAreaField("Содержание")
    location = TextAreaField("Геолокация (координаты через запятую без пробела)")
    is_private = BooleanField("Личное")
    submit = SubmitField('Применить')