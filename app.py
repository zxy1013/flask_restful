from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from apps.user.model import *
from apps import create_app
from exts import db

app = create_app()
# 使用manager管理
manager = Manager(app=app)
# 绑定db和app
migrate = Migrate(app=app, db=db)
# 绑定db和manager
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
