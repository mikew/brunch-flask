#!/usr/bin/env python

from flask_script import Server, Manager

from server import app_factory, cache, db, models
manager = Manager(app_factory)

manager.add_command("runserver", Server(host='0.0.0.0'))

from server.managers.db import manager as db_manager
manager.add_command('db', db_manager)


@manager.shell
def make_shell_context():
    from server.main import app
    return dict(app=app, db=db, models=models, cache=cache)


@manager.command
def clear_cache():
    cache.clear()


if __name__ == "__main__":
    manager.run()
