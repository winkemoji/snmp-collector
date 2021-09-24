from core.db.decorator import query


@query.insert("insert into collections(name,c_pid,p_pid,s_pid,status) values({name},{c_pid},{p_pid},{s_pid},{status})")
def insert_one(name, c_pid, p_pid, s_pid, status):
    pass


@query.select("select * from collections")
def select_all():
    pass


@query.select("select collection_id from collections")
def select_ids():
    pass

@query.delete("delete from collections where collection_id = {collection_id}")
def delete_by_collection_id(collection_id):
    pass

@query.delete("delete from collections")
def clear_all():
    pass


@query.update("update sqlite_sequence set seq=0 where name='collections'")
def reset_ai():
    pass


@query.select("select name from collections")
def select_names():
    pass


@query.select("select * from collections where collection_id={collection_id}")
def select_by_id(collection_id):
    pass


@query.update("update collections set status = {status} where collection_id={collection_id}")
def update_status_by_id(collection_id, status):
    pass



@query.select("select * from collections where name={name}")
def select_by_name(name):
    pass