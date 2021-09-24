from utils.dependency_injection import provider
from utils.dependency_injection import provide

from config.rabbitmq_config import RabbitmqConfig


def test_rabbitmq_config():
    provider.assemble(RabbitmqConfig)
    config = provide(RabbitmqConfig)