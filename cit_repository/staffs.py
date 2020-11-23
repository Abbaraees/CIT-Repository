from flask import (
    Blueprint, render_template, url_for, redirect, flash
)

from .auth import login_required, admin_only
from .forms import DepartmentRegisterForm
from .models import Department, db, Project


bp = Blueprint('staffs', __name__, url_prefix='/staff')


@bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('staffs/dashboard.html')


@bp.route('/projects', methods=['GET'])
@login_required
@admin_only
def all_projects():
    projects = [p for p in Project.query.all() if p.visible]
    
    return render_template('staffs/project_list.html', projects=projects)
    
