import traceback
import sqlite3
from utils.log import init_logger
from config.sqlite_config import SqliteConfig
from utils.dependency_injection import provider
from utils.dependency_injection.wiring import provide

provider.assemble(SqliteConfig)
sqlite_config = provide(SqliteConfig)
logger = init_logger(__name__)


class DataBase(object):
    def __init__(self, db_file_path):
        self._db_file_path = db_file_path

    def init_conn(self):
        conn = sqlite3.connect(self._db_file_path)
        return conn

    def init_table_by_mapper(self, mapper):
        conn = self.init_conn()
        try:
            cur = conn.cursor()
            for table_name, fields in mapper.items():
                exec_sql = "CREATE TABLE IF NOT EXISTS %s (" % table_name
                for field in fields:
                    for k, v in field.items():
                        exec_sql = exec_sql + "%s %s," % (k, v)
                exec_sql = exec_sql[:-1] + ")"
                logger.debug(exec_sql)
                cur.execute(exec_sql)
        except BaseException as e:
            traceback.print_exc()
            logger.error(e)
        finally:
            conn.close()
        return self

    def dict_factory(self, cursor, row):
        d = {}
        for index, col in enumerate(cursor.description):
            d[col[0]] = row[index]
        return d

    def select(self, exec_sql):
        conn = self.init_conn()
        conn.row_factory = self.dict_factory
        try:
            cur = conn.cursor()
            logger.debug("exec sql: %s" % exec_sql)
            res = cur.execute(exec_sql).fetchall()
            return res
        except BaseException as e:
            traceback.print_exc()
            logger.error(e)
        finally:
            conn.close()

    def op_with_commit(self, exec_sql):
        conn = self.init_conn()
        cur = conn.cursor()
        logger.debug("exec sql: %s" % exec_sql)
        cur.execute(exec_sql)
        conn.commit()
        logger.debug("affected rows: %s" % cur.rowcount)
        conn.close()
        return cur.rowcount


database = DataBase(sqlite_config.file_path)
