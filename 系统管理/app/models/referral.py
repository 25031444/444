from app import db
from datetime import datetime

class Referral(db.Model):
    __tablename__ = 'referrals'
    
    id = db.Column(db.Integer, primary_key=True)
    referrer_id = db.Column(db.Integer, db.ForeignKey('members.id'), nullable=False)
    referred_id = db.Column(db.Integer, db.ForeignKey('members.id'), nullable=False)
    reward_amount = db.Column(db.Float, default=0.0)
    reward_points = db.Column(db.Integer, default=0)
    status = db.Column(db.String(20), default='pending')  # pending, rewarded
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    referrer = db.relationship('Member', foreign_keys=[referrer_id])
    referred = db.relationship('Member', foreign_keys=[referred_id])
    
    def __repr__(self):
        return f'<Referral {self.id}>'