from flask import (
    Blueprint, render_template, url_for, redirect
)

from .auth import login_required, admin_only

bp = Blueprint('staffs', __name__, url_prefix='/staff')

@bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('staff/dashboard.html')

@bp.route('/add_department')
@login_required
@admin_only
def add department