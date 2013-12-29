import os
from server import app_factory, db, config

import unittest
from nose.tools import eq_, ok_


def relative_path(*parts):
    dirname, realpath, join_path = (os.path.dirname,
                                    os.path.realpath,
                                    os.path.join)

    cwd = dirname(realpath(__file__))
    return realpath(join_path(cwd, '..', *parts))


def read_file(*parts):
    """Easily read a file in the tests/ directory."""
    parts = ('tests',) + parts
    f = open(relative_path(*parts))
    data = f.read()
    f.close()

    return data


class TestCase(unittest.TestCase):
    def setUp(self):
        app = app_factory(config.test)
        app.test_request_context().push()
        self.app = app
        self.client = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
