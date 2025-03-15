from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app.forms.auth import LoginForm
from app.forms.staff import ChangePasswordForm
from app.models.staff import Staff
from app import db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        staff = Staff.query.filter_by(username=form.username.data).first()
        if staff is None or not staff.check_password(form.password.data) or not staff.is_active:
            flash('用户名或密码错误', 'danger')
            return render_template('auth/login.html', form=form)
        
        login_user(staff, remember=form.remember_me.data)
        staff.update_last_login()
        
        next_page = request.args.get('next')
        if not next_page or not next_page.startswith('/'):
            next_page = url_for('dashboard.index')
        
        return redirect(next_page)
    
    return render_template('auth/login.html', form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('您已成功登出', 'success')
    return redirect(url_for('auth.login'))

@auth_bp.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if not current_user.check_password(form.old_password.data):
            flash('原密码错误', 'danger')
            return render_template('auth/change_password.html', form=form)
        
        current_user.set_password(form.password.data)
        db.session.commit()
        flash('密码已成功修改', 'success')
        return redirect(url_for('dashboard.index'))
    
    return render_template('auth/change_password.html', form=form)