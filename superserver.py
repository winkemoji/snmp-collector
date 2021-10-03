from flask import Flask,request,jsonify
import subprocess
import os
import traceback
import logging
import json
from flask_cors import CORS
from gevent import pywsgi
import requests
import psutil

app = Flask(__name__)
# 开启跨域
CORS(app, resources=r'/*')

PIDS = []
CONFIG_FILE_PATH = './snmp-collector/assets/config.json'
DEFAULT_CONFIG_PATH = './snmp-collector/assets/default-config.json'
SNAPSHOT_PATH = './snmp-collector/assets/collections-snapshot.json'
SNMP_COLLECTOR_SERVER = 'http://0.0.0.0:4399'

def init_logger(name, filename='./superserver_log.txt'):
    logger = logging.getLogger(name)
    logger.setLevel(level=logging.DEBUG)
    handler = logging.FileHandler(filename)
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)

    logger.addHandler(handler)
    logger.addHandler(console)
    return logger

logger = init_logger(__name__)

def kill_process(pid):
    parent_proc = psutil.Process(pid)
    for child_proc in parent_proc.children(recursive=True):
        child_proc.kill()
    parent_proc.kill()

def start_snmp_collector():
    try:
        for pid in PIDS:
            # kill(pid)
            kill_process(pid)
            PIDS.remove(pid)
        cmd=['python','main.py']
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,cwd="./snmp-collector")
        PIDS.append(process.pid)
        # restore_by_snapshot()
    except BaseException as e:
        traceback.print_exc()
    return {
        "info":"restart snmp collector service.",
        "pid":process.pid
    }

@app.route("/")
def defalut_msg():
    return "snmp collector superserver is running."

@app.route("/config")
def get_config():
    config_file_path = CONFIG_FILE_PATH
    with open(config_file_path, encoding='utf-8') as fp:
        config = json.load(fp)
    return config

@app.route("/default-config")
def get_default_config():
    config_file_path = DEFAULT_CONFIG_PATH
    with open(config_file_path, encoding='utf-8') as fp:
        config = json.load(fp)
    return config



@app.route("/restart")
def restart_service():
    res = start_snmp_collector()
    return res


@app.route("/update-config",methods=['post'])
def update_config():
    data = json.loads(request.data.decode('utf-8'))
    config_file_path = CONFIG_FILE_PATH
    with open(config_file_path, encoding='utf-8') as fp:
        config = json.load(fp)
    if data['logger']:
        config['logger'] = data['logger']
    if data['rabbitmq']:
        config['rabbitmq'] = data['rabbitmq']
    json_string = json.dumps(config, indent=4, ensure_ascii=False)
    with open(config_file_path, 'w', encoding='utf-8') as fp:
        fp.write(json_string)
    start_snmp_collector()
    return config



if __name__ == '__main__':
    res = start_snmp_collector()
    if res['pid']:
        # for debug
        # app.run(host='0.0.0.0',port='4400')
        server = pywsgi.WSGIServer(('0.0.0.0',4400),app)
        server.serve_forever()
