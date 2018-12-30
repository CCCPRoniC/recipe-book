# -*- coding: utf-8 -*-
"""The app module, containing the app factory function."""
import logging
import sys
import commands
from flask import Flask
from flask_security import SQLAlchemyUserDatastore
from extensions import db, bcrypt, debug_toolbar, bootstrap, nav, security
from models import Role, User
from home.views import home
from recipes.views import recipe
from users.views import user
from config import ProdConfig

DEFAULT_BLUEPRINTS = (
    home,
    recipe,
    user
)


def app_factory(config_object=ProdConfig, blueprints=DEFAULT_BLUEPRINTS):
    """An application factory, that creates a new Flask app.
    More information can be found here: http://flask.pocoo.org/docs/patterns/appfactories/.
    :param config_object: The configuration object to use.
    """
    app = Flask(
        __name__.split('.')[0],
        static_folder=config_object.STATIC_DIR,
        template_folder=config_object.TEMPLATE_DIR
    )
    configure_app(app, config_object)
    register_extensions(app)
    register_blueprints(app, blueprints)
    register_hooks(app)
    configure_logging(app)
    register_shellcontext(app)
    register_commands(app)
    return app


def configure_app(app, config):
    """Configure app."""
    app.config.from_object(config)


def register_extensions(app):
    """Register Flask extensions.
    :app: The Flask app.
    """
    db.init_app(app)
    bcrypt.init_app(app)
    user_datastore = SQLAlchemyUserDatastore(db, User, Role)
    security.init_app(app, user_datastore)
    bootstrap.init_app(app)
    nav.init_app(app)
    debug_toolbar.init_app(app)


def register_blueprints(app, blueprints):
    """Register Flask blueprints."""
    for blueprint in blueprints:
        app.register_blueprint(blueprint)


def register_hooks(app):
    """Configure hook."""
    @app.before_first_request
    def before_request():
        db.create_all()
        if not Role.get_role("chef"):
            db.session.add(Role(name='chef', description='Chef in the kitchen.'))
        if not Role.get_role("guest"):
            db.session.add(Role(name='guest', description='Visitor.'))
        db.session.commit()
        print("Successfully generated user roles")


def register_shellcontext(app):
    """Register shell context objects."""
    def shell_context():
        """Shell context objects."""
        return {'db': db}
    app.shell_context_processor(shell_context)


def configure_logging(app):
    """Configure logging."""
    loggers = [app.logger]
    stream_handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    stream_handler.setFormatter(formatter)
    for logger in loggers:
        logger.setLevel(app.config['LOG_LEVEL'])
        logger.addHandler(stream_handler)


def register_commands(app):
    """Register Click commands."""
    app.cli.add_command(commands.clean)
    app.cli.add_command(commands.lint)
    app.cli.add_command(commands.urls)
    app.cli.add_command(commands.make_users)
