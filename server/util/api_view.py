from .view_decorators import jsonify, normalize_response
from server import db

from flask.views import MethodView
from flask import current_app, g, request, Response, url_for


class ResourceMixin(object):
    paginate_by = 0
    page_arg = 'page'

    def get_collection(self):
        base_q = self.model.query

        should_filter = request.args.get('filter', False)
        if should_filter:
            base_q = self.filter_query(base_q)

        if self.paginate_by:
            page_num = int(request.args.get(self.page_arg, 1))
            return base_q.paginate(page_num, self.paginate_by)

        return base_q.all()

    def filter_query(self, q):
        return q.filter(**request.args.to_dict())

    def get_resource(self, pk):
        return self.model.query.get_or_404(pk)

    def create_resource(self):
        resource = self.model()
        resource, errors = self.set_attributes(resource)

        if errors['errors']:
            return errors, 400

        db.session.add(resource)
        db.session.commit()
        return resource

    def update_resource(self, pk):
        # This might be more efficient in the long run,
        # though getting something to return would still be and extra
        # query, and we'd lose the abort(404)
        #self.model.query.filter_by(id=pk).update(**request.get_json())

        resource = self.get_resource(pk)
        resource, errors = self.set_attributes(resource)

        if errors['errors']:
            return errors, 400

        db.session.commit()
        return resource

    def delete_resource(self, pk):
        # Again, this would probably be more efficient, but yadda yadda.
        #self.model.query.filter_by(id=pk).delete()

        resource = self.get_resource(pk)
        db.session.delete(resource)
        db.session.commit()
        return {'message': 'ok'}

    def set_attributes(self, resource):
        errors = {'errors': {}}
        data = request.get_json()

        if data is None:
            data = request.form.to_dict()

        for column in resource.__table__.columns:
            cname = column.name
            if cname in data:
                try:
                    setattr(resource, cname, data[cname])
                except Exception, e:
                    msg = str(e[0])
                    if cname in errors['errors']:
                        errors['errors'][cname].append(msg)
                    else:
                        errors['errors'][cname] = [msg]

        return resource, errors


class ApiView(ResourceMixin, MethodView):
    @classmethod
    def register_with(cls, app, endpoint, url, pk='pk', pk_type='int'):
        register_api(app, cls, endpoint, url, pk, pk_type)

    def dispatch_request(self, *args, **kwargs):
        from_form = request.form.get('_method', None)

        if from_form:
            request_method = from_form
        else:
            request_method = request.method

        meth = getattr(self, request_method.lower(), None)
        if meth is None and request.method == 'HEAD':
            meth = getattr(self, 'get', None)
        assert meth is not None, 'Unimplemented method %r' % request.method

        # If the response is already a Response class, do nothing
        result = meth(*args, **kwargs)
        resp, status, headers = normalize_response(result)
        if isinstance(resp, Response):
            return resp, status, headers

        return jsonify(resp), status, headers

    @property
    def request(self):
        return request

    @property
    def g(self):
        return g

    @property
    def logger(self):
        return current_app.logger

    def get(self, pk):
        if pk is None:
            return self.index()

        return self.show(pk)

    def index(self):
        return self.get_collection()

    def post(self):
        return self.create_resource()

    def put(self, pk):
        return self.update_resource(pk)

    def show(self, pk):
        return self.get_resource(pk)

    def delete(self, pk):
        return self.delete_resource(pk)

    def url_for(self, endpoint, **kwargs):
        return url_for(endpoint, **kwargs)


def register_api(app, view, endpoint, url, pk='pk', pk_type='int'):
    view_func = view.as_view(endpoint)
    app.add_url_rule(url, defaults={pk: None},
                     view_func=view_func, methods=['GET'])
    app.add_url_rule(url, view_func=view_func, methods=['POST'])
    app.add_url_rule('%s/<%s:%s>' % (url, pk_type, pk), view_func=view_func,
                     methods=['GET', 'PUT', 'DELETE'])
