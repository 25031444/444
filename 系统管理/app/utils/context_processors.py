from app.models.settings import Settings

def inject_settings():
    """向所有模板注入设置变量"""
    settings = Settings.get_all_settings()
    return dict(settings=settings)