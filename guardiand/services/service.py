import queue
import re
from multiprocessing import Process

from guardiand.actions.firewalld import FirewalldActions
from guardiand.actions.iptables import IPTablesActions
from guardiand.logger.logger import Logger

class Service(Process):
    """
    """

    def __init__(self, name, regex):
        """ Constructs a new Service

        A Service represents a certain server or program that is running on
        this host that should be protected by guardian, e.g. sshd. Services
        each run in their own thread and read from a queue.

        Params:
            regex Regular expression that dictates which log lines will be
                  parsed and handled.

        Returns:
            n/a
        """
        # call super constructor
        Process.__init__(self, target=self.consume_lines)

        self.logger = Logger(name + ' service')
        self.logger.info('starting service process...')

        self.queue = queue.Queue()
        self.regex = re.compile(regex)
        self.logger.info("compiled regex: '{}'".format(regex))

    def match_line(self, line):
        """ Matches the line to this service's regex

        Allows the guardian daemon to determine if this service is suitable for
        handling the given line. If so, then the line will be queued for
        processing by this service.

        Params:
            line Line to match regex against

        Returns:
            true if match was found, false otherwise
        """
        #self.logger.info('Checking line: ' + line)

        return self.regex.search(line)

    def queue_line(self, line):
        """ Adds the given line to this service's processing queue

        Params:
            line Line to add to processing queue
        """
        self.logger.info('Queued: ' + line)
        self.queue.put(line)

    def consume_lines(self):
        """
        """
        consuming = True
        while consuming:
            line = self.queue.get()
            self.process_line(line)

    def process_line(self, line):
        """
        """
        self.logger.info('Processing: ' + line)
