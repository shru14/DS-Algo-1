from flask import Flask
from .extensions import db

#Creating database instance
def create_app(config_filename='config.py'):
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_pyfile(config_filename)
    app.config.from_pyfile('instance/config.py', silent=True)

    db.init_app(app)

    with app.app_context():
        from . import routes, models
        if app.config.get('INIT_DB', False):
            db.create_all()
            from .init_scenario import init_configurations 
            init_configurations()

    return app