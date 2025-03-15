from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.models.payment import Payment
from app.models.member import Member
from app.forms.payment import PaymentForm
from datetime import datetime

payment_bp = Blueprint('payment', __name__)

# 支付列表
@payment_bp.route('/')
@login_required
def index():
    payments = Payment.query.order_by(Payment.payment_time.desc()).all()
    return render_template('payment/index.html', payments=payments)

# 添加支付
@payment_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    form = PaymentForm()
    if form.validate_on_submit():
        # 获取会员
        member = Member.query.get(form.member_id.data.id)
        
        # 检查积分是否足够
        if form.points_used.data and form.points_used.data > member.points:
            flash('会员积分不足', 'danger')
            return render_template('payment/form.html', form=form, title='添加支付')
        
        # 创建支付记录
        payment = Payment(
            member_id=form.member_id.data.id,
            appointment_id=form.appointment_id.data.id if form.appointment_id.data else None,
            delivery_order_id=form.delivery_order_id.data.id if form.delivery_order_id.data else None,
            amount=form.amount.data,
            payment_method=form.payment_method.data,
            points_used=form.points_used.data or 0,
            notes=form.notes.data,
            payment_time=datetime.now()
        )
        
        # 如果使用账户余额支付
        if form.payment_method.data == 'balance':
            if member.balance < form.amount.data:
                flash('会员余额不足', 'danger')
                return render_template('payment/form.html', form=form, title='添加支付')
            
            # 扣除余额
            member.balance -= form.amount.data
        
        # 扣除积分
        if form.points_used.data:
            member.points -= form.points_used.data
        
        db.session.add(payment)
        db.session.commit()
        
        flash('支付记录添加成功', 'success')
        return redirect(url_for('payment.index'))
    
    return render_template('payment/form.html', form=form, title='添加支付')

# 支付详情
@payment_bp.route('/view/<int:id>')
@login_required
def view(id):
    payment = Payment.query.get_or_404(id)
    return render_template('payment/view.html', payment=payment)

# 获取会员信息（用于AJAX请求）
@payment_bp.route('/get_member_info/<int:id>')
@login_required
def get_member_info(id):
    member = Member.query.get_or_404(id)
    return {
        'balance': member.balance,
        'points': member.points,
        'level': member.level.name if member.level else '无'
    }