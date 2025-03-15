from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FloatField, IntegerField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Optional, NumberRange
from wtforms_sqlalchemy.fields import QuerySelectField
from app.models.business import ServiceType, Service
from app.models.member import MemberLevel

def get_service_types():
    return ServiceType.query.order_by(ServiceType.name).all()

def get_services():
    return Service.query.filter_by(is_active=True).order_by(Service.name).all()

def get_member_levels():
    return MemberLevel.query.order_by(MemberLevel.min_recharge).all()

class ServiceTypeForm(FlaskForm):
    """服务类型表单"""
    name = StringField('类型名称', validators=[DataRequired('请输入类型名称')])
    description = TextAreaField('描述')
    is_active = BooleanField('启用状态', default=True)
    submit = SubmitField('提交')

class ServiceForm(FlaskForm):
    name = StringField('名称', validators=[DataRequired(), Length(1, 64)])
    type_id = QuerySelectField('服务类型', query_factory=get_service_types, get_label='name', allow_blank=True, blank_text='请选择服务类型')
    description = TextAreaField('描述', validators=[Optional()])
    base_price = FloatField('基础价格', validators=[DataRequired(), NumberRange(min=0)])
    cost = FloatField('成本', validators=[Optional(), NumberRange(min=0)])
    duration = IntegerField('时长(分钟)', validators=[Optional(), NumberRange(min=0)])
    commission_rate = FloatField('提成比例(%)', validators=[Optional(), NumberRange(min=0, max=100)])
    is_delivery = BooleanField('支持外卖')
    is_active = BooleanField('是否启用')
    submit = SubmitField('保存')

class ServicePriceForm(FlaskForm):
    service_id = QuerySelectField('服务项目', query_factory=get_services, get_label='name', allow_blank=True, blank_text='请选择服务项目')
    level_id = QuerySelectField('会员级别', query_factory=get_member_levels, get_label='name', allow_blank=True, blank_text='请选择会员级别')
    price = FloatField('会员价格', validators=[DataRequired(), NumberRange(min=0)])
    commission_rate = FloatField('提成比例(%)', validators=[Optional(), NumberRange(min=0, max=100)])
    submit = SubmitField('保存')

class ProductForm(FlaskForm):
    name = StringField('名称', validators=[DataRequired(), Length(1, 64)])
    description = TextAreaField('描述', validators=[Optional()])
    base_price = FloatField('基础价格', validators=[DataRequired(), NumberRange(min=0)])
    cost = FloatField('成本', validators=[Optional(), NumberRange(min=0)])
    stock = IntegerField('库存', validators=[Optional(), NumberRange(min=0)])
    commission_rate = FloatField('提成比例(%)', validators=[Optional(), NumberRange(min=0, max=100)])
    is_delivery = BooleanField('支持外卖')
    is_active = BooleanField('是否启用')
    submit = SubmitField('保存')

class ProductPriceForm(FlaskForm):
    product_id = QuerySelectField('产品', query_factory=lambda: Product.query.filter_by(is_active=True).order_by(Product.name).all(), get_label='name', allow_blank=True, blank_text='请选择产品')
    level_id = QuerySelectField('会员级别', query_factory=get_member_levels, get_label='name', allow_blank=True, blank_text='请选择会员级别')
    price = FloatField('会员价格', validators=[DataRequired(), NumberRange(min=0)])
    commission_rate = FloatField('提成比例(%)', validators=[Optional(), NumberRange(min=0, max=100)])
    submit = SubmitField('保存')