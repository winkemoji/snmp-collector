from abc import ABC

from utils.module_builder.builder_base import ModuleBuilderBase
from modules.collect_data import CollectDataModule
from modules.parse_data import ParseDataModule
from modules.save_data import SaveDataModule


class CollectDataModuleBuilder(ModuleBuilderBase, ABC):
    def __init__(self):
        super(CollectDataModuleBuilder, self).__init__()
        self._module = CollectDataModule()

    def build(self):
        self._module.set_mq_config(self._mq_config)
        self._module.set_exchange(self._exchange)
        self._module.set_id("{}.collect_data".format(self._exchange))
        self._module.set_routing_keys(self._routing_keys)
        self._module.set_binding_key(self._binding_key)
        self._module.set_custom_variables(self._custom_variables)
        return self._module


class ParseDataModuleBuilder(ModuleBuilderBase, ABC):
    def __init__(self):
        super(ParseDataModuleBuilder, self).__init__()
        self._module = ParseDataModule()

    def build(self):
        self._module.set_mq_config(self._mq_config)
        self._module.set_exchange(self._exchange)
        self._module.set_id("{}.parse_data".format(self._exchange))
        self._module.set_routing_keys(self._routing_keys)
        self._module.set_binding_key(self._binding_key)
        self._module.set_custom_variables(self._custom_variables)
        return self._module


class SaveDataModuleBuilder(ModuleBuilderBase, ABC):
    def __init__(self):
        super(SaveDataModuleBuilder, self).__init__()
        self._module = SaveDataModule()

    def build(self):
        self._module.set_mq_config(self._mq_config)
        self._module.set_exchange(self._exchange)
        self._module.set_id("{}.save_data".format(self._exchange))
        self._module.set_routing_keys(self._routing_keys)
        self._module.set_binding_key(self._binding_key)
        self._module.set_custom_variables(self._custom_variables)
        return self._module
