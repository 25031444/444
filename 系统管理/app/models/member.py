from app import db
from datetime import datetime

class MemberLevel(db.Model):
    __tablename__ = 'member_levels'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    min_recharge = db.Column(db.Float, nullable=False)  # 最低充值金额
    max_recharge = db.Column(db.Float)  # 最高充值金额
    points_percentage = db.Column(db.Integer)  # 积分返还百分比
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    members = db.relationship('Member', backref='level', lazy='dynamic')
    
    def __repr__(self):
        return f'<MemberLevel {self.name}>'

class Member(db.Model):
    __tablename__ = 'members'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    phone = db.Column(db.String(20), nullable=False, unique=True)
    gender = db.Column(db.String(10))
    birthday = db.Column(db.Date)
    address = db.Column(db.String(128))
    level_id = db.Column(db.Integer, db.ForeignKey('member_levels.id'))
    referrer_id = db.Column(db.Integer, db.ForeignKey('members.id'))
    balance = db.Column(db.Float, default=0.0)  # 账户余额
    points = db.Column(db.Integer, default=0)  # 积分
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关联
    referrals = db.relationship('Member', backref=db.backref('referrer', remote_side=[id]), lazy='dynamic')
    appointments = db.relationship('Appointment', backref='member', lazy='dynamic')
    delivery_orders = db.relationship('DeliveryOrder', backref='member', lazy='dynamic')
    payments = db.relationship('Payment', backref='member', lazy='dynamic')
    recharges = db.relationship('Recharge', backref='member', lazy='dynamic')
    
    def __repr__(self):
        return f'<Member {self.name}>'