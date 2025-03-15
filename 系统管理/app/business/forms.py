from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SubmitField
from wtforms.validators import DataRequired

class ServiceTypeForm(FlaskForm):
    """服务类型表单"""
    name = StringField('类型名称', validators=[DataRequired('请输入类型名称')])
    description = TextAreaField('描述')
    is_active = BooleanField('启用状态', default=True)
    submit = SubmitField('提交')