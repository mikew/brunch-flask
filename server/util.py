from flask import Response, json, render_template, request
from functools import wraps


class Duration(object):
    # Cache times
    MINUTE = 60
    HOUR = 60 * MINUTE
    DAY = 24 * HOUR
    WEEK = 7 * DAY
    MONTH = 30 * DAY
    YEAR = 365 * DAY

    SHORT = 15 * MINUTE
    LONG = HOUR
    FOREVER = DAY


class SerializedJSON(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj, 'serialized'):
            return obj.serialized

        return super(SerializedJSON, self).default(obj)


def is_ajax(req):
    return req.is_xhr


def templated(template=None):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            template_name = template
            if template_name is None:
                template_name = request.endpoint.replace('.', '/') + '.html'

            ctx = f(*args, **kwargs)
            if ctx is None:
                ctx = {}
            elif not isinstance(ctx, dict):
                return ctx

            return render_template(template_name, **ctx)
        return decorated_function
    return decorator


def template_or_json(template=None):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            template_name = template
            if template_name is None:
                template_name = request.endpoint.replace('.', '/') + '.html'

            ctx = f(*args, **kwargs)
            if ctx is None:
                ctx = {}
            elif not isinstance(ctx, dict):
                return ctx

            if is_ajax(request):
                return jsonify(ctx)

            return render_template(template_name, **ctx)
        return decorated_function
    return decorator


def jsonify(obj):
    dumped = json.dumps(obj, separators=(',', ':'))
    return Response(dumped, mimetype='application/json')


def json_response(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        ctx = f(*args, **kwargs)
        return jsonify(ctx)

    return decorated_function
