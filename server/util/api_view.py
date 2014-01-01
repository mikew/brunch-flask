from .view_decorators import jsonify
from flask.views import MethodView
from flask import request, Response, url_for as url_for


class ApiView(MethodView):
    def dispatch_request(self, *args, **kwargs):
        # Taken from flask/views.py
        meth = getattr(self, request.method.lower(), None)
        if meth is None and request.method == 'HEAD':
            meth = getattr(self, 'get', None)
        assert meth is not None, 'Unimplemented method %r' % request.method

        # If the response is already a Response class, do nothing
        resp = meth(*args, **kwargs)
        if isinstance(resp, Response):
            return resp

        return jsonify(resp)

    def get(self, pk):
        if pk is None:
            return self.index()

        return self.show(pk)

    def index(self):
        pass

    def post(self):
        pass

    def show(self, pk):
        pass

    def delete(self, pk):
        pass

    def put(self, pk):
        pass

    def url_for(self, endpoint, **kwargs):
        return url_for(endpoint, **kwargs)


def register_api(app, view, endpoint, url, pk='pk', pk_type='int'):
    view_func = view.as_view(endpoint)
    app.add_url_rule(url, defaults={pk: None},
                     view_func=view_func, methods=['GET'])
    app.add_url_rule(url, view_func=view_func, methods=['POST'])
    app.add_url_rule('%s/<%s:%s>' % (url, pk_type, pk), view_func=view_func,
                     methods=['GET', 'PUT', 'DELETE'])
