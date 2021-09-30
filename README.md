## 容器打包：
```shell
docker build -t snmp-collector .
```

## 导出镜像
```shell
docker save > snmp-collector.tar snmp-collector:latest
```

## 镜像导入

```shell
docker load < snmp-collector.tar
```
## 容器启动：

```shell
docker run -it -d --name snmp-collector  -p 4400:4400 -p 4399:4399 -e TZ=Asia/Shanghai snmp-collector
```