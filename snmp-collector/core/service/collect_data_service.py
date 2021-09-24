from utils import list2string
from core.query import collect_data_details


class CollectDataService(object):
    @staticmethod
    def insert_one(pid, binding_key, routing_keys, status):
        collect_data_details.insert_one(pid=pid, binding_key=binding_key,
                                        routing_keys=list2string(routing_keys), status=status)

    @staticmethod
    def select_by_pid(pid):
        return collect_data_details.select_by_pid(pid=pid)