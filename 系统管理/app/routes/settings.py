from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.models.settings import SystemSetting
from app.forms.settings import SystemSettingForm

settings_bp = Blueprint('settings', __name__)

# 系统设置列表
@settings_bp.route('/')
@login_required
def index():
    if not current_user.is_admin:
        flash('您没有权限访问此页面', 'danger')
        return redirect(url_for('dashboard.index'))
    
    settings = SystemSetting.query.order_by(SystemSetting.key).all()
    return render_template('settings/index.html', settings=settings)

# 添加系统设置
@settings_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    if not current_user.is_admin:
        flash('您没有权限访问此页面', 'danger')
        return redirect(url_for('dashboard.index'))
    
    form = SystemSettingForm()
    if form.validate_on_submit():
        # 检查键是否已存在
        if SystemSetting.query.filter_by(key=form.key.data).first():
            flash('设置键已存在', 'danger')
            return render_template('settings/form.html', form=form, title='添加系统设置')
        
        setting = SystemSetting(
            key=form.key.data,
            value=form.value.data,
            description=form.description.data
        )
        
        db.session.add(setting)
        db.session.commit()
        
        flash('系统设置添加成功', 'success')
        return redirect(url_for('settings.index'))
    
    return render_template('settings/form.html', form=form, title='添加系统设置')

# 编辑系统设置
@settings_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    if not current_user.is_admin:
        flash('您没有权限访问此页面', 'danger')
        return redirect(url_for('dashboard.index'))
    
    setting = SystemSetting.query.get_or_404(id)
    form = SystemSettingForm(obj=setting)
    
    if form.validate_on_submit():
        # 检查键是否已存在（排除当前设置）
        existing_setting = SystemSetting.query.filter_by(key=form.key.data).first()
        if existing_setting and existing_setting.id != id:
            flash('设置键已存在', 'danger')
            return render_template('settings/form.html', form=form, title='编辑系统设置')
        
        setting.key = form.key.data
        setting.value = form.value.data
        setting.description = form.description.data
        
        db.session.commit()
        
        flash('系统设置已更新', 'success')
        return redirect(url_for('settings.index'))
    
    return render_template('settings/form.html', form=form, title='编辑系统设置')

# 删除系统设置
@settings_bp.route('/delete/<int:id>')
@login_required
def delete(id):
    if not current_user.is_admin:
        flash('您没有权限访问此页面', 'danger')
        return redirect(url_for('dashboard.index'))
    
    setting = SystemSetting.query.get_or_404(id)
    
    db.session.delete(setting)
    db.session.commit()
    
    flash('系统设置已删除', 'success')
    return redirect(url_for('settings.index'))

# 获取系统设置值（辅助函数）
def get_setting(key, default=None):
    setting = SystemSetting.query.filter_by(key=key).first()
    return setting.value if setting else default