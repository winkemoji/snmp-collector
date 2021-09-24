import abc


class ModuleBuilderBase(metaclass=abc.ABCMeta):
    def __init__(self):
        self._module = None
        self._mq_config = None
        self._id = None
        self._exchange = None
        self._binding_key = ""
        self._routing_keys = []
        self._custom_variables = None

    def set_custom_variables(self, custom_variables):
        self._custom_variables = custom_variables
        return self

    def set_mq_config(self, mq_config):
        self._mq_config = mq_config
        return self

    def set_exchange(self, exchange):
        self._exchange = exchange
        return self

    def set_routing_keys(self, routing_keys):
        self._routing_keys = routing_keys
        return self

    def set_binding_key(self, binding_key):
        self._binding_key = binding_key
        return self

    def append_routing_key(self, routing_key):
        self._routing_keys.append(routing_key)
        return self

    def set_id(self, identification):
        self._id = identification
        return self

    def get_module(self):
        return self._module

    @abc.abstractmethod
    def build(self):
        pass
