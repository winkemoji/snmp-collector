from core.db.decorator import query


@query.insert("insert into blueprints(name,tag,blueprint) values({name},{tag},{blueprint})")
def insert_one(name, tag, blueprint):
    pass


@query.select("select * from blueprints ")
def select_all():
    pass


@query.select("select * from blueprints where blueprint_id={blueprint_id}")
def select_by_id(blueprint_id):
    pass


@query.delete("delete from blueprints where blueprint_id={blueprint_id}")
def delete_by_id(blueprint_id):
    pass


@query.update("update blueprints set name={name}, blueprint={blueprint},tag={tag} where blueprint_id = {"
              "blueprint_id} ")
def update_by_id(blueprint_id, name, tag, blueprint):
    pass


@query.select("select name from blueprints")
def select_names():
    pass
