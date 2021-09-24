import abc
from abc import ABC


class ContainerBase(metaclass=abc.ABCMeta):
    def __init__(self):
        self._container = {}
        pass

    @abc.abstractmethod
    def load_instance(self, name, instance):
        pass

    @abc.abstractmethod
    def get_instance(self, *args):
        pass


class Container(ContainerBase, ABC):
    def __init__(self):
        super(Container, self).__init__()

    def load_instance(self, name, instance):
        self._container[name] = instance

    def get_instance(self, arg):
        instance = None
        if isinstance(arg, str):
            instance = self._get_instance_by_name(arg)
        elif isinstance(arg, type):
            instance = self._get_instance_by_cls(arg)
        if instance is None:
            raise Exception("please input register name or class.")
        return instance

    def get_instances(self):
        return self._container

    def _get_instance_by_name(self, name):
        if name not in self._container.keys():
            raise Exception("can not find instance by current name.")
        return self._container[name]

    def _get_instance_by_cls(self, cls):
        instance = None
        for obj in self._container.values():
            if isinstance(obj, cls):
                instance = obj
        if instance is None:
            raise Exception("can not find instance by current cls.")
        return instance


container = Container()
