import os
from flask_migrate import Migrate, upgrade
from app import create_app, db
from app.models.settings import Settings
from app.models.user import User

app = create_app(os.getenv('FLASK_CONFIG') or 'default')

def init_db():
    with app.app_context():
        # 创建所有表
        db.create_all()
        
        # 添加默认设置
        Settings.set_setting('site_name', '系统管理平台', '网站名称')
        Settings.set_setting('site_description', '一个功能强大的系统管理平台', '网站描述')
        
        # 添加管理员用户
        if User.query.filter_by(username='admin').first() is None:
            admin = User(
                username='admin',
                email='admin@example.com',
                is_admin=True
            )
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()
            
        print("数据库初始化完成！")

if __name__ == '__main__':
    init_db()