from server.main import app, cache
from server.util import Duration, templated


@app.route('/')
@cache.cached(Duration.FOREVER)
@templated('index.html')
def index():
    return {}
