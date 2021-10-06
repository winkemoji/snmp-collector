# SNMP Collector

## 介绍

`Snmp Collector `是基于`SNMP`协议`v3`版本的数据采集工具，用于对大量的路由器或交换机进行数据获取，解析，并存储。支持多个采集同时进行，用于满足不同区域机器的统一管理需求。

## 提前准备

配置了SNMPv3的路由器或交换机(如需在本机测试需安装snmp)

MongoDB

snmpd(如在本地环境中部署)

RabbitMQ (如在本地环境中部署)

## 部署

`Snmp Collector`提供两种使用方式,一种直接在本机python环境下使用，另一种运行已经构建好的docker镜像。

### 1. 在本地环境中部署

将根目录下`requirements.txt`内所有包安装到您的python环境中。

```shell
pip install -r requirements.txt
```

安装好所有依赖后启动根目录下的`start.py`文件。

```shell
python start.py
```

启动后浏览器访问`http://localhost:4400/`出现 `snmp collector superserver is running.`即启动成功。

### 2. 在docker上部署（推荐）

打开控制台输入以下命令，`snmp-collector`(镜像中携带`RabbitMQ`)。

```shell
docker pull winkemoji/snmp-collector:latest
docker run -it -d --name snmp-collector  -p 4400:4400 -p 4399:4399  -e TZ=Asia/Shanghai snmp-collector
```

`SC Control Plane` 是针对`Snmp Collector`的可视化工具，使用它可以方便的对`Snmp Collector`进行操作与管理。

```shell
docker pull winkemoji/sc-control-plane:latest
docker run -it -d --name sc-control-plane  -e SC_HOST='192.168.230.72'  -p 15674:80   -e TZ=Asia/Shanghai sc-control-plane
```

`Snmp Collector` 使用端口`4399`，`4400`， `SC Control Plane` 使用端口`15674`,若需要远程访问`Snmp Collector` 需环境变量`SC_HOST`指定`Snmp Collector`服务器ip地址，默认为`localhost`。

启动两个容器后浏览器访问`http://localhost:15674/`即可。

## 使用手册 

[Snmp Collector User Manual(Chinese Version).pdf](https://github.com/winkemoji/snmp-collector/doc/.pdf)

## 其他 

`Snmp Collector` 只提供基础数据采集功能，如您需要针对其进行二次开发，提供更丰富的功能，可参考api文档。

[SNMP Collector api index.md](https://github.com/winkemoji/snmp-collector/blob/master/doc/api%20index.md)

## 作者 

WinkEmoji 1321807986@qq.com