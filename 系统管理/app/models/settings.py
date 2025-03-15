from app import db
from datetime import datetime

class Settings(db.Model):
    __tablename__ = 'settings'
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(64), unique=True, index=True)
    value = db.Column(db.String(256))
    description = db.Column(db.String(256))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __init__(self, key=None, value=None, description=None):
        self.key = key
        self.value = value
        self.description = description
    
    def __repr__(self):
        return f'<Settings {self.key}>'
    
    @staticmethod
    def get_setting(key, default=None):
        setting = Settings.query.filter_by(key=key).first()
        if setting:
            return setting.value
        return default
    
    @staticmethod
    def set_setting(key, value, description=None):
        setting = Settings.query.filter_by(key=key).first()
        if setting:
            setting.value = value
            if description:
                setting.description = description
        else:
            setting = Settings(key=key, value=value, description=description)
            db.session.add(setting)
        db.session.commit()
        return setting

# 添加这一行，创建 SystemSetting 作为 Settings 的别名
SystemSetting = Settings