from builtins import OSError

import os
from flask import Flask

# Factory Method
from advclick.utils import json_response


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

    # register click blueprint
    from advclick.click import click_api
    app.register_blueprint(click_api.bp)

    # register manager blueprint
    from advclick.manager import manager_api
    app.register_blueprint(manager_api.bp)

    # a simple page that says hello
    @app.route('/')
    def hello():
        return json_response.get_success_msg(
            "Welcome to AdvClick Project.\n\nAll Rights Reserved @AcmeS SwordFish Project 2018.\nMake it Simple & Possible.")

    return app
