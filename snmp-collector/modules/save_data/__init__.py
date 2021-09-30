from abc import ABC

from modules import ModuleBase
import traceback
import motor.motor_asyncio
import asyncio
import datetime
import time
import json
from utils.log import init_logger
from apscheduler.schedulers.blocking import BlockingScheduler
import threading

logger = init_logger(__name__)

lock = threading.Lock()

class SaveDataModule(ModuleBase, ABC):
    def __init__(self):
        super(SaveDataModule, self).__init__()
        self.host = ""
        self.port = ""
        self.username = ""
        self.password = ""
        self.database = ""
        self.length = 100
        self._collection = None
        self._loop = None
        self.collection_name = ""
        self.connection = ""
        self.start_date = ""


    def init_custom_variables(self):
        val = self.get_custom_variables()
        mongodb = val['mongodb']
        self.host = mongodb['host']
        self.port = mongodb['port']
        self.username = mongodb['username']
        self.password = mongodb['password']
        self.database = mongodb['database']

        self.connection = self.init_connection()
        self.start_date = datetime.date.today()
        self.set_collection()
    
    def init_connection(self):
        self._init_event_loop()
        return self._connect_and_getting_database()
    
    def set_collection(self):
        lock.acquire()
        try:
            self.collection_name = str(datetime.date.today())
            self._collection = self.connection[self.collection_name]
        finally:
            lock.release()

    def reset_collection(self):
        current_date = datetime.date.today()
        if current_date.day != self.start_date.day:
            self.set_collection()
            self.start_date = current_date
    
    def binding_callback(self, ch, method, properties, body):
        try:
            self.reset_collection()
            data = body.decode("utf-8")
            data = json.loads(data)
            self.do_insert(data)
        except BaseException as e:
            self.emit(traceback.format_exc(), log=True)
            traceback.print_exc()
            logger.error(e)


    def _init_event_loop(self):
        if self._loop is None:
            new_loop = asyncio.new_event_loop()
            asyncio.set_event_loop(new_loop)
            self._loop = asyncio.get_event_loop()
    def _connect_and_getting_database(self):
        try:
            conn_url = 'mongodb://{}:{}@{}:{}'.format(self.username, self.password, self.host, self.port)
            conn_info = 'data stored in {}:{}/{}/{}'.format(self.host, self.port, self.database, self.collection_name)
            logger.info(conn_info)
            print(conn_info)
            client = motor.motor_asyncio.AsyncIOMotorClient(conn_url)
            return client[self.database]
        except Exception as e:
            logger.error(e)

    def do_insert(self, *args, **kwargs):
        """插入多条数据
        :param args: 多条数据，可以是dict、dict的list或dict的tuple
        :param kwargs: 单条数据，如name=XerCis, gender=male
        :return: 添加的数据在库中的_id
        """
        try:
            documents = []
            for i in args:
                if isinstance(i, dict):
                    documents.append(i)
                else:
                    documents += [x for x in i]
            if kwargs != {}:
                documents.append(kwargs)
            # LOCK
            with lock:
                self._loop.run_until_complete(self.__do_insert(documents))
        except Exception as e:
            logger.error(e)

    def do_find(self, query):
        """
        查找多条数据
        """
        try:
            self._loop.run_until_complete(self.__do_find(query))
        except Exception as e:
            logger.error(e)

    def do_count(self, query):
        try:
            return self._loop.run_until_complete(self.__do_count(query))
        except Exception as e:
            logger.error(e)

    async def __do_count(self, query):
        return await self._collection.count_documents(query)

    async def __do_find(self, query):
        cursor = self._collection.find(query)
        documents = [document for document in await cursor.to_list(self.length)]
        logger.info('find %d docs (length AKA batch size: %d)' % (len(documents), self.length,))
        return documents

    async def __do_insert(self, documents):
        result = await self._collection.insert_many(documents)
        # logger.info('inserted %d docs' % (len(result.inserted_ids),))
        

