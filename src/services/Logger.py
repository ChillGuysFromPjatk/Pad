import logging
import argparse

log = logging.Logger('logger')
from src.services.Metaclasses.SingletonMeta import SingletonMeta


class Logger(metaclass=SingletonMeta): #Singleton czy logging.Loger?
    log_levels = {
        'DEBUG': logging.DEBUG,
        'INFO': logging.INFO,
        'WARNING': logging.WARNING,
        'ERROR': logging.ERROR,
        'CRITICAL': logging.CRITICAL
    }

    def __init__(self, name=None, level=logging.NOTSET):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)

        handler = logging.StreamHandler()
        console_format = logging.Formatter('%(asctime)s -- %(levelname)s -- %(message)s')
        handler.setFormatter(console_format)

        if not self.logger.hasHandlers():
            self.logger.addHandler(handler)

    def parse_logging_level(self):
        #To w sumie można zrobić jako static i wrzucić tu ten dict z wyżej
        parser = argparse.ArgumentParser(description='Set logging level')
        parser.add_argument('--logging_level', type=str, default='ERROR',
                            help='Set logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL')
        args = parser.parse_args()

        log_level_str = args.logging_level.upper()
        return self.log_levels.get(log_level_str)

    def info(self, message):
        self.logger.info(message)

    def warning(self, message):
        self.logger.warning(message)

    def error(self, message):
        self.logger.error(message)

    def exception(self, message):
        self.logger.exception(message)
