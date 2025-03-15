from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required
from app import db
from app.models.business import Product, ProductPrice
from app.forms.business import ProductForm, ProductPriceForm

product_bp = Blueprint('product', __name__)

# 产品列表
@product_bp.route('/')
@login_required
def index():
    products = Product.query.order_by(Product.name).all()
    return render_template('product/index.html', products=products)

# 添加产品
@product_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    form = ProductForm()
    if form.validate_on_submit():
        product = Product(
            name=form.name.data,
            description=form.description.data,
            base_price=form.base_price.data,
            cost=form.cost.data,
            stock=form.stock.data,
            commission_rate=form.commission_rate.data,
            is_delivery=form.is_delivery.data,
            is_active=form.is_active.data
        )
        db.session.add(product)
        db.session.commit()
        flash('产品添加成功', 'success')
        return redirect(url_for('product.index'))
    return render_template('product/form.html', form=form, title='添加产品')

# 编辑产品
@product_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    product = Product.query.get_or_404(id)
    form = ProductForm(obj=product)
    if form.validate_on_submit():
        product.name = form.name.data
        product.description = form.description.data
        product.base_price = form.base_price.data
        product.cost = form.cost.data
        product.stock = form.stock.data
        product.commission_rate = form.commission_rate.data
        product.is_delivery = form.is_delivery.data
        product.is_active = form.is_active.data
        db.session.commit()
        flash('产品信息已更新', 'success')
        return redirect(url_for('product.index'))
    return render_template('product/form.html', form=form, title='编辑产品')

# 产品详情
@product_bp.route('/view/<int:id>')
@login_required
def view(id):
    product = Product.query.get_or_404(id)
    return render_template('product/view.html', product=product)

# 产品价格列表
@product_bp.route('/prices')
@login_required
def prices():
    prices = ProductPrice.query.all()
    return render_template('product/prices.html', prices=prices)

# 添加产品价格
@product_bp.route('/prices/add', methods=['GET', 'POST'])
@login_required
def add_price():
    form = ProductPriceForm()
    if form.validate_on_submit():
        price = ProductPrice(
            product_id=form.product_id.data.id,
            level_id=form.level_id.data.id,
            price=form.price.data,
            commission_rate=form.commission_rate.data
        )
        db.session.add(price)
        db.session.commit()
        flash('产品价格添加成功', 'success')
        return redirect(url_for('product.prices'))
    return render_template('product/price_form.html', form=form, title='添加产品价格')

# 编辑产品价格
@product_bp.route('/prices/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_price(id):
    price = ProductPrice.query.get_or_404(id)
    form = ProductPriceForm(obj=price)
    if form.validate_on_submit():
        price.product_id = form.product_id.data.id
        price.level_id = form.level_id.data.id
        price.price = form.price.data
        price.commission_rate = form.commission_rate.data
        db.session.commit()
        flash('产品价格已更新', 'success')
        return redirect(url_for('product.prices'))
    return render_template('product/price_form.html', form=form, title='编辑产品价格')