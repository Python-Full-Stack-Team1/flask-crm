from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from api import create_app, db
from api.models import UserInfo, UserLogin

app = create_app('development')
manager = Manager(app)
Migrate(app, db)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
