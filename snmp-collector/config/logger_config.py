from utils import load_config_from_file
from utils.dependency_injection.wiring import register


@register(config_file_path="./assets/config.json")
class LoggerConfig(object):
    def __init__(self, config_file_path):
        self._logger_config = load_config_from_file(config_file_path)['logger']

    @property
    def debug(self):
        return self._logger_config['debug']

    @property
    def file_path(self):
        return self._logger_config['file_path']
