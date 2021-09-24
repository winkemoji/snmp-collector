import logging
from utils.dependency_injection import provider
from utils.dependency_injection.wiring import provide
from config.logger_config import LoggerConfig

provider.assemble(LoggerConfig)

logger_config = provide(LoggerConfig)


def init_logger(name, config=logger_config):
    logger = logging.getLogger(name)
    logger.setLevel(level=config.debug)
    handler = logging.FileHandler(config.file_path)
    handler.setLevel(config.debug)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    console = logging.StreamHandler()
    console.setLevel(config.debug)

    logger.addHandler(handler)
    logger.addHandler(console)
    return logger
