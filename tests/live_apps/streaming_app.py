from werkzeug.wrappers import Request
from werkzeug.wrappers import Response


@Request.application
def app(request):
    def g():
        for x in range(5):
            yield "%d\n" % x

        if request.path == "/crash":
            raise Exception("crash requested")

    return Response(g())
