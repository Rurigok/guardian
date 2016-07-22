import re

import guardiand.actions.firewalld
from guardiand.logger.logger import Logger

class Service(object):

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
        self.logger = Logger(name + ' service')
        self.logger.info('starting service...')

        self.queue = list()
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
        result = re.search(regex, line)

        if result:
            self.queue_line(line)

        return result

    def queue_line(self, line):
        """ Adds the given line to this service's processing queue

        Params:
            line Line to add to processing queue
        """
        self.queue.append(line)
