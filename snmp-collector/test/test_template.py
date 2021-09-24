import pytest


# 模块中的方法
def setup_module():
    print("setup_module：整个.py模块只执行一次")


def teardown_module():
    print("teardown_module：整个test_module.py模块只执行一次")


def setup_function():
    print("setup_function：每个用例开始前都会执行")


def teardown_function():
    print("teardown_function：每个用例结束后都会执行")


# 测试模块中的用例1
def test_one():
    print("正在执行测试模块----test_one")
    x = "this"
    assert 'h' in x


# 测试模块中的用例2
def test_two():
    print("正在执行测试模块----test_two")
    x = "hello"
    assert hasattr(x, 'check')


# 测试类
class TestCase:

    def setup_class(self):
        print("setup_class：所有用例执行之前")

    def teardown_class(self):
        print("teardown_class：所有用例执行之后")

    def setup(self):
        print("setup：每个用例开始前都会执行")

    def teardown(self):
        print("teardown：每个用例结束后都会执行")

    def test_three(self):
        print("正在执行测试类----test_three")
        x = "this"
        assert 'h' in x
