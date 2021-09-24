from utils.log import init_logger
import traceback
import pika
import datetime
import abc

logger = init_logger(__name__)


class ModuleBase(metaclass=abc.ABCMeta):
    def __init__(self):
        self._exchange = ""
        self._routing_keys = []
        self._binding_key = ""
        self._id = None
        self._mq_connection = None
        self._mq_channel = None
        self._mq_config = None
        self._custom_variables = {}
        pass

    def _init_mq_connection(self):
        mq_config = self._mq_config
        host = mq_config.host
        port = mq_config.port
        username = mq_config.username
        password = mq_config.password
        credentials = pika.PlainCredentials(username, password)
        c_para = pika.ConnectionParameters(host=host, port=port, credentials=credentials)
        self._mq_connection = pika.BlockingConnection(c_para)

    def _init_mongo_connection(self, mongo_config):
        pass

    def _init_channel(self):
        channel = self._mq_connection.channel()
        channel.exchange_declare(exchange=self.get_exchange(), exchange_type='topic')
        self._mq_channel = channel

    def set_id(self, identification):
        self._id = identification

    def get_id(self):
        return self._id

    def set_exchange(self, exchange):
        self._exchange = exchange

    def get_exchange(self):
        return self._exchange

    def set_mq_config(self, mq_config):
        self._mq_config = mq_config

    def set_binding_key(self, binding_key):
        self._binding_key = binding_key

    def set_routing_keys(self, routing_keys):
        self._routing_keys = routing_keys

    def set_custom_variables(self, custom_variables):
        self._custom_variables = custom_variables

    def get_custom_variables(self):
        return self._custom_variables

    def _bind_key(self):
        self._mq_channel.exchange_declare(exchange=self.get_exchange(), exchange_type='topic')
        result = self._mq_channel.queue_declare(queue='', exclusive=True, durable=True)
        queue_name = result.method.queue
        self._mq_channel.queue_bind(exchange=self.get_exchange(), queue=queue_name, routing_key=self._binding_key)
        logger.debug("{} binding key: {}".format(self.get_id(), self._binding_key))
        logger.debug("{} routing keys: {}".format(self.get_id(), self._routing_keys))
        self._mq_channel.basic_consume(
            queue=queue_name, on_message_callback=self.binding_callback, auto_ack=True)

    def emit(self, message, log=False):
        """根据routing_keys发送信息

        Note:
            正常发送消息不向log.x发送，只有当log=True才向日志队列发送.

        Args:
            `message (string)`: 所发送的消息.
            `log (bool, optional)`: 是否发送信息至日志队列. Defaults to False.
        """
        emit_keys = self._routing_keys
        log_keys = self._get_log_routing_keys()
        if log_keys:
            emit_keys = [k for k in emit_keys if k not in log_keys]
        if log:
            emit_keys = log_keys
            message = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S >") + message
        # 多线程下channel会关掉，使用的是block_connection,需要新建一个connection
        self._init_mq_connection()
        self._init_channel()
        for key in emit_keys:
            self._mq_channel.basic_publish(exchange=self.get_exchange(), routing_key=key, body=message)

    def _get_log_routing_keys(self):
        log_keys = [x for i, x in enumerate(self._routing_keys) if x.find('log.') != -1]
        if len(log_keys) != 0:
            return log_keys
        else:
            return False

    def start_consuming(self):
        self._bind_key()
        logger.debug("{} start consuming...".format(self.get_id()))
        self._mq_channel.start_consuming()

    @abc.abstractmethod
    def binding_callback(self, ch, method, properties, body):
        """绑定回调函数,模块的入口

        Args:
            ch ([type]): [description]
            method ([type]): [description]
            properties ([type]): [description]
            body (byte):接收的信息
        """
        pass

    @abc.abstractmethod
    def init_custom_variables(self):
        pass

    def run(self):
        """初始化模块并启动
        """
        try:
            self._init_mq_connection()
            self._init_channel()
            self.init_custom_variables()
            self.start_consuming()
        except Exception as e:
            self.emit(traceback.format_exc(),log=True)
            traceback.print_exc()
            logger.error(e)
