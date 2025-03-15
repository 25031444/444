from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SelectField, FloatField, SubmitField
from wtforms.validators import DataRequired, Length, Optional, EqualTo, NumberRange

class StaffForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired(), Length(1, 64)])
    name = StringField('姓名', validators=[DataRequired(), Length(1, 64)])
    password = PasswordField('密码', validators=[
        Optional(),
        Length(6, 128),
        EqualTo('password2', message='两次输入的密码不匹配')
    ])
    password2 = PasswordField('确认密码', validators=[Optional()])
    position = StringField('职位', validators=[DataRequired(), Length(1, 64)])
    id_number = StringField('身份证号', validators=[Optional(), Length(18, 18)])
    phone = StringField('电话', validators=[Optional(), Length(1, 20)])
    address = StringField('地址', validators=[Optional(), Length(0, 128)])
    commission_rate = FloatField('提成比例(%)', validators=[Optional(), NumberRange(min=0, max=100)])
    is_admin = BooleanField('管理员权限')
    is_active = BooleanField('是否启用')
    submit = SubmitField('保存')

class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('原密码', validators=[DataRequired()])
    password = PasswordField('新密码', validators=[
        DataRequired(),
        Length(6, 128),
        EqualTo('password2', message='两次输入的密码不匹配')
    ])
    password2 = PasswordField('确认新密码', validators=[DataRequired()])
    submit = SubmitField('修改密码')