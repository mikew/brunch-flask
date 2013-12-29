from server.main import app, cache
from server.util import Duration, json_response, template_or_json


class Struct(object):
    def __init__(self, *args, **kwargs):
        for k, v in kwargs.iteritems():
            setattr(self, k, v)

    @property
    def serialized(self):
        return vars(self)


@app.route('/')
@cache.cached(Duration.FOREVER)
@json_response
def hello():
    return ['hello world']


@app.route('/template')
@cache.cached(Duration.FOREVER)
@template_or_json()
def hello2():
    foo = dict(foo='bar')
    return foo
