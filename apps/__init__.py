from flask import Flask
from apps.user.view import user_bp
from exts import db, api
from settings import DevelopmentConfig

def create_app():
    app = Flask(__name__)
    # 加载配置文件
    app.config.from_object(DevelopmentConfig)
    # 初始化创建
    db.init_app(app=app)
    api.init_app(app=app)
    # 注册蓝图
    app.register_blueprint(user_bp)
    print(app.url_map)
    return app