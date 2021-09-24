import pytest
from core.dependency_injection import container
from core.dependency_injection import provider
from core.dependency_injection.wiring import register
from core.dependency_injection.wiring import provide


@register
class cls1:
    def __init__(self):
        pass

    def test(self):
        return "cls1 test."


@register("cls2_alias")
class cls2:
    def __init__(self):
        pass


@register(name="cls3_alias")
class cls3:
    def __init__(self):
        pass

    def test(self):
        return "i am cls3"


@register(a=3, b=4)
class cls4:
    def __init__(self, a, b):
        print("cls2:a ={}  b = {}".format(a, b))


@register(name="cls5_alias", a=3, b=4, c=5)
class cls5:
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c
        pass

    def test(self):
        return self.a + self.b + self.c


def test_register():
    """
    expect results:
        {'register_cls_name': 'cls1', 'register_cls': <class 'test_wiring.cls1'>, 'register_cls_params': {}}
        {'register_cls_name': 'cls2_alias', 'register_cls': <class 'test_wiring.cls2'>, 'register_cls_params': {}}
        {'register_cls_name': 'cls3_alias', 'register_cls': <class 'test_wiring.cls3'>, 'register_cls_params': {}}
        {'register_cls_name': 'cls4', 'register_cls': <class 'test_wiring.cls4'>, 'register_cls_params': {'a': 3, 'b': 4}}
        {'register_cls_name': 'cls5', 'register_cls': <class 'test_wiring.cls5'>, 'register_cls_params': {'a': 3, 'b': 4, 'c': 5}}
    """
    registers = register.get_registers()
    print()
    for item in registers:
        print(item)


def test_provider():
    provider.assemble(cls1).assemble(cls2).assemble(cls3).assemble(cls4).assemble(cls5).assemble(cls5).assemble(cls3,
                                                                                                                "123")

def test_container():
    res = container.get_instances()
    print()
    for item in res:
        print(item)



def test_provide():
    ins1 = provide(cls1)
    ins1.test()

    ins3 = provide("cls3_alias")
    assert ins3.test() == "i am cls3"

    ins5_1 = provide(cls5)
    ins5_2 = provide("cls5_alias")
    assert ins5_1 == ins5_2
    provide("123")
