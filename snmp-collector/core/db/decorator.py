from core.db.db import database
from functools import wraps
from utils.log import init_logger
import re

logger = init_logger(__name__)


class DataType:
    NULL = "NULL"
    INTEGER = "INTEGER"
    TEXT = "TEXT"
    REAL = "REAL"
    BLOB = "BLOB"
    types = [INTEGER, TEXT, NULL, REAL, BLOB]


class Field(object):
    def __init__(self):
        self._data_type = None
        self._not_null = False
        self._primary_key = False
        self._auto_increment = False
        self._unique = False
        self._custom_sql = None

    def set_dt(self, data_type):
        self._data_type = data_type
        return self

    def is_nn(self):
        self._not_null = True
        return self

    def is_pk(self):
        self._primary_key = True
        return self

    def is_ai(self):
        self._primary_key = True
        self._auto_increment = True
        return self

    def is_u(self):
        self._unique = True
        return self

    def custom(self, custom_sql):
        self._custom_sql = custom_sql
        return self

    def _reset(self):
        self._data_type = None
        self._custom_sql = None
        self._not_null = False
        self._primary_key = False
        self._auto_increment = False
        self._unique = False

    def build(self):
        if self._custom_sql:
            sql = self._custom_sql
            self._reset()
            return sql
        if self._data_type not in DataType.types:
            raise TypeError("error data type.")
        s = [self._data_type]
        if self._not_null:
            s.append("NOT NULL")
        if self._primary_key:
            s.append("PRIMARY KEY")
        if self._auto_increment:
            s.append("AUTOINCREMENT")
        if self._unique:
            s.append("UNIQUE")
        s = " ".join(s)
        self._reset()
        return s


class EntityBase(object):
    def __init__(self):
        self._mapper_relation = {}

    def register(self, key, value):
        self._mapper_relation[key] = value

    def exist(self, key):
        if key in self._mapper_relation:
            return True
        return False

    def value(self, key):
        return self._mapper_relation[key]

    def get_mapper(self):
        return self._mapper_relation


class Entity(EntityBase):
    def __init__(self):
        super(Entity, self).__init__()

    def __call__(self, table_name):
        return self.wrapper(table_name)

    def wrapper(self, table_name):
        def inner(obj):
            ins = obj()
            fields = [{attr: getattr(ins, attr)} for attr in dir(ins) if isinstance(getattr(ins, attr), str)][1:]
            self.register(table_name, fields)
            return obj

        return inner


class QueryBase(object):
    def __init__(self):
        self._db = None

    @property
    def db(self):
        return self._db

    def set_db(self, db):
        self._db = db
        return self


class Query(QueryBase):
    def __init__(self):
        super(Query, self).__init__()

    def select(self, sql):
        def wrapper(func):
            @wraps(func)
            def inner(**kwargs):
                exec_sql = sql
                patt = re.compile("(?<={)[^}]*(?=})")
                keys = re.findall(patt, sql)
                for key in kwargs.keys():
                    if key not in keys:
                        raise KeyError("key: %s not in sql keys: %s." % (key, keys))
                for k, v in kwargs.items():
                    exec_sql = exec_sql.replace('{%s}' % k, "'%s'" % v)
                res = self.db.select(exec_sql)
                return res

            return inner

        return wrapper

    def insert(self, sql):
        def wrapper(func):
            @wraps(func)
            def inner(**kwargs):
                exec_sql = sql
                patt = re.compile("(?<={)[^}]*(?=})")
                keys = re.findall(patt, sql)
                for key in kwargs.keys():
                    if key not in keys:
                        raise KeyError("key: %s not in sql keys: %s." % (key, keys))
                for k, v in kwargs.items():
                    exec_sql = exec_sql.replace('{%s}' % k, "'%s'" % v)
                res = self.db.op_with_commit(exec_sql)
                return res

            return inner

        return wrapper

    def delete(self, sql):
        def wrapper(func):
            @wraps(func)
            def inner(**kwargs):
                exec_sql = sql
                patt = re.compile("(?<={)[^}]*(?=})")
                keys = re.findall(patt, sql)
                for key in kwargs.keys():
                    if key not in keys:
                        raise KeyError("key: %s not in sql keys: %s." % (key, keys))
                for k, v in kwargs.items():
                    exec_sql = exec_sql.replace('{%s}' % k, "'%s'" % v)
                    # exec_sql = exec_sql.replace('{%s}' % k, "\"%s\"" % v)
                res = self.db.op_with_commit(exec_sql)
                return res

            return inner

        return wrapper

    def update(self, sql):
        def wrapper(func):
            @wraps(func)
            def inner(**kwargs):
                exec_sql = sql
                patt = re.compile("(?<={)[^}]*(?=})")
                keys = re.findall(patt, sql)
                for key in kwargs.keys():
                    if key not in keys:
                        raise KeyError("key: %s not in sql keys: %s." % (key, keys))
                for k, v in kwargs.items():
                    exec_sql = exec_sql.replace('{%s}' % k, "'%s'" % v)
                res = self.db.op_with_commit(exec_sql)
                return res

            return inner

        return wrapper


# instantiate field builder.
field = Field()

# create entity decorator.
entity = Entity()

# register all tables.
from core.db.entity import *

# create tables in sqlite.
database.init_table_by_mapper(entity.get_mapper())

# create query decorator.
query = Query().set_db(database)
# query.db = database
