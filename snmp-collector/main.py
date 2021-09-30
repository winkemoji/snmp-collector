from core.engine import engine_builder
from utils.dependency_injection import provider
from utils.dependency_injection.wiring import provide
from config.api_server_config import ApiServerConfig
from config.rabbitmq_config import RabbitmqConfig
from config.collections_snapshot import CollectionsSnapshot

provider.assemble(ApiServerConfig)
provider.assemble(RabbitmqConfig)
provider.assemble(CollectionsSnapshot)


if __name__ == '__main__':
    engine_builder(provide(ApiServerConfig)).build().run()
