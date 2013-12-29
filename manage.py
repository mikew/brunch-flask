#!/usr/bin/env python

from flask_script import Manager

from server import app_factory, cache, db, models
manager = Manager(app_factory)

from server.managers.db import manager as db_manager
manager.add_command('db', db_manager)


@manager.shell
def make_shell_context():
    from server.main import app
    return dict(app=app, db=db, models=models, cache=cache)


if __name__ == "__main__":
    manager.run()
