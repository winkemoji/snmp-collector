from utils.dependency_injection.wiring import register
from utils import load_config_from_file


@register(config_file_path="./assets/config.json")
class SqliteConfig(object):
    def __init__(self, config_file_path):
        self._rabbit_config = load_config_from_file(config_file_path)['sqlite']

    @property
    def file_path(self):
        return self._rabbit_config['file_path']
