from app import create_app, db
from app.models.staff import Staff
from app.models.member import Member, MemberLevel
from app.models.service import SystemService
from app.models.business import ServiceType, Service, ServicePrice, Product, ProductPrice
from app.models.appointment import Appointment
from app.models.delivery import DeliveryOrder, DeliveryItem
from app.models.payment import Payment
from app.models.recharge import Recharge
from app.models.settings import SystemSetting
from app.models.activity_log import ActivityLog
from flask_migrate import Migrate

app = create_app()
migrate = Migrate(app, db)

@app.shell_context_processor
def make_shell_context():
    return dict(
        db=db, 
        Staff=Staff, 
        Member=Member, 
        MemberLevel=MemberLevel,
        SystemService=SystemService,
        ServiceType=ServiceType,
        Service=Service,
        ServicePrice=ServicePrice,
        Product=Product,
        ProductPrice=ProductPrice,
        Appointment=Appointment,
        DeliveryOrder=DeliveryOrder,
        DeliveryItem=DeliveryItem,
        Payment=Payment,
        Recharge=Recharge,
        SystemSetting=SystemSetting,
        ActivityLog=ActivityLog
    )

@app.cli.command()
def init_db():
    """初始化数据库"""
    db.create_all()
    
    # 创建默认管理员账号
    if not Staff.query.filter_by(username='admin').first():
        admin = Staff(
            name='管理员',
            username='admin',
            role='admin',
            is_active=True
        )
        admin.password = 'admin123'
        db.session.add(admin)
    
    # 创建默认会员级别
    if not MemberLevel.query.filter_by(name='普通会员').first():
        level = MemberLevel(
            name='普通会员',
            discount=1.0,
            points_rate=1.0,
            min_points=0,
            description='默认会员级别'
        )
        db.session.add(level)
    
    # 创建默认服务类型
    if not ServiceType.query.filter_by(name='头部按摩').first():
        service_type = ServiceType(
            name='头部按摩',
            description='头部按摩服务',
            icon='fa-spa'
        )
        db.session.add(service_type)
    
    # 创建默认系统设置
    default_settings = {
        'shop_name': '头疗SPA管理系统',
        'shop_phone': '12345678910',
        'shop_address': '示例地址',
        'business_hours': '9:00-21:00',
        'points_rate': '0.01',
        'delivery_fee': '5.0',
        'free_delivery_amount': '50.0',
        'shop_announcement': '欢迎使用头疗SPA管理系统！'
    }
    
    for key, value in default_settings.items():
        if not SystemSetting.query.filter_by(key=key).first():
            setting = SystemSetting(key=key, value=value)
            db.session.add(setting)
    
    db.session.commit()
    print('数据库初始化完成！')

if __name__ == '__main__':
    app.run(debug=True)