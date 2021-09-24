from utils.dependency_injection.wiring import register
from utils import load_config_from_file


@register(config_file_path="./assets/config.json")
class ApiServerConfig(object):
    def __init__(self, config_file_path):
        self._flask_config = load_config_from_file(config_file_path)['api_server']

    @property
    def host(self):
        return self._flask_config['host']

    @property
    def port(self):
        return self._flask_config['port']
