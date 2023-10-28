from flask import Flask
from flask_restful import Api

from app.ext import migrate, ma
from app.db import db

from flask_cors import CORS

cors = CORS()

import os, logging

def create_app(settings_module):
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_object(settings_module)

    if app.config.get("TESTING", False):
        app.config.from_pyfile("config-testing.py", silent=True)
    else:
        app.config.from_pyfile("config.py", silent=True)

    # init apps
    db.init_app(app)
    ma.init_app(app)
    migrate.init_app(app, db)

    cors.init_app(app, supports_credentials=True, origins=["*"])

    Api(app)

    # blueprints
    from app.kitchen.api_v1_0 import kitchen_bp
    from app.rol.api_v1_0 import rol_bp
    from app.users.api_v1_0 import users_bp

    app.register_blueprint(kitchen_bp, url_prefix="/api/v1.0")
    app.register_blueprint(rol_bp, url_prefix="/api/v1.0")
    app.register_blueprint(users_bp, url_prefix="/api/v1.0")

    configure_logging(app)

    return app

def configure_logging(app):
    del app.logger.handlers[:]

    loggers = [app.logger,]
    handlers = []


    console_handler = logging.StreamHandler()
    console_handler.setFormatter(verbose_formatter())

    # if (app.config['APP_ENV'] == app.config['APP_ENV_TESTING']) or (
    #         app.config['APP_ENV'] == app.config['APP_ENV_DEVELOPMENT']):
    #     console_handler.setLevel(logging.DEBUG)
    #     handlers.append(console_handler)
    # elif app.config['APP_ENV'] == app.config['APP_ENV_PRODUCTION']:
    #     console_handler.setLevel(logging.INFO)
    #     handlers.append(console_handler)

    #     # mail_handler = SMTPHandler((app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
    #     #                            app.config['DONT_REPLY_FROM_EMAIL'],
    #     #                            app.config['ADMINS'],
    #     #                            '[Error][{}] La aplicación falló'.format(app.config['APP_ENV']),
    #     #                            (app.config['MAIL_USERNAME'],
    #     #                             app.config['MAIL_PASSWORD']),
    #     #                            ())
    #     # mail_handler.setLevel(logging.ERROR)
    #     # mail_handler.setFormatter(mail_handler_formatter())
    #     # handlers.append(mail_handler)

    for l in loggers:
        for handler in handlers:
            l.addHandler(handler)
        l.propagate = False
        l.setLevel(logging.DEBUG)

def verbose_formatter():
    return logging.Formatter(
        "[%(asctime)s.%(msecs)d]\t %(levelname)s \t[%(name)s.%(funcName)s:%(lineno)d]\t %(message)s",
        datefmt="%d/%m/%Y %H:%M:%S",
    )

def mail_handler_formatter():
    return logging.Formatter(
        '''
            Message type:       %(levelname)s
            Location:           %(pathname)s:%(lineno)d
            Module:             %(module)s
            Function:           %(funcName)s
            Time:               %(asctime)s.%(msecs)d

            Message:

            %(message)s
        ''',
        datefmt='%d/%m/%Y %H:%M:%S'
    )

