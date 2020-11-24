from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Email, Length


class LoginForm(FlaskForm):
    username = StringField('username', validators=[DataRequired(), Length(min=5, max=30)])
    password = StringField('password', validators=[DataRequired()])
    is_admin = BooleanField('admin')



class ProjectRegisterForm(FlaskForm):
    department = SelectField(validators=[DataRequired()])
    project_number = StringField('Project Number', validators=[DataRequired()])
    topic = StringField('Topic', validators=[DataRequired()])
    student_name = StringField('Student Name', validators=[DataRequired()])
    supervisor_name = StringField('Supervisor Name', validators=[DataRequired()])
    year_of_submission = StringField('Year Of Submission', validators=[DataRequired()])
    body = TextAreaField('Body', validators=[DataRequired()])
    references = StringField('References')
    methodology = StringField('Methodology')
    visible = BooleanField('Make Project Visible Online ')


class StaffRegisterForm(FlaskForm):
    fullname = StringField('Full Name', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    password = StringField('Password', validators=[DataRequired()])
    department = SelectField('Department', validators=[DataRequired()])
    user_level = StringField('User Level')
