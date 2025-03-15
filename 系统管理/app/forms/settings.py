from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length, Optional

class SystemSettingForm(FlaskForm):
    key = StringField('键', validators=[DataRequired(), Length(1, 64)])
    value = TextAreaField('值', validators=[DataRequired()])
    description = TextAreaField('描述', validators=[Optional()])
    submit = SubmitField('保存')