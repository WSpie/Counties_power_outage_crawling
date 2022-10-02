import logging
from logging import FileHandler
import os

class ErrLog:
    def __init__(self, func_name):
        self.func_name = func_name
        self.logger = logging.getLogger(func_name)
        self.logger.setLevel(logging.ERROR)
        self.log_path = self.func_name + '.log'
        self.logger_file_handler = FileHandler(self.log_path, mode='w')
        self.logger.addHandler(self.logger_file_handler)
        self.logger_formatter = logging.Formatter('%(asctime)s:%(name)s:%(message)s')
        self.logger_file_handler.setFormatter(self.logger_formatter)

    def exception(self):
        self.logger.exception('[ERROR]')
        
    def shutdown(self):
        self.logger.handlers.clear()