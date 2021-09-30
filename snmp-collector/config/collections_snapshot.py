from utils import load_config_from_file
from utils.dependency_injection.wiring import register
import json


@register(config_file_path="./assets/collections-snapshot.json")
class CollectionsSnapshot(object):
    def __init__(self, config_file_path):
        self.config_file_path = config_file_path
    def get_content(self):
        return  load_config_from_file(self.config_file_path)['collections']
    def write_content(self, content):
        wrapper = {"collections":content}
        json_string = json.dumps(wrapper, indent=4, ensure_ascii=False)
        with open(self.config_file_path, 'w', encoding='utf-8') as fp:
            fp.write(json_string)


    def append(self, status):
        content = self.get_content()
        content.append(status)
        self.write_content(content)
    
    def update(self, name, is_running=False):
        content = self.get_content()
        index = -1
        for i,item in enumerate(content):
            if item['name'] == name:
                item['is_running'] = is_running
                index = i
                break
        if index != -1:
            self.write_content(content)
    
    def delete(self, name):
        content = self.get_content()
        index = -1
        for i,item in enumerate(content):
            if item['name'] == name:
                index = i
            break
        if index !=-1:
            content.pop(index)
            self.write_content(content)

