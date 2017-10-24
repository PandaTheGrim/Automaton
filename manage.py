#!/usr/bin/env python
import os
from flask_script import Manager

from app import create_app

from app.database import db

from flask_migrate import Migrate, MigrateCommand

app = create_app()
app.config.from_object('config.DevelopmentConfig')

manager = Manager(app)
migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
