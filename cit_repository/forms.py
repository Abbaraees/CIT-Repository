from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField
from wtforms.validators import DataRequired, Email, Length


class LoginForm(FlaskForm):
    username = StringField('username', validators=[DataRequired(), Length(min=5, max=30)])
    password = StringField('password', validators=[DataRequired()])
    is_admin = BooleanField('admin')
