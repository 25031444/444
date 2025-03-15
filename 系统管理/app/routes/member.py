from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required
from app import db
from app.models.member import Member, MemberLevel
from app.forms.member import MemberForm, MemberLevelForm

member_bp = Blueprint('member', __name__)

# 会员列表
@member_bp.route('/')
@login_required
def index():
    members = Member.query.order_by(Member.name).all()
    return render_template('member/index.html', members=members)

# 添加会员
@member_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    form = MemberForm()
    if form.validate_on_submit():
        member = Member(
            name=form.name.data,
            phone=form.phone.data,
            gender=form.gender.data,
            birthday=form.birthday.data,
            address=form.address.data,
            level_id=form.level_id.data.id if form.level_id.data else None,
            referrer_id=form.referrer_id.data.id if form.referrer_id.data else None,
            notes=form.notes.data
        )
        db.session.add(member)
        db.session.commit()
        flash('会员添加成功', 'success')
        return redirect(url_for('member.index'))
    return render_template('member/form.html', form=form, title='添加会员')

# 编辑会员
@member_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    member = Member.query.get_or_404(id)
    form = MemberForm(obj=member)
    if form.validate_on_submit():
        member.name = form.name.data
        member.phone = form.phone.data
        member.gender = form.gender.data
        member.birthday = form.birthday.data
        member.address = form.address.data
        member.level_id = form.level_id.data.id if form.level_id.data else None
        member.referrer_id = form.referrer_id.data.id if form.referrer_id.data else None
        member.notes = form.notes.data
        db.session.commit()
        flash('会员信息已更新', 'success')
        return redirect(url_for('member.index'))
    return render_template('member/form.html', form=form, title='编辑会员')

# 会员详情
@member_bp.route('/view/<int:id>')
@login_required
def view(id):
    member = Member.query.get_or_404(id)
    return render_template('member/view.html', member=member)

# 会员级别列表
@member_bp.route('/levels')
@login_required
def levels():
    levels = MemberLevel.query.order_by(MemberLevel.min_recharge).all()
    return render_template('member/levels.html', levels=levels)

# 添加会员级别
@member_bp.route('/levels/add', methods=['GET', 'POST'])
@login_required
def add_level():
    form = MemberLevelForm()
    if form.validate_on_submit():
        level = MemberLevel(
            name=form.name.data,
            min_recharge=form.min_recharge.data,
            max_recharge=form.max_recharge.data,
            points_percentage=form.points_percentage.data,
            description=form.description.data
        )
        db.session.add(level)
        db.session.commit()
        flash('会员级别添加成功', 'success')
        return redirect(url_for('member.levels'))
    return render_template('member/level_form.html', form=form, title='添加会员级别')

# 编辑会员级别
@member_bp.route('/levels/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_level(id):
    level = MemberLevel.query.get_or_404(id)
    form = MemberLevelForm(obj=level)
    if form.validate_on_submit():
        level.name = form.name.data
        level.min_recharge = form.min_recharge.data
        level.max_recharge = form.max_recharge.data
        level.points_percentage = form.points_percentage.data
        level.description = form.description.data
        db.session.commit()
        flash('会员级别已更新', 'success')
        return redirect(url_for('member.levels'))
    return render_template('member/level_form.html', form=form, title='编辑会员级别')