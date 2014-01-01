from server.main import cache
from .view_decorators import (json_response,
                              template_or_json as template_or_json_,
                              templated)


def route(app, route, ttl=0, json=False, template=False,
          template_or_json=False, cache_kwargs={}, **kwargs):
    def decorator(f):
        if json or template or template_or_json:
            _integrity_check(json, template, template_or_json)

        if json is not False:
            f = json_response(f)

        if template is not False:
            f = templated(template)(f)

        if template_or_json is not False:
            f = template_or_json_(template)(f)

        if ttl:
            f = cache.cached(ttl, **cache_kwargs)(f)

        return app.route(route, **kwargs)(f)
    return decorator


def _integrity_check(json, template, template_or_json):
    _json = json
    _template = template
    _template_or_json = template_or_json

    # template / template_or_json can be None when the template name is to be
    # inferred
    if _template is None:
        _template = True
    if _template_or_json is None:
        _template_or_json = True

    overlap = filter(bool, [_json, _template, _template_or_json])
    if len(overlap) > 1:
        msg = 'Use one of `json`, `template` or `template_or_json`'
        raise Exception(msg)
