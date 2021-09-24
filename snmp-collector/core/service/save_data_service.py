from utils import list2string
from core.query import save_data_details


class SaveDataService(object):
    @staticmethod
    def insert_one(pid, binding_key, routing_keys, status):
        save_data_details.insert_one(pid=pid, binding_key=binding_key,
                                     routing_keys=list2string(routing_keys), status=status)

    @staticmethod
    def select_by_pid(pid):
        return save_data_details.select_by_pid(pid=pid)
