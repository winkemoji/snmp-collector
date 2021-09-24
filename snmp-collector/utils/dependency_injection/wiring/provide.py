from utils.dependency_injection.container import container


class ProvideBase(object):
    def __init__(self, ins_container):
        self._container = ins_container
        pass


class Provide(ProvideBase):
    def __init__(self, ins_container):
        super(Provide, self).__init__(ins_container)

    def __call__(self, arg):
        return self._container.get_instance(arg)


provide = Provide(ins_container=container)
