import re

from guardiand.model import model

from guardiand.actions.firewalld import FirewalldActions
from guardiand.actions.iptables import IPTablesActions
from guardiand.logger.logger import Logger
from guardiand.services.entry import Entry

class Service(object):
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
            a new Service
        """
        self.logger = Logger(name + ' service')
        self.logger.info('starting service process...')

        self.regex = re.compile(regex)
        self.logger.info("compiled regex: '{}'".format(regex))

        # Attempt to find an existing model for this service, otherwise
        # create a new one.
        self.model = model.find_model(name)
        if not self.model:
            self.model = model.create_model(name)

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

    def process_line(self, line):
        """ Sends the log entry to the classifier

        This method asks the classifier if the given line is malicious, and if
        so will take the appropriate action.

        Params:
            line The line to check

        Returns:
            n/a
        """
        self.logger.info('processing entry...')
        entry = Entry(line)
        # First, make a decision based on our existing data
        if self.model.is_malicious(entry):
            self.logger.info('possible attack detected!!')
        else:
            self.logger.info('entry classified as non-malicious.')
        # Then, add that data to our model
        self.model.add_entry(entry)
        self.logger.info('added entry to model')
