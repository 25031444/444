from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required
from app import db
from app.models.business import ServiceType, Service, ServicePrice
from app.forms.business import ServiceTypeForm, ServiceForm, ServicePriceForm

service_bp = Blueprint('service', __name__)

# 服务类型列表
@service_bp.route('/types')
@login_required
def types():
    types = ServiceType.query.order_by(ServiceType.name).all()
    return render_template('service/types.html', types=types)

# 添加服务类型
@service_bp.route('/types/add', methods=['GET', 'POST'])
@login_required
def add_type():
    form = ServiceTypeForm()
    if form.validate_on_submit():
        type = ServiceType(
            name=form.name.data,
            description=form.description.data
        )
        db.session.add(type)
        db.session.commit()
        flash('服务类型添加成功', 'success')
        return redirect(url_for('service.types'))
    return render_template('service/type_form.html', form=form, title='添加服务类型')

# 编辑服务类型
@service_bp.route('/types/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_type(id):
    type = ServiceType.query.get_or_404(id)
    form = ServiceTypeForm(obj=type)
    if form.validate_on_submit():
        type.name = form.name.data
        type.description = form.description.data
        db.session.commit()
        flash('服务类型已更新', 'success')
        return redirect(url_for('service.types'))
    return render_template('service/type_form.html', form=form, title='编辑服务类型')

# 服务列表
@service_bp.route('/')
@login_required
def index():
    services = Service.query.order_by(Service.name).all()
    return render_template('service/index.html', services=services)

# 添加服务
@service_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    form = ServiceForm()
    if form.validate_on_submit():
        service = Service(
            name=form.name.data,
            type_id=form.type_id.data.id if form.type_id.data else None,
            description=form.description.data,
            base_price=form.base_price.data,
            cost=form.cost.data,
            duration=form.duration.data,
            commission_rate=form.commission_rate.data,
            is_delivery=form.is_delivery.data,
            is_active=form.is_active.data
        )
        db.session.add(service)
        db.session.commit()
        flash('服务添加成功', 'success')
        return redirect(url_for('service.index'))
    return render_template('service/form.html', form=form, title='添加服务')

# 编辑服务
@service_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    service = Service.query.get_or_404(id)
    form = ServiceForm(obj=service)
    if form.validate_on_submit():
        service.name = form.name.data
        service.type_id = form.type_id.data.id if form.type_id.data else None
        service.description = form.description.data
        service.base_price = form.base_price.data
        service.cost = form.cost.data
        service.duration = form.duration.data
        service.commission_rate = form.commission_rate.data
        service.is_delivery = form.is_delivery.data
        service.is_active = form.is_active.data
        db.session.commit()
        flash('服务信息已更新', 'success')
        return redirect(url_for('service.index'))
    return render_template('service/form.html', form=form, title='编辑服务')

# 服务详情
@service_bp.route('/view/<int:id>')
@login_required
def view(id):
    service = Service.query.get_or_404(id)
    return render_template('service/view.html', service=service)

# 服务价格列表
@service_bp.route('/prices')
@login_required
def prices():
    prices = ServicePrice.query.all()
    return render_template('service/prices.html', prices=prices)

# 添加服务价格
@service_bp.route('/prices/add', methods=['GET', 'POST'])
@login_required
def add_price():
    form = ServicePriceForm()
    if form.validate_on_submit():
        price = ServicePrice(
            service_id=form.service_id.data.id,
            level_id=form.level_id.data.id,
            price=form.price.data,
            commission_rate=form.commission_rate.data
        )
        db.session.add(price)
        db.session.commit()
        flash('服务价格添加成功', 'success')
        return redirect(url_for('service.prices'))
    return render_template('service/price_form.html', form=form, title='添加服务价格')

# 编辑服务价格
@service_bp.route('/prices/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_price(id):
    price = ServicePrice.query.get_or_404(id)
    form = ServicePriceForm(obj=price)
    if form.validate_on_submit():
        price.service_id = form.service_id.data.id
        price.level_id = form.level_id.data.id
        price.price = form.price.data
        price.commission_rate = form.commission_rate.data
        db.session.commit()
        flash('服务价格已更新', 'success')
        return redirect(url_for('service.prices'))
    return render_template('service/price_form.html', form=form, title='编辑服务价格')