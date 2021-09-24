from core.db.decorator import entity, DataType, field


@entity(table_name="blueprints")
class Blueprints:
    def __init__(self):
        self.blueprint_id = field.set_dt(DataType.INTEGER).is_pk().is_ai().is_u().build()
        self.name = field.set_dt(DataType.TEXT).build()
        self.blueprint = field.set_dt(DataType.TEXT).build()
        self.create_time = field.custom("TIMESTAMP NOT NULL DEFAULT (datetime(CURRENT_TIMESTAMP, 'localtime'))").build()
        self.tag = field.set_dt(DataType.TEXT).build()


@entity(table_name="collections")
class Collections:
    def __init__(self):
        self.collection_id = field.set_dt(DataType.INTEGER).is_pk().is_ai().is_u().build()
        self.name = field.set_dt(DataType.TEXT).is_u().build()
        self.c_pid = field.set_dt(DataType.INTEGER).build()
        self.p_pid = field.set_dt(DataType.INTEGER).build()
        self.s_pid = field.set_dt(DataType.INTEGER).build()
        self.status = field.set_dt(DataType.INTEGER).build()
        self.create_time = field.custom("TIMESTAMP NOT NULL DEFAULT (datetime(CURRENT_TIMESTAMP, 'localtime'))").build()


@entity(table_name="collect_data_details")
class CollectDataDetails:
    def __init__(self):
        self.pid = field.set_dt(DataType.INTEGER).build()
        self.routing_keys = field.set_dt(DataType.TEXT).build()
        self.binding_key = field.set_dt(DataType.TEXT).build()
        self.status = field.set_dt(DataType.INTEGER).build()


@entity(table_name="parse_data_details")
class ParseDataDetails:
    def __init__(self):
        self.pid = field.set_dt(DataType.INTEGER).build()
        self.routing_keys = field.set_dt(DataType.TEXT).build()
        self.binding_key = field.set_dt(DataType.TEXT).build()
        self.status = field.set_dt(DataType.INTEGER).build()


@entity(table_name="save_data_details")
class SaveDataDetails:
    def __init__(self):
        self.pid = field.set_dt(DataType.INTEGER).build()
        self.routing_keys = field.set_dt(DataType.TEXT).build()
        self.binding_key = field.set_dt(DataType.TEXT).build()
        self.status = field.set_dt(DataType.INTEGER).build()
