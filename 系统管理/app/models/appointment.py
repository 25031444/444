from app import db
from datetime import datetime

class Appointment(db.Model):
    """预约模型"""
    __tablename__ = 'appointments'
    
    id = db.Column(db.Integer, primary_key=True)
    member_id = db.Column(db.Integer, db.ForeignKey('members.id'))
    service_id = db.Column(db.Integer, db.ForeignKey('services.id'))
    staff_id = db.Column(db.Integer, db.ForeignKey('staff.id'))
    appointment_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)
    status = db.Column(db.String(20))  # pending, confirmed, completed, cancelled
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Appointment {self.id}>'