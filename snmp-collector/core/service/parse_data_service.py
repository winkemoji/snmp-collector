from utils import list2string
from core.query import parse_data_details


class ParseDataService(object):
    @staticmethod
    def insert_one(pid, binding_key, routing_keys, status):
        parse_data_details.insert_one(pid=pid, binding_key=binding_key,
                                      routing_keys=list2string(routing_keys), status=status)
