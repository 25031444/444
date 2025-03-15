from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from app import db
from app.models.delivery import DeliveryOrder, DeliveryItem
from app.models.business import Service, Product
from app.forms.delivery import DeliveryOrderForm, DeliveryItemForm
from datetime import datetime

delivery_bp = Blueprint('delivery', __name__)

# 外卖订单列表
@delivery_bp.route('/')
@login_required
def index():
    orders = DeliveryOrder.query.order_by(DeliveryOrder.created_at.desc()).all()
    return render_template('delivery/index.html', orders=orders)

# 添加外卖订单
@delivery_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    form = DeliveryOrderForm()
    if form.validate_on_submit():
        order = DeliveryOrder(
            member_id=form.member_id.data.id,
            staff_id=form.staff_id.data.id if form.staff_id.data else None,
            address=form.address.data,
            total_amount=0,  # 初始金额为0，后续添加项目后更新
            status=form.status.data,
            notes=form.notes.data
        )
        db.session.add(order)
        db.session.commit()
        flash('外卖订单创建成功，请添加订单项目', 'success')
        return redirect(url_for('delivery.edit_items', id=order.id))
    return render_template('delivery/form.html', form=form, title='添加外卖订单')

# 编辑外卖订单
@delivery_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    order = DeliveryOrder.query.get_or_404(id)
    form = DeliveryOrderForm(obj=order)
    if form.validate_on_submit():
        order.member_id = form.member_id.data.id
        order.staff_id = form.staff_id.data.id if form.staff_id.data else None
        order.address = form.address.data
        order.status = form.status.data
        order.notes = form.notes.data
        db.session.commit()
        flash('外卖订单信息已更新', 'success')
        return redirect(url_for('delivery.index'))
    return render_template('delivery/form.html', form=form, title='编辑外卖订单')

# 外卖订单详情
@delivery_bp.route('/view/<int:id>')
@login_required
def view(id):
    order = DeliveryOrder.query.get_or_404(id)
    return render_template('delivery/view.html', order=order)

# 编辑订单项目
@delivery_bp.route('/items/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_items(id):
    order = DeliveryOrder.query.get_or_404(id)
    form = DeliveryItemForm()
    
    if form.validate_on_submit():
        item = DeliveryItem(
            order_id=order.id,
            service_id=form.service_id.data.id if form.service_id.data else None,
            product_id=form.product_id.data.id if form.product_id.data else None,
            quantity=form.quantity.data,
            price=form.price.data
        )
        db.session.add(item)
        
        # 更新订单总金额
        order.total_amount += item.price * item.quantity
        db.session.commit()
        
        flash('项目已添加', 'success')
        return redirect(url_for('delivery.edit_items', id=order.id))
    
    