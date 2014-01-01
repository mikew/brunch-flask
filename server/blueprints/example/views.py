from flask import Blueprint
from server.util import Duration, route

app = Blueprint('example', __name__, url_prefix='/example')


@route(app, '/', json=True)
def wut():
    return 42
