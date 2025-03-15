from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.models.appointment import Appointment
from app.forms.appointment import AppointmentForm
from datetime import datetime, timedelta

appointment_bp = Blueprint('appointment', __name__)

# 预约列表
@appointment_bp.route('/')
@login_required
def index():
    appointments = Appointment.query.order_by(Appointment.appointment_time.desc()).all()
    return render_template('appointment/index.html', appointments=appointments)

# 添加预约
@appointment_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    form = AppointmentForm()
    if form.validate_on_submit():
        # 合并日期和时间
        appointment_datetime = datetime.combine(form.appointment_date.data, form.appointment_time.data)
        
        appointment = Appointment(
            member_id=form.member_id.data.id,
            service_id=form.service_id.data.id,
            staff_id=form.staff_id.data.id if form.staff_id.data else None,
            appointment_time=appointment_datetime,
            status=form.status.data,
            notes=form.notes.data
        )
        db.session.add(appointment)
        db.session.commit()
        flash('预约添加成功', 'success')
        return redirect(url_for('appointment.index'))
    return render_template('appointment/form.html', form=form, title='添加预约')

# 编辑预约
@appointment_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    appointment = Appointment.query.get_or_404(id)
    form = AppointmentForm(obj=appointment)
    
    # 分离日期和时间
    if request.method == 'GET':
        form.appointment_date.data = appointment.appointment_time.date()
        form.appointment_time.data = appointment.appointment_time.time()
    
    if form.validate_on_submit():
        # 合并日期和时间
        appointment_datetime = datetime.combine(form.appointment_date.data, form.appointment_time.data)
        
        appointment.member_id = form.member_id.data.id
        appointment.service_id = form.service_id.data.id
        appointment.staff_id = form.staff_id.data.id if form.staff_id.data else None
        appointment.appointment_time = appointment_datetime
        appointment.status = form.status.data
        appointment.notes = form.notes.data
        
        db.session.commit()
        flash('预约信息已更新', 'success')
        return redirect(url_for('appointment.index'))
    return render_template('appointment/form.html', form=form, title='编辑预约')

# 预约详情
@appointment_bp.route('/view/<int:id>')
@login_required
def view(id):
    appointment = Appointment.query.get_or_404(id)
    return render_template('appointment/view.html', appointment=appointment)

# 取消预约
@appointment_bp.route('/cancel/<int:id>')
@login_required
def cancel(id):
    appointment = Appointment.query.get_or_404(id)
    appointment.status = 'cancelled'
    db.session.commit()
    flash('预约已取消', 'success')
    return redirect(url_for('appointment.index'))

# 完成预约
@appointment_bp.route('/complete/<int:id>')
@login_required
def complete(id):
    appointment = Appointment.query.get_or_404(id)
    appointment.status = 'completed'
    db.session.commit()
    flash('预约已完成', 'success')
    return redirect(url_for('appointment.index'))

# 日历视图
@appointment_bp.route('/calendar')
@login_required
def calendar():
    # 获取当前日期
    today = datetime.now().date()
    start_date = request.args.get('start_date', today.strftime('%Y-%m-%d'))
    start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
    
    # 获取一周的日期
    dates = []
    for i in range(7):
        dates.append(start_date + timedelta(days=i))
    
    # 获取这一周的预约
    start_datetime = datetime.combine(dates[0], datetime.min.time())
    end_datetime = datetime.combine(dates[-1], datetime.max.time())
    appointments = Appointment.query.filter(
        Appointment.appointment_time.between(start_datetime, end_datetime)
    ).order_by(Appointment.appointment_time).all()
    
    # 按日期和时间组织预约
    appointments_by_date = {}
    for date in dates:
        appointments_by_date[date] = []
    
    for appointment in appointments:
        appointment_date = appointment.appointment_time.date()
        if appointment_date in appointments_by_date:
            appointments_by_date[appointment_date].append(appointment)
    
    return render_template(
        'appointment/calendar.html',
        dates=dates,
        appointments_by_date=appointments_by_date,
        prev_week=(start_date - timedelta(days=7)).strftime('%Y-%m-%d'),
        next_week=(start_date + timedelta(days=7)).strftime('%Y-%m-%d'),
        today=today.strftime('%Y-%m-%d')
    )