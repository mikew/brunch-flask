from .duration import Duration  # noqa
from .view_decorators import (SerializedJSON, is_ajax, jsonify,  # noqa
                              templated, template_or_json, json_response)
from .route_scaffold import route  # noqa
from .api_view import ApiView, register_api  # noqa
from server import cache
cached = cache.cached
del cache
