import os
import sys
# import six


def falcon(body, headers):
    import falcon

    path = '/hello/{account_id}/test'
    falcon_app = falcon.API('text/plain')

    # def ask(req, resp, params):
    #     params['answer'] = 42

    # @falcon.before(ask)
    class HelloResource:
        def on_get(self, req, resp, account_id):
            user_agent = req.user_agent  # NOQA
            limit = req.get_param('limit') or '10'  # NOQA
            resp.data = body
            # if six.PY3:
            #     resp.body = body
            # else:
            #     resp.data = body

            # resp.vary = ['accept-encoding', 'x-auth-token']
            #resp.content_range = (0, 499, 10240)

            resp.set_headers(headers)

    falcon_app.add_route(path, HelloResource())

    return falcon_app


def flask(body, headers):
    import flask

    path = '/hello/<account_id>/test'
    flask_app = flask.Flask('hello')

    @flask_app.route(path)
    def hello(account_id):
        request = flask.request
        user_agent = request.headers['User-Agent']  # NOQA
        limit = request.args.get('limit', '10')  # NOQA

        return flask.Response(body, headers=headers,
                              mimetype='text/plain')

    return flask_app


def bottle(body, headers):
    import bottle
    path = '/hello/<account_id>/test'

    @bottle.route(path)
    def hello(account_id):
        user_agent = bottle.request.headers['User-Agent']  # NOQA
        limit = bottle.request.query.limit or '10'  # NOQA

        return bottle.Response(body, headers=headers)

    return bottle.default_app()


def werkzeug(body, headers):
    import werkzeug.wrappers as werkzeug
    from werkzeug.routing import Map, Rule

    path = '/hello/<account_id>/test'
    url_map = Map([Rule(path, endpoint='hello')])

    @werkzeug.Request.application
    def hello(request):
        user_agent = request.headers['User-Agent']  # NOQA
        limit = request.args.get('limit', '10')  # NOQA
        adapter = url_map.bind_to_environ(request.environ)  # NOQA
        endpoint, values = adapter.match()  # NOQA
        aid = values['account_id']  # NOQA

        return werkzeug.Response(body, headers=headers,
                                 mimetype='text/plain')

    return hello


def cherrypy(body, headers):
    import cherrypy

    # Disable logging
    cherrypy.config.update({'environment': 'embedded'})

    class HelloResource(object):

        exposed = True

        def GET(self, account_id, test, limit=8):
            user_agent = cherrypy.request.headers['User-Agent']  # NOQA
            for name, value in headers.items():
                cherrypy.response.headers[name] = value

            return body

    class Root(object):
        pass

    root = Root()
    root.hello = HelloResource()

    conf = {
        '/': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
        }
    }

    app = cherrypy.tree.mount(root, '/', conf)
    return app


# def wsme(body, headers):
#     import wsme

#     class HelloService(wsme.WSRoot):

#         @wsme.expose(str, str)
#         def hello(self, limit='10'):
#             import pdb
#             pdb.set_trace()
#             return body

#     ws = HelloService(protocols=['restjson'])
#     return ws.wsgiapp()


def pecan(body, headers):
    import falcon.bench.nuts.nuts.app as nuts

    sys.path.append(os.path.dirname(nuts.__file__))
    app = nuts.create()
    del sys.path[-1]

    return app
