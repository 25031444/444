from app import db
from datetime import datetime

class Recharge(db.Model):
    __tablename__ = 'recharges'
    
    id = db.Column(db.Integer, primary_key=True)
    member_id = db.Column(db.Integer, db.ForeignKey('members.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    payment_method = db.Column(db.String(20), nullable=False)  # cash, wechat, alipay, card
    points_added = db.Column(db.Integer, default=0)
    notes = db.Column(db.Text)
    recharge_time = db.Column(db.DateTime, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Recharge {self.id}>'