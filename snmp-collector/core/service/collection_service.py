from core.query import collections
from core.query import collect_data_details
from core.query import parse_data_details
from core.query import save_data_details

from core.service.collect_data_service import CollectDataService
from core.service.parse_data_service import ParseDataService
from core.service.save_data_service import SaveDataService


class CollectionService(object):
    @staticmethod
    def init_all(c, c_pid, p_pid, s_pid):
        CollectionService.insert_one(name=c.unique_name, c_pid=c_pid, p_pid=p_pid, s_pid=s_pid)
        temp = c.collect_data_module
        CollectDataService.insert_one(pid=c_pid, binding_key=temp.binding_key, routing_keys=temp.routing_keys,
                                      status=1)
        temp = c.parse_data_module
        ParseDataService.insert_one(pid=p_pid, binding_key=temp.binding_key, routing_keys=temp.routing_keys, status=1)
        temp = c.save_data_module
        SaveDataService.insert_one(pid=s_pid, binding_key=temp.binding_key, routing_keys=temp.routing_keys, status=1)


    @staticmethod
    def clear_all():
        collections.clear_all()
        collections.reset_ai()
        collect_data_details.clear_all()
        parse_data_details.clear_all()
        save_data_details.clear_all()

    @staticmethod
    def insert_one(name, c_pid, p_pid, s_pid):
        collections.insert_one(name=name, c_pid=c_pid, p_pid=p_pid, s_pid=s_pid, status=0)

    @staticmethod
    def select_all():
        return collections.select_all()

    @staticmethod
    def select_names():
        return collections.select_names()

    @staticmethod
    def select_by_id(collection_id):
        return collections.select_by_id(collection_id=collection_id)

    @staticmethod
    def select_by_name(name):
        return collections.select_by_name(name=name)

    @staticmethod
    def update_status(collection_id, status):
        if status == Status.start:
            collections.update_status_by_id(collection_id=collection_id, status=1)
        if status == Status.stop:
            collections.update_status_by_id(collection_id=collection_id, status=0)
    
    @staticmethod
    def delete_details_by_pid(c_pid, p_pid, s_pid):
        collect_data_details.delete_by_pid(pid=c_pid)
        parse_data_details.delete_by_pid(pid=p_pid)
        save_data_details.delete_by_pid(pid=s_pid)
    @staticmethod
    def delete_collection_by_collection_id(collection_id):
        collections.delete_by_collection_id(collection_id=collection_id)

class Status:
    start = "start"
    stop = "stop"
