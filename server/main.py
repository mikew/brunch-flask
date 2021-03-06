# -*- coding:utf-8 -*-

from . import models
import logging
from flask import Flask, render_template, url_for
from flask_cache import Cache
#from flask_gzip import Gzip

# For delayed jobs
#from flask_rq import RQ as RQ
#rq = RQ()

app = None
cache = Cache(with_jinja2_ext=False)
db = models.db


def app_factory(config=None, app_name=None, blueprints=None):
    global app

    app_name = app_name or __name__
    app = Flask(app_name, static_folder='../public/', static_url_path='/static')

    config = config_str_to_obj(config)
    configure_app(app, config)
    configure_database(app)
    configure_extensions(app)
    configure_logger(app, config)
    configure_error_handlers(app)
    configure_context_processors(app)
    configure_template_filters(app)
    configure_before_request(app)
    configure_views(app)
    configure_blueprints(app, blueprints or config.BLUEPRINTS)

    return app


def configure_app(app, config):
    """Loads configuration class into flask app"""
    app.config.from_object(config)
    app.config.from_envvar('APP_CONFIG', silent=True)  # available in the server


def configure_database(app):
    """Database configuration should be set here"""
    db.init_app(app)


def configure_extensions(app):
    """Configure extensions like mail and login here"""
    from .util import SerializedJSON
    app.json_encoder = SerializedJSON
    #Gzip(app)
    cache.init_app(app)
    #rq.init_app(app)


def configure_views(app):
    from . import views  # noqa


def configure_logger(app, config):
    log_filename = config.LOG_FILENAME

    # Create a file logger since we got a logdir
    log_file = logging.FileHandler(filename=log_filename)
    formatter = logging.Formatter(config.LOG_FORMAT)
    log_file.setFormatter(formatter)
    log_file.setLevel(config.LOG_LEVEL)
    app.logger.addHandler(log_file)


def configure_blueprints(app, blueprints):
    """Registers all blueprints set up in config.py"""
    autoload_blueprints(app)

    for blueprint_config in blueprints:
        blueprint, kwargs = None, {}

        if isinstance(blueprint_config, basestring):
            blueprint = blueprint_config
        elif isinstance(blueprint_config, tuple):
            blueprint = blueprint_config[0]
            if isinstance(blueprint_config[1], basestring):
                kwargs = {'url_prefix': blueprint_config[1]}
            else:
                kwargs = blueprint_config[1]
        else:
            print 'Error in BLUEPRINTS setup in config.py'
            print 'Please, verify if each blueprint setup is either a string or a tuple.'
            exit(1)

        blueprint = __import_blueprint(blueprint)
        app.register_blueprint(blueprint, **kwargs)


def autoload_blueprints(app):
    import os
    import importlib
    import warnings

    blueprint_path = os.path.join(app.root_path, 'blueprints')

    for f in os.listdir(blueprint_path):
        if not os.path.isdir(os.path.join(blueprint_path, f)):
            continue

        kwargs = {}
        import_name = '.blueprints.%s' % f
        blueprint = importlib.import_module(import_name, package='server')

        if not hasattr(blueprint, 'app'):
            msg = ('Blueprint "%s" has no app attribute. It will be skipped.'
                   % f)
            warnings.warn(msg, RuntimeWarning)
            continue

        app.register_blueprint(blueprint.app)


def configure_error_handlers(app):
    @app.errorhandler(403)
    def forbidden_page(error):
        """
        The server understood the request, but is refusing to fulfill it.
        Authorization will not help and the request SHOULD NOT be repeated.
        If the request method was not HEAD and the server wishes to make public
        why the request has not been fulfilled, it SHOULD describe the reason for
        the refusal in the entity. If the server does not wish to make this
        information available to the client, the status code 404 (Not Found)
        can be used instead.
        """
        return render_template('access_forbidden.html'), 403

    @app.errorhandler(404)
    def page_not_found(error):
        """
        The server has not found anything matching the Request-URI. No indication
        is given of whether the condition is temporary or permanent. The 410 (Gone)
        status code SHOULD be used if the server knows, through some internally
        configurable mechanism, that an old resource is permanently unavailable
        and has no forwarding address. This status code is commonly used when the
        server does not wish to reveal exactly why the request has been refused,
        or when no other response is applicable.
        """
        return render_template('page_not_found.html'), 404

    @app.errorhandler(405)
    def method_not_allowed_page(error):
        """
        The method specified in the Request-Line is not allowed for the resource
        identified by the Request-URI. The response MUST include an Allow header
        containing a list of valid methods for the requested resource.
        """
        return render_template('method_not_allowed.html'), 405

    @app.errorhandler(500)
    def server_error_page(error):
        return render_template('server_error.html'), 500


def configure_context_processors(app):
    """Modify templates context here"""
    pass


def configure_template_filters(app):
    """Configure filters and tags for jinja"""
    app.jinja_env.globals['static'] = (
        lambda filename: url_for('static', filename=filename))


def configure_before_request(app):
    pass


def config_str_to_obj(cfg):
    from . import config

    if cfg is None:
        if hasattr(config, config.APP_ENV):
            return getattr(config, config.APP_ENV)
        else:
            return getattr(config, config.DEFAULT_ENV)

    return cfg


def __import_blueprint(blueprint_str):
    blueprint_str = 'server.%s' % blueprint_str
    module_path, variable_name = blueprint_str.rsplit('.', 1)
    mod = __import__(module_path, fromlist=[variable_name])
    return getattr(mod, variable_name)
