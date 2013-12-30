from server.main import app
from server.util import Duration, route


@route(app, '/', ttl=Duration.FOREVER, template='index.html')
def index():
    return {}
