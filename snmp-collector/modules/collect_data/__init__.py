import time
import subprocess
import traceback
import re
import json
from abc import ABC
from threading import Thread
from modules import ModuleBase
from utils.log import init_logger
from utils.cmd_builder import GetCmdBuilder, WalkCmdBuilder, version, securityLevel

logger = init_logger(__name__)


class CollectDataModule(ModuleBase, ABC):
    """采集数据模块

    Args:
        ModuleBase: 基础模块，模块的基本方法与初始化
    """
    def __init__(self):
        super(CollectDataModule, self).__init__()
        self.agents = []
        self.snmp_credentials = {}
        self.oids = []
        self.get_op_oids = []
        self.walk_op_oids = []
        self.collect_interval = None
        self._thread_stop = False

    def init_custom_variables(self):
        """初始化custom_variables

        Note:
            通过get_custom_variables()获取所有当前模块配置信息
        """
        self.agents = self.get_custom_variables()['agents']
        self.snmp_credentials = self.get_custom_variables()['snmp_credentials']
        self.oids = self.get_custom_variables()['oids']
        self.get_op_oids = [o['oid'] for o in self.oids if o['operation'] == 'get'
                            ]  # get操作和walk操作分开,因为get操作可以一连串执行多个oid,可以加快采集速度
        self.walk_op_oids = [
            o['oid'] for o in self.oids if o['operation'] == 'walk'
        ]
        self.collect_interval = self.get_custom_variables()['collect_interval']

    def binding_callback(self, ch, method, properties, body):
        """回调函数，用于处理接收到的数据

        Args:
            ch ([type]): [description]
            method ([type]): [description]
            properties ([type]): [description]
            body (byte): 接收到的数据
        """
        msg = body.decode("utf-8").lower()
        if msg == "start":
            self.async_collect_data()
        elif msg == "stop":
            self.stop_collect_data()
        elif msg == "restart":
            self.stop_collect_data()
            self.async_collect_data()

    def stop_collect_data(self):
        """停止采集
        """
        self.emit("stop collect data...",log=True)
        self._thread_stop = True

    def async_collect_data(self):
        """开始采集
        """
        self.emit("start async collect data...",log=True)
        self._thread_stop = False
        for agent in self.agents:
            self.async_do_snmp_cmd(agent)
        pass
    def async_do_snmp_cmd(self, agent):
        """多线程异步采集数据
        Args:
            agent (dict): agent对象，包括ip, use_default_credentials, credentials
        """
        t = Thread(target=self.do_snmp_cmd,args=(agent,))
        t.setDaemon(True)
        t.start()

    def do_snmp_cmd(self, agent):
        """执行snmp命令获取当前agent下所有oid对应的数据
        Args:
            agent (dict): agent对象，包括ip, use_default_credentials, credentials
        """
        try:
            while not self._thread_stop:
                credentials = self.snmp_credentials
                if not agent['use_default_credentials']: #如果不使用默认登录凭证
                    credentials = agent['credentials']
                get_op_cmd = build_get_op_cmd(ip=agent['ip'], oids=self.get_op_oids, credentials=credentials)
                walk_op_cmds = [build_walk_op_cmd(ip=agent['ip'], oid=o, credentials=credentials) for o in self.walk_op_oids]
                data = self.exec_get_cmd(get_op_cmd)
                for cmd in walk_op_cmds:
                    d = self.exec_walk_cmd(cmd)
                    if d is not None and data is not None:
                        data.append(d)
                self.emit(dump_data(agent=agent['ip'],data=data))
                time.sleep(int(self.collect_interval) * 60) # convert time units from  minutes to seconds.
        except BaseException as e:
            self.emit(traceback.format_exc(), log=True)
            traceback.print_exc()
            logger.error(e)

    def exec_get_cmd(self, cmd):
        """执行snmp指令
        Args:
            cmd (string):snmp指令
        
        Returns:
            [dict]: 执行cmd所获得输出
        """
        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if res.returncode !=0:
            err_str = "exec {}: {}".format(" ".join(cmd), res.stderr.decode('UTF-8'))
            logger.error(err_str)
            self.emit(err_str, log=True)
            data = None
        else:
            get_names = ((o['name'] for o in self.oids if o['operation'] == 'get')) # 获取所有get_oid_name
            data = [{next(get_names): el} for i,el in enumerate(parse_stdout_data(res.stdout)) if i %2 != 0]
            return data


    def exec_walk_cmd(self, cmd):
        """执行snmp指令
        Args:
            cmd (string):snmp指令
        
        Returns:
            [dict]: 执行cmd所获得输出
        """
        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if res.returncode !=0:
            err_str = "exec {}: {}".format(" ".join(cmd), res.stderr.decode('UTF-8'))
            logger.error(err_str)
            self.emit(err_str, log=True)
            return None
        else:
            walk_name = [o['name'] for o in self.oids if o['oid'] == cmd[-1]][0]
            d1 = parse_stdout_data(res.stdout)
            data = [{d1[i]: d1[i+1]} for i,el in enumerate(d1) if i%2==0]
            return {walk_name: data}



def parse_stdout_data(stdout):
    """解析输出

    Args:
        stdout ([byte]): 标准输出

    Returns:
        [list]: 返回解析后的数据
    """
    if stdout is None: #判断输出是否为None
        return
    pattern = r'[\r\n|\r|\n|=]' # 防止不同平台下回车不同，无法正确解析
    res = re.split(pattern,stdout.decode('UTF-8').strip()) #依照回车分割字符串
    for i,el in enumerate(res):
        if el.find(":") !=-1:
            res[i] = re.split(r'[:]',el)[-1]
    return [el.strip() for el in res]

def build_get_op_cmd(ip, oids,credentials):
    """创建get指令字符串

    Args:
        ip (string): agent ip
        oids (list): get operation oid列表
        credentials (dict): snmp凭证

    Returns:
        string: get指令字符串
    """
    return GetCmdBuilder().set_version(version.V3). \
        set_username(credentials['username']). \
        set_security_level(securityLevel.authPriv). \
        set_auth_protocol(credentials['auth_protocol']). \
        set_auth_pass(credentials['auth_pass']). \
        set_priv_protocol(credentials['priv_protocol']). \
        set_priv_pass(credentials['priv_pass']). \
        set_agent(ip). \
        set_oid(oids).build()
    

def build_walk_op_cmd(ip, oid,credentials):
    """创建walk指令字符串

    Args:
        `ip `(string): agent ip.
        `oids`(string): walk operation oid.
        `credentials`(dict): snmp凭证

    Returns:
        `string`: walk指令字符串
    """
    return WalkCmdBuilder().set_version(version.V3). \
        set_username(credentials['username']). \
        set_security_level(securityLevel.authPriv). \
        set_auth_protocol(credentials['auth_protocol']). \
        set_auth_pass(credentials['auth_pass']). \
        set_priv_protocol(credentials['priv_protocol']). \
        set_priv_pass(credentials['priv_pass']). \
        set_agent(ip). \
        set_oid(oid).build()

def dump_data(**kwargs):
    """将获取得到的数据变成json字符串
    Returns:
        string: kwargs对应的json字符串
    """
    kwargs["timestamp"] = int(time.time())
    if kwargs['data'] is None:
        logger.error("agent: {} loss connect.".format(kwargs['agent']))
        kwargs["status"] = 0
    else:
        kwargs["status"] = 1
    return json.dumps(kwargs)