from utils.dependency_injection.wiring.register import register
from utils.dependency_injection.container import container
import abc


class ProviderBase(metaclass=abc.ABCMeta):
    def __init__(self, ins_register, ins_container):
        self._register = ins_register
        self._container = ins_container

    @abc.abstractmethod
    def assemble(self, cls, alias=None):
        pass


class Provider(ProviderBase):
    def __init__(self, ins_register, ins_container):
        super(Provider, self).__init__(ins_register, ins_container)

    def assemble(self, cls, alias=None):
        if not isinstance(cls, type):
            raise Exception("please input class. ")
        register_item = self._register.get_register_item(cls)
        if register_item is None:
            raise Exception("class {} is not registered before.".format(cls.__name__))
        name = register_item['register_cls_name']
        register_cls = register_item['register_cls']
        register_cls_params = register_item['register_cls_params']
        if alias is not None:
            name = alias
        self._container.load_instance(name, register_cls(**register_cls_params))
        return self


provider = Provider(ins_register=register, ins_container=container)
