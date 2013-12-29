#!/usr/bin/env python

from flask.ext.script import Command, Manager

from server import app_factory, cache, db, models
manager = Manager(app_factory)


@manager.command
def db_create():
    """Creates database using SQLAlchemy"""
    db.create_all()


@manager.command
def db_drop():
    """Drops database using SQLAlchemy"""
    db.drop_all()


@manager.shell
def make_shell_context():
    from server.main import app
    return dict(app=app, db=db, models=models, cache=cache)


if __name__ == "__main__":
    manager.run()
