from flask import Blueprint
from server.util import json_response

app = Blueprint('blueprint_scaffold', __name__, url_prefix='/example')


@app.route('/')
@json_response
def wut():
    return 42
