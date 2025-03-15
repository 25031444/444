from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, DateField, TimeField, SubmitField
from wtforms.validators import DataRequired, Optional
from wtforms_sqlalchemy.fields import QuerySelectField
from app.models.member import Member
from app.models.business import Service
from app.models.staff import Staff
from datetime import datetime, time

def get_members():
    return Member.query.order_by(Member.name).all()

def get_services():
    return Service.query.filter_by(is_active=True).order_by(Service.name).all()

def get_staff():
    return Staff.query.filter_by(is_active=True).order_by(Staff.name).all()

class AppointmentForm(FlaskForm):
    member_id = QuerySelectField('会员', query_factory=get_members, get_label='name', allow_blank=True, blank_text='请选择会员')
    service_id = QuerySelectField('服务项目', query_factory=get_services, get_label='name', allow_blank=True, blank_text='请选择服务项目')
    staff_id = QuerySelectField('技师', query_factory=get_staff, get_label='name', allow_blank=True, blank_text='请选择技师', validators=[Optional()])
    appointment_date = DateField('预约日期', format='%Y-%m-%d', validators=[DataRequired()])
    appointment_time = TimeField('预约时间', format='%H:%M', validators=[DataRequired()])
    status = SelectField('状态', choices=[
        ('pending', '待确认'),
        ('confirmed', '已确认'),
        ('completed', '已完成'),
        ('cancelled', '已取消')
    ])
    notes = TextAreaField('备注', validators=[Optional()])
    submit = SubmitField('保存')