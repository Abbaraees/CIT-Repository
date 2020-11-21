import functools

from flask import (
    Blueprint, render_template, redirect, url_for, flash, session, g
)
from werkzeug.exceptions import abort

from .forms import LoginForm
from .models import Admin, Staff

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        is_admin = form.is_admin.data

        if is_admin:
            print("Admin")
            user = Admin.query.filter_by(username=username).first()
            if user is None or not user.verify_password(password):
                flash('Incorrect Username or Password')
            else:
                session.clear()
                session['role'] = 'admin'
                session['user_id'] = user.id

                return redirect(url_for('staffs.dashboard'))
        else:
            print("Staff")
            user = Staff.query.filter_by(username=username).first()
            if user is None or not user.verify_password(password):
                flash('Incorrect Username or Password')
            else:
                session.clear()
                session['role'] = 'staff'
                session['user_id'] = user.id

                return redirect(url_for('staffs.dashboard'))

    return render_template('login.html', form=form)


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@bp.before_app_request
def load_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        if session['role'] == 'admin':
            g.user = Admin.query.filter_by(id=user_id).first()
        else:
            g.user = Staff.query.filter_by(id=user_id).first()


def login_required(func):
    @functools.wraps(func)
    def wrapped_func(*args, **kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return func(*args, **kwargs)

    return wrapped_func

def admin_only(func):
    @functools.wraps(func)
    def wrapped_func(*args, **kwargs):
        if type(g.user) is not Admin:
            return abort(404)
        return func(*args, **kwargs)

    return wrapped_func
