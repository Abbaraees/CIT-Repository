import os

from flask import Flask

from .models import init_app


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_mapping({
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///'+os.path.join(app.instance_path, 'data.sqlite'),
        'SECRET_KEY': 'dev'
    })

    if test_config:
        app.config.from_mapping(test_config)
    else:
        app.config.from_pyfile('config.py', silent=True)

    # Ensure that the instance path exists
    try:
        os.mkdir(app.instance_path)
    except OSError:
        pass

    @app.route('/hello')
    def hello():
        return 'Hello'

    init_app(app)

    return app
