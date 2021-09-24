import json
from utils.dependency_injection.wiring import provide
import pika
import os


def list2string(ls, separate=";"):
    return separate.join(ls)


def string2list(string):
    return string.split(";")


def load_config_from_file(file_path):
    with open(file_path) as f:
        data = json.load(f)
    return data


def publish(exchange, binding_key, message):
    mq_config = provide('RabbitmqConfig')
    host = mq_config.host
    port = mq_config.port
    username = mq_config.username
    password = mq_config.password
    credentials = pika.PlainCredentials(username, password)
    c_para = pika.ConnectionParameters(host=host, port=port, credentials=credentials)
    mq_conn = pika.BlockingConnection(c_para)

    channel = mq_conn.channel()
    channel.exchange_declare(exchange=exchange, exchange_type='topic')
    channel.basic_publish(exchange=exchange, routing_key=binding_key, body=message)


def kill(pid):
    # 本函数用于中止传入pid所对应的进程
    if os.name == 'nt':
        # Windows系统
        cmd = 'taskkill /pid ' + str(pid) + ' /f'
        try:
            os.system(cmd)
            print(pid, 'killed')
        except Exception as e:
            print(e)
    elif os.name == 'posix':
        # Linux系统
        cmd = 'kill ' + str(pid)
        try:
            os.system(cmd)
            print(pid, 'killed')
        except Exception as e:
            print(e)
    else:
        print('Undefined os.name')
