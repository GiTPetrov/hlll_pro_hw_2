from flask import Flask
import os
from flsk_srv.db import get_db


def create_app(test_config=None):
    # create and configure the app
    flsk_app = Flask(__name__, instance_relative_config=True)
    flsk_app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(flsk_app.instance_path, 'flsk_srv.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        flsk_app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        flsk_app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(flsk_app.instance_path)
    except OSError:
        pass

    from . import db
    db.init_app(flsk_app)

    from . import hw_2
    flsk_app.register_blueprint(hw_2.bp)
    flsk_app.add_url_rule('/', endpoint='index')

    from . import hw_3
    flsk_app.register_blueprint(hw_3.bp)
    flsk_app.add_url_rule('/', endpoint='index')

    return flsk_app
