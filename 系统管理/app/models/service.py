from app import db
from datetime import datetime

class SystemService(db.Model):
    """系统服务模型（用于管理系统内部服务）"""
    __tablename__ = 'system_services'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, index=True)
    description = db.Column(db.String(256))
    status = db.Column(db.String(20), default='stopped')  # running, stopped, error
    command = db.Column(db.String(256))
    auto_start = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __init__(self, name=None, description=None, command=None, auto_start=False):
        self.name = name
        self.description = description
        self.command = command
        self.auto_start = auto_start
    
    def __repr__(self):
        return f'<SystemService {self.name}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'status': self.status,
            'command': self.command,
            'auto_start': self.auto_start,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S')
        }
    
    def start(self):
        """启动服务"""
        # 实现服务启动逻辑
        self.status = 'running'
        db.session.commit()
        return True
    
    def stop(self):
        """停止服务"""
        # 实现服务停止逻辑
        self.status = 'stopped'
        db.session.commit()
        return True
    
    def restart(self):
        """重启服务"""
        # 实现服务重启逻辑
        self.status = 'running'
        db.session.commit()
        return True