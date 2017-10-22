import os
from flask import Flask
from .database import db

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.DevelopmentConfig')

    db.init_app(app)
    with app.test_request_context():
        db.create_all()

    import app.auth.controllers as auth
    import app.dashboard.controllers as dashboard
    import app.api.controllers as api
    import app.releases.controllers as releases
    import app.testplans.controllers as testplans
    import app.testcases.controllers as testcases
    import app.documentation.controllers as docs

    app.register_blueprint(auth.module)
    app.register_blueprint(dashboard.module)
    app.register_blueprint(api.module)
    app.register_blueprint(releases.module)
    app.register_blueprint(testcases.module)
    app.register_blueprint(testplans.module)
    app.register_blueprint(docs.module)

    return app