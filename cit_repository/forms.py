from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SelectField
from wtforms.validators import DataRequired, Email, Length


class LoginForm(FlaskForm):
    username = StringField('username', validators=[DataRequired(), Length(min=5, max=30)])
    password = StringField('password', validators=[DataRequired()])
    is_admin = BooleanField('admin')


class DepartmentRegisterForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    slug = StringField('Slug')
    visible = BooleanField('Visible')


class ProjectRegisterForm(FlaskForm):
    department = SelectField(validators=[DataRequired()])
    project_number = StringField('Project Number', validators=[DataRequired()])
    topic = StringField('Topic', validators=[DataRequired()])
    student_name = StringField('Student Name', validators=[DataRequired()])
    supervisor_name = StringField('Supervisor Name', validators=[DataRequired()])
    year_of_submission = StringField('Year Of Submission', validators=[DataRequired()])
    body = StringField('Body', validators=[DataRequired()])
    references = StringField('References')
    methodology = StringField('Methodology')