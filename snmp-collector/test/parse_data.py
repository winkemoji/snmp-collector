import os
import sys
from utils.collection_factory import CollectionFactory, Collection
from utils import load_config_from_file, publish
from utils.dependency_injection import provider
from config.rabbitmq_config import RabbitmqConfig

provider.assemble(RabbitmqConfig)

blueprint = load_config_from_file('./assets/blueprint-template.json')
p_collect = CollectionFactory().use_blueprint(blueprint).construct_collect_data()
p_parse = CollectionFactory().use_blueprint(blueprint).construct_parse_data()
p_collect.daemon = True
p_parse.daemon = True
p_collect.start()
p_parse.start()
while True:
    pass