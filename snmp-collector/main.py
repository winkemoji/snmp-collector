from core.engine import engine_builder
from utils.dependency_injection import provider
from utils.dependency_injection.wiring import provide
from config.api_server_config import ApiServerConfig
from config.rabbitmq_config import RabbitmqConfig

provider.assemble(ApiServerConfig)
provider.assemble(RabbitmqConfig)


if __name__ == '__main__':
    engine_builder(provide(ApiServerConfig)).build().run()
