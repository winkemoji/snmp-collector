from core.db.decorator import query


@query.delete("delete from parse_data_details")
def clear_all():
    pass


@query.insert("insert into parse_data_details(pid,binding_key,routing_keys,status) values({pid},{binding_key},"
              "{routing_keys},{status})")
def insert_one(pid, binding_key, routing_keys, status):
    pass

@query.delete("delete from parse_data_details where pid={pid}")
def delete_by_pid(pid):
    pass