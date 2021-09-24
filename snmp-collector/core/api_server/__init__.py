from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from core.api_server.blueprints import Blueprints, Blueprint, BlueprintAssemble
from core.api_server.collections import Collections, Collection, CollectionStart, CollectionStop, CollectionRestart


api_server = Flask(__name__)

CORS(api_server, resources=r'/*')

api = Api(api_server)

# 获取采集
api.add_resource(Collections, "/api/collections")
# 删除采集
api.add_resource(Collection,"/api/collections/<collection_id>")
# 启动采集
api.add_resource(CollectionStart, "/api/collections/start/<collection_id>")
# 停止采集
api.add_resource(CollectionStop, "/api/collections/stop/<collection_id>")
# 重启采集
api.add_resource(CollectionRestart, "/api/collections/restart/<collection_id>")
# 获取所有蓝图,添加蓝图
api.add_resource(Blueprints, "/api/blueprints")
# 获取,删除,更新指定蓝图
api.add_resource(Blueprint, "/api/blueprints/<blueprint_id>")
# 组装蓝图
api.add_resource(BlueprintAssemble, "/api/blueprints/assemble/<blueprint_id>")