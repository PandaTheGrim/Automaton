import os
from flask import Flask
# from .database import db

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.DevelopmentConfig')

    # db.init_app(app)
    # with app.test_request_context():
      #   db.create_all()

    # import app.auth.controllers as auth
    import app.dashboard.controllers as dashboard

   # app.register_blueprint(auth.module)
    app.register_blueprint(dashboard.module)

    return app