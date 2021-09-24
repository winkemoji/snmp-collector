import json

from core.query import blueprints
from utils.exception import KeyUniqueException


class BlueprintService(object):
    @staticmethod
    def select_all():
        return blueprints.select_all()

    @staticmethod
    def insert_one(name, tag, blueprint):
        names = blueprints.select_names()
        for n in names:
            if n['name'] == name:
                raise KeyUniqueException("blueprint name should be unique.")
        return blueprints.insert_one(name=name, tag=tag, blueprint=blueprint)

    @staticmethod
    def select_by_id(blueprint_id):
        return blueprints.select_by_id(blueprint_id=blueprint_id)

    @staticmethod
    def delete_by_id(blueprint_id):
        return blueprints.delete_by_id(blueprint_id=blueprint_id)

    @staticmethod
    def update_by_id(blueprint_id, name, tag, blueprint):
        old_name = BlueprintService.get_name_in_blueprint_by_id(blueprint_id)
        names = [n['name'] for n in blueprints.select_names() if n['name'] != old_name]
        for n in names:
            if n == name:
                raise KeyUniqueException("blueprint name should be unique.")
        return blueprints.update_by_id(blueprint_id=blueprint_id, name=name, tag=tag, blueprint=blueprint)

    @staticmethod
    def get_name_in_blueprint_by_id(blueprint_id):
        name = json.loads(blueprints.select_by_id(blueprint_id=blueprint_id)[0]['blueprint'])['unique_name']
        return name


