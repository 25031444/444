from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, DateField, TextAreaField, FloatField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Length, Optional, Email, NumberRange
from wtforms_sqlalchemy.fields import QuerySelectField
from app.models.member import MemberLevel, Member

def get_member_levels():
    return MemberLevel.query.order_by(MemberLevel.min_recharge).all()

def get_members():
    return Member.query.order_by(Member.name).all()

class MemberForm(FlaskForm):
    name = StringField('姓名', validators=[DataRequired(), Length(1, 64)])
    phone = StringField('电话', validators=[DataRequired(), Length(1, 20)])
    gender = SelectField('性别', choices=[('male', '男'), ('female', '女')])
    birthday = DateField('生日', format='%Y-%m-%d', validators=[Optional()])
    address = StringField('地址', validators=[Optional(), Length(0, 128)])
    level_id = QuerySelectField('会员级别', query_factory=get_member_levels, get_label='name', allow_blank=True, blank_text='请选择会员级别')
    referrer_id = QuerySelectField('推荐人', query_factory=get_members, get_label='name', allow_blank=True, blank_text='请选择推荐人', validators=[Optional()])
    notes = TextAreaField('备注', validators=[Optional()])
    submit = SubmitField('保存')

class MemberLevelForm(FlaskForm):
    name = StringField('级别名称', validators=[DataRequired(), Length(1, 64)])
    min_recharge = FloatField('最低充值金额', validators=[DataRequired(), NumberRange(min=0)])
    max_recharge = FloatField('最高充值金额', validators=[Optional(), NumberRange(min=0)])
    points_percentage = IntegerField('积分返还百分比', validators=[Optional(), NumberRange(min=0, max=100)])
    description = TextAreaField('描述', validators=[Optional()])
    submit = SubmitField('保存')