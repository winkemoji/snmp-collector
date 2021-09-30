import traceback

from core.api_server import api_server
from gevent.pywsgi import WSGIServer
from core.service import CollectionService
# from utils.dependency_injection.wiring import provide
# from config.collections_snapshot import CollectionsSnapshot


def engine_builder(flask_config):
    return Builder(flask_config)


class Builder(object):
    def __init__(self, flask_config):
        self._flask_config = flask_config

    def build(self):
        return Engine(self._flask_config)


class Engine(object):
    def __init__(self, flask_config):
        self._flask_config = flask_config

    def run(self):
        CollectionService.clear_all()
        # for debug
        # api_server.run(host=self._flask_config.host, port=self._flask_config.port)
        server = WSGIServer((self._flask_config.host,int(self._flask_config.port)),api_server)
        server.serve_forever()

