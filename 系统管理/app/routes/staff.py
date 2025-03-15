from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.models.staff import Staff
from app.forms.staff import StaffForm
from datetime import datetime

staff_bp = Blueprint('staff', __name__)

# 员工列表
@staff_bp.route('/')
@login_required
def index():
    if not current_user.is_admin:
        flash('您没有权限访问此页面', 'danger')
        return redirect(url_for('dashboard.index'))
    
    staff = Staff.query.order_by(Staff.name).all()
    return render_template('staff/index.html', staff=staff)

# 添加员工
@staff_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    if not current_user.is_admin:
        flash('您没有权限访问此页面', 'danger')
        return redirect(url_for('dashboard.index'))
    
    form = StaffForm()
    if form.validate_on_submit():
        # 检查用户名是否已存在
        if Staff.query.filter_by(username=form.username.data).first():
            flash('用户名已存在', 'danger')
            return render_template('staff/form.html', form=form, title='添加员工')
        
        staff = Staff(
            username=form.username.data,
            name=form.name.data,
            position=form.position.data,
            id_number=form.id_number.data,
            phone=form.phone.data,
            address=form.address.data,
            commission_rate=form.commission_rate.data,
            is_admin=form.is_admin.data,
            is_active=form.is_active.data
        )
        
        if form.password.data:
            staff.set_password(form.password.data)
        else:
            staff.set_password('123456')  # 默认密码
        
        db.session.add(staff)
        db.session.commit()
        
        flash('员工添加成功', 'success')
        return redirect(url_for('staff.index'))
    
    return render_template('staff/form.html', form=form, title='添加员工')

# 编辑员工
@staff_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    if not current_user.is_admin and current_user.id != id:
        flash('您没有权限访问此页面', 'danger')
        return redirect(url_for('dashboard.index'))
    
    staff = Staff.query.get_or_404(id)
    form = StaffForm(obj=staff)
    
    if form.validate_on_submit():
        # 检查用户名是否已存在（排除当前用户）
        existing_staff = Staff.query.filter_by(username=form.username.data).first()
        if existing_staff and existing_staff.id != id:
            flash('用户名已存在', 'danger')
            return render_template('staff/form.html', form=form, title='编辑员工')
        
        staff.username = form.username.data
        staff.name = form.name.data
        staff.position = form.position.data
        staff.id_number = form.id_number.data
        staff.phone = form.phone.data
        staff.address = form.address.data
        staff.commission_rate = form.commission_rate.data
        
        # 只有管理员可以修改这些字段
        if current_user.is_admin:
            staff.is_admin = form.is_admin.data
            staff.is_active = form.is_active.data
        
        if form.password.data:
            staff.set_password(form.password.data)
        
        db.session.commit()
        
        flash('员工信息已更新', 'success')
        return redirect(url_for('staff.index'))
    
    return render_template('staff/form.html', form=form, title='编辑员工')

# 员工详情
@staff_bp.route('/view/<int:id>')
@login_required
def view(id):
    if not current_user.is_admin and current_user.id != id:
        flash('您没有权限访问此页面', 'danger')
        return redirect(url_for('dashboard.index'))
    
    staff = Staff.query.get_or_404(id)
    return render_template('staff/view.html', staff=staff)

# 禁用/启用员工
@staff_bp.route('/toggle/<int:id>')
@login_required
def toggle(id):
    if not current_user.is_admin:
        flash('您没有权限访问此页面', 'danger')
        return redirect(url_for('dashboard.index'))
    
    staff = Staff.query.get_or_404(id)
    
    # 不能禁用自己
    if staff.id == current_user.id:
        flash('不能禁用当前登录的账户', 'danger')
        return redirect(url_for('staff.index'))
    
    staff.is_active = not staff.is_active
    db.session.commit()
    
    status = '启用' if staff.is_active else '禁用'
    flash(f'员工 {staff.name} 已{status}', 'success')
    return redirect(url_for('staff.index'))