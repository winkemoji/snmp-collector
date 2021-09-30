import traceback

from flask_restful import Resource, abort
from core.service import CollectionService, CollectDataService
from core.service.collection_service import Status
from utils import publish,kill
from utils.log import init_logger
from utils.dependency_injection.wiring import provide
from config.collections_snapshot import CollectionsSnapshot

logger = init_logger(__name__)


def abort_if_collection_doesnt_exist(collection_id):
    res = CollectionService.select_by_id(collection_id)
    if not len(res):
        abort(404, message="collection {} doesn't exist".format(collection_id))


class Collections(Resource):
    def get(self):
        return CollectionService.select_all()
            
class Collection(Resource):
    def delete(self, collection_id):
        abort_if_collection_doesnt_exist(collection_id)
        try:
            collection = CollectionService.select_by_id(collection_id)[0]
            c_pid = collection['c_pid']
            p_pid = collection['p_pid']
            s_pid = collection['s_pid']
            kill(c_pid)
            kill(p_pid)
            kill(s_pid)
            CollectionService.delete_collection_by_collection_id(collection_id)
            CollectionService.delete_details_by_pid(c_pid,p_pid,s_pid)
            #删除采集快照
            snapShot = provide(CollectionsSnapshot)
            snapShot.delete(collection['name'])
        except Exception as e:
            traceback.print_exc()
            logger.error(e)
            abort(500, message=traceback.format_exc())

class CollectionStart(Resource):
    def post(self, collection_id):
        abort_if_collection_doesnt_exist(collection_id)
        try:
            collection = CollectionService.select_by_id(collection_id)[0]
            c_pid = collection['c_pid']
            collect_data = CollectDataService.select_by_pid(c_pid)[0]
            exchange = collection['name']
            binding_key = collect_data["binding_key"]
            publish(exchange, binding_key, "start")
            CollectionService.update_status(collection_id, Status.start)
            #更新采集快照
            snapshot = provide(CollectionsSnapshot)
            snapshot.update(name=exchange,is_running=True)
            return "collection {} start.".format(exchange), 201
        except Exception as e:
            traceback.print_exc()
            logger.error(e)
            abort(500, message=traceback.format_exc())

class CollectionStop(Resource):
    def post(self, collection_id):
        abort_if_collection_doesnt_exist(collection_id)
        try:
            collection = CollectionService.select_by_id(collection_id)[0]
            c_pid = collection['c_pid']
            collect_data = CollectDataService.select_by_pid(c_pid)[0]
            exchange = collection['name']
            binding_key = collect_data["binding_key"]
            publish(exchange, binding_key, "stop")
            CollectionService.update_status(collection_id, Status.stop)
            #更新采集快照
            snapshot = provide(CollectionsSnapshot)
            snapshot.update(name=exchange,is_running=False)
            return "collection {} stop.".format(exchange), 201
        except Exception as e:
            traceback.print_exc()
            logger.error(e)
            abort(500, message=traceback.format_exc())

class CollectionRestart(Resource):
    def post(self, collection_id):
        abort_if_collection_doesnt_exist(collection_id)
        try:
            collection = CollectionService.select_by_id(collection_id)[0]
            c_pid = collection['c_pid']
            collect_data = CollectDataService.select_by_pid(c_pid)[0]
            exchange = collection['name']
            binding_key = collect_data["binding_key"]
            publish(exchange, binding_key, "restart")
            CollectionService.update_status(collection_id, Status.start)
            #更新采集快照
            snapshot = provide(CollectionsSnapshot)
            snapshot.update(name=exchange,is_running=True)
            return "collection {} restart.".format(exchange), 201
        except Exception as e:
            traceback.print_exc()
            logger.error(e)
            abort(500, message=traceback.format_exc())