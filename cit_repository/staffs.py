from flask import (
    Blueprint, render_template, url_for, redirect, flash, request
)

from .auth import login_required, admin_only
from .forms import ProjectRegisterForm, StaffRegisterForm
from .models import Department, db, Project, Staff


bp = Blueprint('staffs', __name__, url_prefix='/staff')


@bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('staffs/dashboard.html')


@bp.route('/projects', methods=['GET'])
@login_required
def all_projects():
    projects = [p for p in Project.query.all() if p.visible]
    n = len(projects)
    
    return render_template('staffs/project_list.html', projects=projects, n=n)


@bp.route('/add_project', methods=['GET', 'POST'])
@login_required
def add_project():
    form = ProjectRegisterForm()

    if request.method == 'POST':
        topic = form.topic.data
        department = form.department.data
        body = form.body.data
        year = form.year_of_submission.data
        references = form.references.data
        methodology = form.methodology.data
        student = form.student_name.data
        supervisor = form.supervisor_name.data
        project_number=form.project_number.data

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


@bp.route('/all')
@admin_only
def all_staffs():
    staffs = Staff.query.all()
    n = len(staffs)

    return render_template('staffs/staff_list.html', staffs=staffs, n=n)


@bp.route('/add_staff', methods=['GET', 'POST'])
@admin_only
def add_staff():
    form  = StaffRegisterForm()
    if request.method == 'POST':
        username = form.username.data
        fullname = form.fullname.data
        password = form.password.data
        department = form.department.data
        user_level = form.user_level.data

        if Staff.query.filter_by(username=username).first() is not None:
            flash("Username already exists", 'error')
        else:
            department = Department.query.filter_by(name=department).first()
            staff = Staff(
                    username=username,
                    fullname=fullname,
                    user_level=user_level,
                    department=department
                )
            staff.hash_password(password)

            db.session.add(staff)
            db.session.commit()
            flash("Staff Added successfully", 'success')

            return redirect(url_for('staffs.all_staffs'))
    depts = [(dept.name, dept.name) for dept in Department.query.all()]

    form.department.choices = depts
    return render_template('staffs/add_staff.html', form=form)


@bp.route('/staff/<int:id>')
@admin_only
def view_staff(id):
    staff = Staff.query.filter_by(id=id).first_or_404()

    return render_template('staffs/view_staff.html', staff=staff)