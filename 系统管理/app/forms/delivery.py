from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, FloatField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Length, Optional, NumberRange
from wtforms_sqlalchemy.fields import QuerySelectField
from app.models.member import Member
from app.models.staff import Staff
from app.models.business import Service, Product

def get_members():
    return Member.query.order_by(Member.name).all()

def get_staff():
    return Staff.query.filter_by(is_active=True).order_by(Staff.name).all()

def get_services():
    return Service.query.filter_by(is_active=True, is_delivery=True).order_by(Service.name).all()

def get_products():
    return Product.query.filter_by(is_active=True, is_delivery=True).order_by(Product.name).all()

class DeliveryOrderForm(FlaskForm):
    member_id = QuerySelectField('会员', query_factory=get_members, get_label='name', allow_blank=True, blank_text='请选择会员')
    staff_id = QuerySelectField('技师', query_factory=get_staff, get_label='name', allow_blank=True, blank_text='请选择技师', validators=[Optional()])
    address = StringField('配送地址', validators=[DataRequired(), Length(1, 128)])
    status = SelectField('状态', choices=[
        ('pending', '待确认'),
        ('confirmed', '已确认'),
        ('completed', '已完成'),
        ('cancelled', '已取消'),
        ('refunded', '已退款')
    ])
    notes = TextAreaField('备注', validators=[Optional()])
    submit = SubmitField('保存')

class DeliveryItemForm(FlaskForm):
    service_id = QuerySelectField('服务项目', query_factory=get_services, get_label='name', allow_blank=True, blank_text='请选择服务项目', validators=[Optional()])
    product_id = QuerySelectField('产品', query_factory=get_products, get_label='name', allow_blank=True, blank_text='请选择产品', validators=[Optional()])
    quantity = IntegerField('数量', validators=[DataRequired(), NumberRange(min=1)])
    price = FloatField('价格', validators=[DataRequired(), NumberRange(min=0)])
    submit = SubmitField('添加')