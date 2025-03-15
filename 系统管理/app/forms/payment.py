from flask_wtf import FlaskForm
from wtforms import FloatField, SelectField, TextAreaField, SubmitField, IntegerField
from wtforms.validators import DataRequired, NumberRange, Optional
from wtforms_sqlalchemy.fields import QuerySelectField
from app.models.member import Member
from app.models.appointment import Appointment
from app.models.delivery import DeliveryOrder

def get_members():
    return Member.query.order_by(Member.name).all()

def get_appointments():
    return Appointment.query.filter_by(status='completed').order_by(Appointment.appointment_time.desc()).all()

def get_delivery_orders():
    return DeliveryOrder.query.filter_by(status='completed').order_by(DeliveryOrder.created_at.desc()).all()

class RechargeForm(FlaskForm):
    member_id = QuerySelectField('会员', query_factory=get_members, get_label='name', allow_blank=True, blank_text='请选择会员')
    amount = FloatField('充值金额', validators=[DataRequired(), NumberRange(min=0)])
    payment_method = SelectField('支付方式', choices=[
        ('cash', '现金'),
        ('wechat', '微信'),
        ('alipay', '支付宝'),
        ('card', '银行卡')
    ])
    notes = TextAreaField('备注', validators=[Optional()])
    submit = SubmitField('充值')

class PaymentForm(FlaskForm):
    member_id = QuerySelectField('会员', query_factory=get_members, get_label='name', allow_blank=True, blank_text='请选择会员')
    appointment_id = QuerySelectField('关联预约', query_factory=get_appointments, get_label='id', allow_blank=True, blank_text='请选择预约', validators=[Optional()])
    delivery_order_id = QuerySelectField('关联外卖订单', query_factory=get_delivery_orders, get_label='id', allow_blank=True, blank_text='请选择外卖订单', validators=[Optional()])
    amount = FloatField('金额', validators=[DataRequired(), NumberRange(min=0)])
    payment_method = SelectField('支付方式', choices=[
        ('cash', '现金'),
        ('wechat', '微信'),
        ('alipay', '支付宝'),
        ('card', '银行卡'),
        ('balance', '账户余额')
    ])
    points_used = IntegerField('使用积分', validators=[Optional(), NumberRange(min=0)])
    notes = TextAreaField('备注', validators=[Optional()])
    submit = SubmitField('支付')