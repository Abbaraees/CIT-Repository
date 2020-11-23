from flask import (
    Blueprint, render_template, url_for, redirect, flash
)

from .auth import login_required, admin_only
from .forms import ProjectRegisterForm
from .models import Department, db, Project


bp = Blueprint('staffs', __name__, url_prefix='/staff')


@bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('staffs/dashboard.html')


@bp.route('/projects', methods=['GET'])
@login_required
def all_projects():
    projects = [p for p in Project.query.all() if p.visible]
    
    return render_template('staffs/project_list.html', projects=projects)


@bp.route('/add_project', methods=['GET', 'POST'])
@login_required
def add_project():
    form = ProjectRegisterForm()

    print(form.topic.data)
    print(form.department.data)
    print(form.body.data)
    print(form.year.data)
    print(form.references.data)
    print(form.methodology.data)
    print(form.student_name.data)
    print(form.supervisor_name.data)
    print(project_number.data)



    if form.validate_on_submit():
        print("Valid")
        topic = form.topic.data
        department = form.department.data
        body = form.body.data
        year = form.year.data
        references = form.references.data
        methodology = form.methodology.data
        student = form.student_name.data
        supervisor = form.supervisor_name.data
        project_number=project_number.data

        # Check if the project exists
        if Project.query.filter_by(topic=topic, year_of_submission=year).first():
            error = "Project already exists"
        else:
            department = Department.query.filter_by(name=department).first()
            project = Project(
                topic=topic,
                department=department,
                body=body,
                year_of_submission=year,
                student_name=student,
                supervisor_name=supervisor,
                references=references,
                methodology=methodology,
                project_number=project_number
            )
            db.session.add(project)
            db.session.commit()
            flash("Project added successfully", "success")

            return redirect(url_for('staffs.all_projects'))

        flash(error, "warning")

    print("Invalid")
    depts = [(dept.name, dept.name) for dept in Department.query.all()]

    form.department.choices = depts

    return render_template('staffs/add_project.html', form=form)