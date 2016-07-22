import socket
from datetime import datetime

class Logger(object):

    def __init__(self, module):
        self.module = str(module)
        self.hostname = socket.gethostname()

    def debug(self, message):
        self.log_line('DEBUG', message)

    def info(self, message):
        self.log_line('INFO', message)

    def warning(self, message):
        self.log_line('WARNING', message)

    def error(self, message):
        self.log_line('ERROR', message)

    def fatal(self, message):
        self.log_line('FATAL', message)

    def log_line(self, level, message):
        print('{:%Y-%m-%d %H:%M:%S} {} guardiand[{}] {}: {}'
                    .format(datetime.now(), self.hostname,
                            self.module, level, message))
