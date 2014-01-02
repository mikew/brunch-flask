from server import db
from flask import Response, json, render_template, request
from functools import wraps
from flask_sqlalchemy import Pagination


class SerializedJSON(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj, 'serialized'):
            return obj.serialized

        if isinstance(obj, db.Model):
            return self.encode_model(obj)

        if isinstance(obj, Pagination):
            return self.encode_pagination(obj)

        return super(SerializedJSON, self).default(obj)

    def encode_model(self, model):
        data = {}
        exclude = ()
        extra = ()
        only = ()

        if hasattr(model, '__exclude__') and model.__exclude__:
            exclude = model.__exclude__

        if hasattr(model, '__extra__') and model.__extra__:
            extra = model.__extra__

        if hasattr(model, '__only__') and model.__only__:
            only = model.__only__

        if not only:
            for column in model.__table__.columns:
                cname = column.name
                if cname in exclude:
                    continue

                data[cname] = getattr(model, cname)

        for cname in extra + only:
            if hasattr(model, cname):
                result = getattr(model, cname)
                if callable(result):
                    data[cname] = result()
                else:
                    data[cname] = result

        return data

    def encode_pagination(self, obj):
        # Maybe return something more verbose here
        #data = {
            #'pages': obj.pages,
            #'items': obj.items
        #}

        #if obj.has_prev:
            #data['previous'] = obj.prev_num
        #if obj.has_next:
            #data['next'] = obj.next_num

        #return data

        return obj.items


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
