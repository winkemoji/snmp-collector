# API Index

| GET  | PUT  | DELETE | POST | Path                                     | Description                    |
| ---- | ---- | ------ | ---- | ---------------------------------------- | ------------------------------ |
| x    |      |        |      | /api/blueprints                          | 获取所有蓝图                   |
|      |      |        | x    | /api/blueprints                          | 添加蓝图                       |
| x    |      |        |      | /api/blueprints/{blueprint_id}           | 根据blueprint_id获取蓝图       |
|      | x    |        |      | /api/blueprints/{blueprint_id}           | 根据blueprint_id更新蓝图       |
|      |      | x      |      | /api/blueprints/{blueprint_id}           | 删除指定蓝图                   |
|      |      |        | x    | /api/blueprints/assemble/{blueprint_id}  | 根据blueprint_id创建采集       |
| x    |      |        |      | /api/collections                         | 获取所有采集                   |
|      |      | x      |      | /api/collections/{collection_id}         | 根据collection_id删除采集      |
|      |      |        | x    | /api/collections/start/{collection_id}   | 根据collection_id启动采集      |
|      |      |        | x    | /api/collections/stop/{collection_id}    | 根据collection_id停止采集      |
|      |      |        | x    | /api/collections/restart/{collection_id} | 根据collection_id重启采集      |
| x    |      |        |      | /config                                  | 获取snmp-collector配置信息     |
|      |      |        | x    | /config                                  | 更新snmp-collector配置信息     |
| x    |      |        |      | /default-config                          | 获取snmp-collector默认配置信息 |
|      |      |        | x    | /restart                                 | 重启snmp-collector服务         |


