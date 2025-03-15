from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.models.recharge import Recharge
from app.models.member import Member, MemberLevel
from app.forms.payment import RechargeForm
from datetime import datetime

recharge_bp = Blueprint('recharge', __name__)

# 充值列表
@recharge_bp.route('/')
@login_required
def index():
    recharges = Recharge.query.order_by(Recharge.recharge_time.desc()).all()
    return render_template('recharge/index.html', recharges=recharges)

# 添加充值
@recharge_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    form = RechargeForm()
    if form.validate_on_submit():
        # 获取会员
        member = Member.query.get(form.member_id.data.id)
        
        # 计算积分
        points_percentage = 0
        if member.level:
            points_percentage = member.level.points_percentage or 0
        
        points_added = int(form.amount.data * points_percentage / 100)
        
        # 创建充值记录
        recharge = Recharge(
            member_id=form.member_id.data.id,
            amount=form.amount.data,
            payment_method=form.payment_method.data,
            points_added=points_added,
            notes=form.notes.data,
            recharge_time=datetime.now()
        )
        
        # 更新会员余额和积分
        member.balance += form.amount.data
        member.points += points_added
        
        # 检查是否需要更新会员级别
        total_recharge = member.balance  # 简化处理，实际应该是累计充值金额
        levels = MemberLevel.query.order_by(MemberLevel.min_recharge.desc()).all()
        
        for level in levels:
            if total_recharge >= level.min_recharge:
                if level.max_recharge is None or total_recharge <= level.max_recharge:
                    member.level_id = level.id
                    break
        
        db.session.add(recharge)
        db.session.commit()
        
        flash('充值成功', 'success')
        return redirect(url_for('recharge.index'))
    
    return render_template('recharge/form.html', form=form, title='添加充值')

# 充值详情
@recharge_bp.route('/view/<int:id>')
@login_required
def view(id):
    recharge = Recharge.query.get_or_404(id)
    return render_template('recharge/view.html', recharge=recharge)

# 获取会员信息（用于AJAX请求）
@recharge_bp.route('/get_member_info/<int:id>')
@login_required
def get_member_info(id):
    member = Member.query.get_or_404(id)
    return {
        'balance': member.balance,
        'points': member.points,
        'level': member.level.name if member.level else '无',
        'points_percentage': member.level.points_percentage if member.level else 0
    }