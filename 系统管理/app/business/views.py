from flask import render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from . import business
from app import db
from app.models.business import ServiceType, Service, ServicePrice, Product, ProductPrice
from .forms import ServiceTypeForm
from datetime import datetime

# 服务类型管理
@business.route('/service_types')
@login_required
def service_types():
    """服务类型列表"""
    service_types = ServiceType.query.all()
    return render_template('business/service_types.html', service_types=service_types)

@business.route('/add_service_type', methods=['GET', 'POST'])
@login_required
def add_service_type():
    """添加服务类型"""
    form = ServiceTypeForm()
    if form.validate_on_submit():
        service_type = ServiceType(
            name=form.name.data,
            description=form.description.data,
            is_active=form.is_active.data
        )
        db.session.add(service_type)
        db.session.commit()
        flash('服务类型添加成功')
        return redirect(url_for('business.service_types'))
    return render_template('business/service_type_form.html', form=form, title='添加服务类型')

@business.route('/edit_service_type/<int:type_id>', methods=['GET', 'POST'])
@login_required
def edit_service_type(type_id):
    """编辑服务类型"""
    service_type = ServiceType.query.get_or_404(type_id)
    form = ServiceTypeForm(obj=service_type)
    if form.validate_on_submit():
        form.populate_obj(service_type)
        db.session.commit()
        flash('服务类型更新成功')
        return redirect(url_for('business.service_types'))
    return render_template('business/service_type_form.html', form=form, title='编辑服务类型')

@business.route('/delete_service_type', methods=['POST'])
@login_required
def delete_service_type():
    """删除服务类型"""
    type_id = request.form.get('id')
    service_type = ServiceType.query.get_or_404(type_id)
    
    # 检查是否有服务使用此类型
    services = Service.query.filter_by(type_id=type_id).first()
    if services:
        return jsonify({"code": 1, "msg": "该类型下有服务项目，无法删除"})
    
    db.session.delete(service_type)
    db.session.commit()
    return jsonify({"code": 0, "msg": "删除成功"})

# 服务管理
@business.route('/services')
@login_required
def services():
    """服务列表"""
    services = Service.query.all()
    return render_template('business/services.html', services=services)

@business.route('/services/add', methods=['GET', 'POST'])
@login_required
def add_service():
    """添加服务"""
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        duration = request.form.get('duration')
        type_id = request.form.get('type_id')
        price = request.form.get('price')
        member_price = request.form.get('member_price')
        
        if Service.query.filter_by(name=name).first():
            flash('服务已存在', 'error')
            return redirect(url_for('business.add_service'))
        
        service = Service(
            name=name,
            description=description,
            duration=duration,
            type_id=type_id
        )
        
        db.session.add(service)
        db.session.flush()  # 获取 service.id
        
        # 添加价格
        service_price = ServicePrice(
            service_id=service.id,
            price=price,
            member_price=member_price
        )
        
        db.session.add(service_price)
        db.session.commit()
        flash('服务添加成功')
        return redirect(url_for('business.services'))
    
    types = ServiceType.query.all()
    return render_template('business/add_service.html', types=types)

# 产品管理
@business.route('/products')
@login_required
def products():
    """产品列表"""
    products = Product.query.all()
    return render_template('business/products.html', products=products)