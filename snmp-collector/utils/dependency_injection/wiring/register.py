class Register(object):
    """
    description:
    Register the class.
    Usage:
    @register
    class foo:
            ...

    @register(name="foo1")
    class foo:
            ...

    @register(name="foo2", a=4)
    class foo:
        def __init__(self, a):
            ...

    @register(a=4, b=5, c=6)
    class foo:
        def __init__(self, a, b, c):
            ...
    """

    def __init__(self):
        self._registers = []

        self._register_name_cache = []
        self._register_cls_name = None
        self._register_cls = None
        self._register_cls_params = {}

        super(Register, self).__init__()

    def __call__(self, *args, **kwargs):
        return self._caller(*args, **kwargs)

    def _caller(self, *args, **kwargs):
        """
        check whether decorator has parameters and continue.
        :param args:
        :param kwargs:
        :return:
        """
        if len(args) is not 1 and len(kwargs) is 0:
            raise Exception("Wrong usage.")
        self._clear_cls_info()
        if self._hasWrapper(*args, **kwargs):
            if len(kwargs) is 0:
                self._register_cls_name = args[0]
            else:
                if kwargs.__contains__("name"):
                    self._register_cls_name = kwargs["name"]
                    kwargs.pop("name")
                    self._register_cls_params = kwargs
                else:
                    self._register_cls_params = kwargs
            return self._wrapper
        else:
            self._register_cls_name = args[0].__name__
            self._register_cls = args[0]
            self._set_registers()
            return self._get_cls()

    def _set_registers(self):
        if self._register_cls_name in self._register_name_cache:
            raise Exception("Multiple class with same alias name.")
        self._register_name_cache.append(self._register_cls_name)

        self._registers.append({
            "register_cls_name": self._register_cls_name,
            "register_cls": self._register_cls,
            "register_cls_params": self._register_cls_params,
        })

    def _clear_cls_info(self):
        self._register_cls_name = None
        self._register_cls = None
        self._register_cls_params = {}

    def get_register_item(self, cls):
        for register_item in self._registers:
            if register_item['register_cls'].__name__ == cls.__name__:
                return register_item

    def get_registers(self):
        return self._registers

    def _hasWrapper(self, *args, **kwargs):
        """
        check whether need wrapper.
        :param args:
        :param kwargs:
        :return:
        """
        flag = False
        if len(args) != 0 and not callable(args[0]):
            flag = True

        if len(kwargs) != 0:
            flag = True
        return flag

    def _wrapper(self, *args, **kwargs):
        """
        if decorator with parameters, need wrapper, otherwise don't need it.
        :param args:
        :param kwargs:
        :return:
        """
        if self._register_cls_name is None:
            self._register_cls_name = args[0].__name__
        self._register_cls = args[0]

        self._set_registers()
        return self._get_cls()

    def _get_cls(self):
        return self._register_cls


register = Register()
