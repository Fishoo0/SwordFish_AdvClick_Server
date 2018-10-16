from builtins import OSError

import os
from flask import Flask


# Factory Method



def create_app(test_config=None):
    # create and configure the account
    app = Flask(__name__, instance_relative_config=True)

    # print the path message
    print('instance_path -> ' + app.instance_path)

    # sets some default configuration that the account will use
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'advclick.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # init the database
    from advclick.db import db
    db.init_app(app)

    # register auth blueprint
    from advclick.account import auth_api
    app.register_blueprint(auth_api.bp)

    # register home blueprint
    from advclick.home import home_api
    app.register_blueprint(home_api.bp)

    #lls

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World! I am flask1.0.2 in pip3 !!!'

    return app
