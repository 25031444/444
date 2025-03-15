from flask import Blueprint, render_template
from flask_login import login_required
from app.models.member import Member
from app.models.appointment import Appointment
from app.models.business import Service
from app.models.payment import Payment
from app.models.delivery import DeliveryOrder
from app import db
from datetime import datetime, timedelta
import json

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/')
@login_required
def index():
    # 获取统计数据
    total_members = Member.query.count()
    total_appointments = Appointment.query.count()
    total_services = Service.query.count()
    
    # 获取今日预约
    today = datetime.now().date()
    today_start = datetime.combine(today, datetime.min.time())
    today_end = datetime.combine(today, datetime.max.time())
    today_appointments = Appointment.query.filter(
        Appointment.appointment_time.between(today_start, today_end)
    ).order_by(Appointment.appointment_time).all()
    
    # 获取最近的预约
    recent_appointments = Appointment.query.order_by(
        Appointment.appointment_time.desc()
    ).limit(5).all()
    
    # 获取最近的外卖订单
    recent_deliveries = DeliveryOrder.query.order_by(
        DeliveryOrder.created_at.desc()
    ).limit(5).all()
    
    # 获取最近7天的收入数据
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=6)
    
    chart_dates = []
    chart_earnings = []
    
    for i in range(7):
        date = start_date + timedelta(days=i)
        day_start = datetime.combine(date, datetime.min.time())
        day_end = datetime.combine(date, datetime.max.time())
        
        # 计算当天的收入
        payments = Payment.query.filter(
            Payment.payment_time.between(day_start, day_end)
        ).all()
        
        daily_earnings = sum(payment.amount for payment in payments)
        
        chart_dates.append(date.strftime('%m-%d'))
        chart_earnings.append(float(daily_earnings))
    
    return render_template(
        'dashboard/index.html',
        total_members=total_members,
        total_appointments=total_appointments,
        total_services=total_services,
        today_appointments=today_appointments,
        recent_appointments=recent_appointments,
        recent_deliveries=recent_deliveries,
        chart_dates=json.dumps(chart_dates),
        chart_earnings=json.dumps(chart_earnings)
    )