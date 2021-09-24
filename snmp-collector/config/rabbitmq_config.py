from utils.dependency_injection.wiring import register
from utils import load_config_from_file


@register(config_file_path="./assets/config.json")
class RabbitmqConfig(object):
    def __init__(self, config_file_path):
        self._rabbit_config = load_config_from_file(config_file_path)['rabbitmq']

    @property
    def host(self):
        return self._rabbit_config['host']

    @property
    def port(self):
        return self._rabbit_config['port']

    @property
    def username(self):
        return self._rabbit_config['username']

    @property
    def password(self):
        return self._rabbit_config['password']
