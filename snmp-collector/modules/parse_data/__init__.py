from abc import ABC

from modules import ModuleBase
import json
import traceback
from utils.log import init_logger

logger = init_logger(__name__)

class ParseDataModule(ModuleBase, ABC):
    def __init__(self):
        super(ParseDataModule, self).__init__()
        self.script = ""

    def init_custom_variables(self):
        self.script = self.get_custom_variables()['script']
        self.script = self.script + "\nres = parse_data(data)"

    def binding_callback(self, ch, method, properties, body):
        data = json.loads(body.decode("utf-8"))
        local = {}
        try:
            exec(self.script,{"data":data},local)
            res = local['res']
            self.emit(json.dumps(res))
        except BaseException as e:
            self.emit(traceback.format_exc(), log=True)
            traceback.print_exc()
            logger.error(e)
        pass
    pass
