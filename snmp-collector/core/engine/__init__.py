import traceback

from core.api_server import api_server
from gevent.pywsgi import WSGIServer
from core.service import CollectionService


def engine_builder(flask_config):
    return Builder(flask_config)


class Builder(object):
    def __init__(self, flask_config):
        self._flask_config = flask_config
        pass

    def build(self):
        return Engine(self._flask_config)


class Engine(object):
    def __init__(self, flask_config):
        self._flask_config = flask_config

    def run(self):
        CollectionService.clear_all()
        api_server.run(host=self._flask_config.host, port=self._flask_config.port)

