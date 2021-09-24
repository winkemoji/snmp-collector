from core.dependency_injection import provider
from core.dependency_injection.wiring import provide
from config.rabbitmq_config import RabbitmqConfig
import multiprocessing
from config.collections_blueprint import Collections
from core.collection_factory.collection_factory import CollectionFactory


def test_collection_factory():
    provider.assemble(RabbitmqConfig)
    provider.assemble(Collections)
    collections = provide(Collections)
    c = collections.next_collection()
    cf = CollectionFactory().use(c).construct()
