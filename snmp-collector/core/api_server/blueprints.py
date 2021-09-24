import json

import werkzeug.exceptions
from flask_restful import Resource, reqparse, abort
from core.service import BlueprintService, CollectionService
from utils.collection_factory import CollectionFactory
from utils import publish
from utils.log import init_logger
from utils.exception import KeyUniqueException
import traceback

logger = init_logger(__name__)


def abort_if_blueprint_doesnt_exist(blueprint_id):
    res = BlueprintService.select_by_id(blueprint_id=blueprint_id)
    if not len(res):
        abort(404, message="blueprint {} doesn't exist".format(blueprint_id))


parser = reqparse.RequestParser()
parser.add_argument('unique_name')
parser.add_argument('blueprint')
parser.add_argument('tag')


class Blueprints(Resource):
    def get(self):
        res = BlueprintService.select_all()
        return res

    def post(self):
        try:
            args = parser.parse_args(strict=True)
            # blueprint = args['blueprint'].replace('\n', '').replace(' ', '')
            blueprint = args['blueprint']
            res = BlueprintService.insert_one(name=args['unique_name'], tag=args['tag'], blueprint=blueprint)
            return res, 201
        except KeyUniqueException as e:
            abort(400, message=str(e))


class Blueprint(Resource):
    def get(self, blueprint_id):
        abort_if_blueprint_doesnt_exist(blueprint_id)
        res = BlueprintService.select_by_id(blueprint_id=blueprint_id)
        return res

    def delete(self, blueprint_id):
        abort_if_blueprint_doesnt_exist(blueprint_id)
        BlueprintService.delete_by_id(blueprint_id=blueprint_id)
        return '', 204

    def put(self, blueprint_id):
        try:
            abort_if_blueprint_doesnt_exist(blueprint_id)
            args = parser.parse_args(strict=True)
            res = BlueprintService.update_by_id(blueprint_id=blueprint_id, name=args['unique_name'], tag=args['tag'], blueprint=args['blueprint'])
            return res, 201
        except KeyUniqueException as e:
            abort(400, message=str(e))


class BlueprintAssemble(Resource):
    def post(self, blueprint_id):
        abort_if_blueprint_doesnt_exist(blueprint_id)
        try:
            blueprint = json.loads(BlueprintService.select_by_id(blueprint_id=blueprint_id)[0]['blueprint'])
            factory = CollectionFactory()
            process_list = factory.use_blueprint(blueprint).construct()
            collection = factory.get_collection()
            unique_name = collection.unique_name

            for name in CollectionService.select_names():
                if name['name'] == unique_name:
                    raise KeyUniqueException("already have collection named %s. please use another name or delete current collection." % unique_name)
            pid_list = []
            for process in process_list:
                process.daemon = True # 设置守护进程，主进程结束，各个模块进程也结束
                process.start() 
                pid_list.append(process.pid)
            CollectionService.init_all(collection, c_pid=pid_list[0], p_pid=pid_list[1], s_pid=pid_list[2])
            c_item = CollectionService.select_by_name(name=unique_name)
            return {"blueprint_id":blueprint_id,"collection":c_item[0]}, 201
        except KeyError as e:
            abort(400, message="key error: %s, please check blueprint." % e)
        except KeyUniqueException as e:
            abort(400, message=str(e))
        except Exception as e:
            traceback.print_exc()
            logger.error(e)
            abort(500, message=traceback.format_exc())
