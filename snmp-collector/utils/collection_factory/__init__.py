from utils.dependency_injection.wiring import provide
from config.rabbitmq_config import RabbitmqConfig
from utils.module_builder import CollectDataModuleBuilder, ParseDataModuleBuilder, SaveDataModuleBuilder
from multiprocessing import Process
import json


class Collection(object):
    def __init__(self):
        self.unique_name = None
        self.collect_data_module = None
        self.parse_data_module = None
        self.save_data_module = None

    class CollectDataModule:
        def __init__(self, routing_keys, binding_key, custom_variables):
            self.routing_keys = routing_keys
            self.binding_key = binding_key
            self.custom_variables = custom_variables

    class ParseDataModule:
        def __init__(self, routing_keys, binding_key, custom_variables):
            self.routing_keys = routing_keys
            self.binding_key = binding_key
            self.custom_variables = custom_variables

    class SaveDataModule:
        def __init__(self, routing_keys, binding_key, custom_variables):
            self.routing_keys = routing_keys
            self.binding_key = binding_key
            self.custom_variables = custom_variables


class CollectionFactory(object):
    def __init__(self, collect_data_builder=CollectDataModuleBuilder(), parse_data_builder=ParseDataModuleBuilder(),
                 save_data_builder=SaveDataModuleBuilder()):
        self.collect_data_builder = collect_data_builder
        self.parse_data_builder = parse_data_builder
        self.save_data_builder = save_data_builder

        self._collection = None

    def use(self, collection):
        self._collection = collection
        return self

    def get_collection(self):
        return self._collection

    def use_blueprint(self, blueprint):
        c = Collection()
        c.unique_name = blueprint['unique_name']
        m = blueprint['modules']
        c.collect_data_module = c.CollectDataModule(m['collect_data']['routing_keys'],
                                                    m['collect_data']['binding_key'],
                                                    m['collect_data'])
        c.parse_data_module = c.ParseDataModule(m['parse_data']['routing_keys'],
                                                m['parse_data']['binding_key'],
                                                m['parse_data'])
        c.save_data_module = c.SaveDataModule(m['save_data']['routing_keys'],
                                              m['save_data']['binding_key'],
                                              m['save_data'])

        self._collection = c
        return self

    def construct(self):
        p_collect = self.construct_collect_data()
        p_parse = self.construct_parse_data()
        p_save = self.construct_save_data()
        return [p_collect, p_parse, p_save]

    def construct_collect_data(self):
        c = self._collection
        cd = c.collect_data_module
        collect_data_module = self.collect_data_builder.set_mq_config(provide(RabbitmqConfig)).set_exchange(
            c.unique_name). \
            set_routing_keys(cd.routing_keys). \
            set_binding_key(cd.binding_key).set_custom_variables(cd.custom_variables).build()
        p_collect = Process(target=collect_data_module.run, name='%s.collect_data_module' % c.unique_name)
        return p_collect

    def construct_parse_data(self):
        c = self._collection
        pd = c.parse_data_module
        parse_data_module = self.parse_data_builder.set_mq_config(provide(RabbitmqConfig)).set_exchange(c.unique_name). \
            set_routing_keys(pd.routing_keys). \
            set_binding_key(pd.binding_key).set_custom_variables(pd.custom_variables).build()
        p_parse = Process(target=parse_data_module.run, name='%s.parse_data_module' % c.unique_name)
        return p_parse

    def construct_save_data(self):
        c = self._collection
        sd = c.save_data_module
        save_data_module = self.save_data_builder.set_mq_config(provide(RabbitmqConfig)).set_exchange(c.unique_name). \
            set_routing_keys(sd.routing_keys). \
            set_binding_key(sd.binding_key).set_custom_variables(sd.custom_variables).build()
        p_save = Process(target=save_data_module.run, name='%s.save_data_module' % c.unique_name)
        return p_save
