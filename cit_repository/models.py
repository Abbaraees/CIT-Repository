from datetime import datetime

from click import command, echo
from flask.cli import with_appcontext
from flask_sqlalchemy import SQLAlchemy
from passlib.apps import custom_app_context as pwd_context


db = SQLAlchemy()


class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50))
    password_hash = db.Column(db.String(255), nullable=False)

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    def __repr__(self):
        return f"<Admin: '{self.username}'>"


class Staff(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    fullname = db.Column(db.String(100), nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'), nullable=False)
    department = db.relationship('Department', backref=db.backref('staffs', lazy=True)) 
    user_level = db.Column(db.Integer, nullable=False)
    visible = db.Column(db.Boolean, default=True)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime)

    def __repr__(self):
        return f"<Staff: '{self.username}'>"
    

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    def __repr__(self):
        return f"Staff: '{self.username}'"


class Department(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    visible = db.Column(db.Boolean)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime)

    def __repr__(self):
        return f"<Department: '{self.name}'>"


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'),  nullable=True)
    department = db.relationship('Department', backref=db.backref('projects', lazy=True))
    project_number = db.Column(db.String(20), nullable=False)
    year_of_submission = db.Column(db.Integer)
    student_name = db.Column(db.String(100), nullable=False)
    supervisor_name = db.Column(db.String(100), nullable=False)
    topic = db.Column(db.String(255), nullable=False)
    body = db.Column(db.String(255), nullable=False)
    methodology = db.Column(db.String(255))
    references = db.Column(db.String)
    visible = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime)

    def __repr__(self):
        return f"<Project: '{self.topic}'>"


@command('init-db')
@with_appcontext
def init_db():
    db.create_all()
    admin = Admin(username='admin', email='admin@example.com')
    admin.hash_password('adminpass')
    db.session.add(admin)
    db.session.commit()

    echo('Database is initialized')


def init_app(app):
    app.cli.add_command(init_db)
    db.init_app(app)

