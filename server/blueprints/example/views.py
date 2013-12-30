from flask import Blueprint
from server.util import Duration, route

app = Blueprint('blueprint_scaffold', __name__, url_prefix='/example')


@route(app, '/', json=True)
def wut():
    return 42
