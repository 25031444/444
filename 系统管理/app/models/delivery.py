from app import db
from datetime import datetime

class DeliveryOrder(db.Model):
    __tablename__ = 'delivery_orders'
    
    id = db.Column(db.Integer, primary_key=True)
    member_id = db.Column(db.Integer, db.ForeignKey('members.id'), nullable=False)
    staff_id = db.Column(db.Integer, db.ForeignKey('staff.id'))
    address = db.Column(db.String(128), nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending, confirmed, completed, cancelled, refunded
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关联
    items = db.relationship('DeliveryItem', backref='order', lazy='dynamic', cascade='all, delete-orphan')
    payments = db.relationship('Payment', backref='delivery_order', lazy='dynamic')
    
    def __repr__(self):
        return f'<DeliveryOrder {self.id}>'

class DeliveryItem(db.Model):
    __tablename__ = 'delivery_items'
    
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('delivery_orders.id'), nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey('services.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<DeliveryItem {self.id}>'