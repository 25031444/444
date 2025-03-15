from app import db
from datetime import datetime

class ActivityLog(db.Model):
    __tablename__ = 'activity_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)  # 可以是 staff_id 或 member_id
    user_type = db.Column(db.String(20))  # 'staff' 或 'member'
    action = db.Column(db.String(64))  # 例如 'login', 'create', 'update', 'delete'
    resource_type = db.Column(db.String(64))  # 例如 'member', 'service', 'product'
    resource_id = db.Column(db.Integer)
    details = db.Column(db.Text)  # 可以存储 JSON 格式的详细信息
    ip_address = db.Column(db.String(64))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<ActivityLog {self.action} {self.resource_type} {self.resource_id}>'