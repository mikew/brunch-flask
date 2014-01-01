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


@manager.command
def routes():
    from server.main import app
    from flask import url_for
    import urllib

    output = []
    for rule in app.url_map.iter_rules():

        options = {}
        for arg in rule.arguments:
            options[arg] = "[{0}]".format(arg)

        methods = ','.join(rule.methods)
        try:
            url = url_for(rule.endpoint, **options)
        except:
            url = str(rule)
        line = urllib.unquote("{:50s} {:20s} {}"
                              .format(rule.endpoint, methods, url))
        output.append(line)

    for line in sorted(output):
        print line


if __name__ == "__main__":
    manager.run()
