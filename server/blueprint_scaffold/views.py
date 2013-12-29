from flask import Blueprint
from server.util import json_response

app = Blueprint('blueprint_scaffold', __name__, template_folder='templates')


@app.route('/')
@json_response
def wut():
    return 42
