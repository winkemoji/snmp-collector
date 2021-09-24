from utils.dependency_injection.wiring import register
from utils import load_config_from_file


@register(config_file_path="./assets/blueprints.json")
class Collections(object):
    def __init__(self, config_file_path):
        self._collection = iter(load_config_from_file(config_file_path)['blueprints'])

    def next_collection(self):
        c = next(self._collection)
        collection = Collection()
        collection.id = c['id']
        m = c["modules"]
        collection.collect_data_module = collection.CollectDataModule(m['collect_data']['routing_keys'],
                                                                      m['collect_data']['publish_keys'])
        collection.parse_data_module = collection.ParseDataModule(m['parse_data']['routing_keys'],
                                                                  m['parse_data']['publish_keys'])
        collection.save_data_module = collection.SaveDataModule(m['save_data']['routing_keys'],
                                                                m['save_data']['publish_keys'])

        return collection


class Collection(object):
    def __init__(self):
        self.id = None
        self.collect_data_module = None
        self.parse_data_module = None
        self.save_data_module = None

    class CollectDataModule:
        def __init__(self, routing_keys, publish_keys):
            self.routing_keys = routing_keys
            self.publish_keys = publish_keys

    class ParseDataModule:
        def __init__(self, routing_keys, publish_keys):
            self.routing_keys = routing_keys
            self.publish_keys = publish_keys

    class SaveDataModule:
        def __init__(self, routing_keys, publish_keys):
            self.routing_keys = routing_keys
            self.publish_keys = publish_keys
