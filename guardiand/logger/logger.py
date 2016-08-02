import socket
from datetime import datetime

class Logger(object):
    """
    """

    def __init__(self, module):
        self.module = str(module)
        self.hostname = socket.gethostname()

    def debug(self, message):
        """ Prints a verbose log message

        Params:
            message The message to be logged
        """
        self.log_line('DEBUG', message)

    def info(self, message):
        """ Prints an standard informational log message

        Params:
            message The message to be logged
        """
        self.log_line('INFO', message)

    def warning(self, message):
        """ Prints a warning log message

        Params:
            message The message to be logged
        """
        self.log_line('WARNING', message)

    def error(self, message):
        """ Prints an error log message

        Params:
            message The message to be logged
        """
        self.log_line('ERROR', message)

    def fatal(self, message):
        """ Prints a fatal log message

        Params:
            message The message to be logged
        """
        self.log_line('FATAL', message)

    def log_line(self, level, message):
        """ Prints a log message

        Params:
            level Severity of the message
            message The message to be logged
        """
        # TODO: make this actually log like a real unix program
        print('{:%Y-%m-%d %H:%M:%S} {} guardiand[{}] {}: {}'
              .format(datetime.now(), self.hostname,
                      self.module, level, message))
