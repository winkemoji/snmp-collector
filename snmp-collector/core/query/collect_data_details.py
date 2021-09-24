from core.db.decorator import query


@query.delete("delete from collect_data_details")
def clear_all():
    pass


@query.insert("insert into collect_data_details(pid,binding_key,routing_keys,status) values({pid},{binding_key},"
              "{routing_keys},{status})")
def insert_one(pid, binding_key, routing_keys, status):
    pass


@query.select("select * from collect_data_details where pid={pid}")
def select_by_pid(pid):
    pass

@query.delete("delete from collect_data_details where pid={pid}")
def delete_by_pid(pid):
    pass