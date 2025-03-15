from app import db
from datetime import datetime

class ServiceType(db.Model):
    """服务类型模型"""
    __tablename__ = 'service_types'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, index=True)
    description = db.Column(db.String(256))
    icon = db.Column(db.String(64))  # 图标名称，如 'fa-spa'

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)  # 添加这一行
    services = db.relationship('Service', backref='type', lazy='dynamic')
    
    def __repr__(self):
        return f'<ServiceType {self.name}>'

class Service(db.Model):
    """服务项目模型"""
    __tablename__ = 'services'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, index=True)
    description = db.Column(db.Text)
    duration = db.Column(db.Integer)  # 服务时长（分钟）
    type_id = db.Column(db.Integer, db.ForeignKey('service_types.id'))
    image = db.Column(db.String(256))  # 服务图片路径
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    prices = db.relationship('ServicePrice', backref='service', lazy='dynamic')
    
    def __repr__(self):
        return f'<Service {self.name}>'
    
    def current_price(self):
        """获取当前价格"""
        return ServicePrice.query.filter_by(service_id=self.id).order_by(ServicePrice.created_at.desc()).first()

class ServicePrice(db.Model):
    """服务价格模型（保留历史价格）"""
    __tablename__ = 'service_prices'
    
    id = db.Column(db.Integer, primary_key=True)
    service_id = db.Column(db.Integer, db.ForeignKey('services.id'))
    price = db.Column(db.Float)
    member_price = db.Column(db.Float)  # 会员价格
    effective_date = db.Column(db.DateTime, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<ServicePrice {self.service_id} {self.price}>'

class Product(db.Model):
    """产品模型"""
    __tablename__ = 'products'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, index=True)
    description = db.Column(db.Text)
    sku = db.Column(db.String(64), unique=True)  # 产品编码
    image = db.Column(db.String(256))  # 产品图片路径
    stock = db.Column(db.Integer, default=0)  # 库存
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    prices = db.relationship('ProductPrice', backref='product', lazy='dynamic')
    
    def __repr__(self):
        return f'<Product {self.name}>'
    
    def current_price(self):
        """获取当前价格"""
        return ProductPrice.query.filter_by(product_id=self.id).order_by(ProductPrice.created_at.desc()).first()

class ProductPrice(db.Model):
    """产品价格模型（保留历史价格）"""
    __tablename__ = 'product_prices'
    
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))
    price = db.Column(db.Float)
    member_price = db.Column(db.Float)  # 会员价格
    effective_date = db.Column(db.DateTime, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<ProductPrice {self.product_id} {self.price}>'