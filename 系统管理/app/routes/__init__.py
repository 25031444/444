from flask import Blueprint

# 导入所有蓝图
from .auth import auth_bp
from .dashboard import dashboard_bp
from .member import member_bp
from .service import service_bp
from .product import product_bp
from .appointment import appointment_bp
from .delivery import delivery_bp
from .payment import payment_bp
from .recharge import recharge_bp
from .staff import staff_bp
from .settings import settings_bp

# 创建一个函数来注册所有蓝图
def register_blueprints(app):
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(member_bp, url_prefix='/members')
    app.register_blueprint(service_bp, url_prefix='/services')
    app.register_blueprint(product_bp, url_prefix='/products')
    app.register_blueprint(appointment_bp, url_prefix='/appointments')
    app.register_blueprint(delivery_bp, url_prefix='/delivery')
    app.register_blueprint(payment_bp, url_prefix='/payments')
    app.register_blueprint(recharge_bp, url_prefix='/recharges')
    app.register_blueprint(staff_bp, url_prefix='/staff')
    app.register_blueprint(settings_bp, url_prefix='/settings')