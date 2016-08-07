import subprocess

from pprint import pprint

from guardiand.services.service import Service
from guardiand.logger.logger import Logger

class GuardianDaemon(object):
    """
    """

    logger = Logger('daemon')

    def __init__(self):
        self.services = []

    def run(self):
        """ Initializes the new GuardianDaemon.

        Contains the initialization code for this instance and its main event
        loop where all lines are parsed and handled.
        """

        self.logger.info('initializing guardiand...')

        # Detects and enables services
        self.services = self.initialize_services()

        if not self.services:
            self.logger.fatal('Uh oh, no services were found! Exiting...')
            exit()

        ######################################################
        # Hook to load in test data
        self.logger.info('********* Loading test data!!')
        with open('secure') as f:
            for line in f.readlines():
                self.parse_line(line)

        # Print our bags of words from our models
        for s in self.services:
            self.logger.info('printing bags of words')
            pprint(s.model.bag_of_words)
        ######################################################

        # TODO: allow reading of lines from syslog/rsyslog/journald
        # Tail the specified log file
        filename = '/var/log/auth.log'
        tail = subprocess.Popen(['tail', '--follow', filename],\
            stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        listening = True
        # Main event loop: reads lines from the specified log file
        while listening:
            self.parse_line(tail.stdout.readline())

    def initialize_services(self):
        """ Detects services and initializes them as needed

        Detects the status of all services for this instance of guardian, and
        enables them as needed.
        """
        services = list()

        # TODO: add functionality to actually detect/init services
        # hard-code ssh and sudo services for testing
        services.append(Service('ssh', 'sshd'))
        services.append(Service('sudo', 'sudo'))

        return services

    def parse_line(self, line):
        """
        """
        if not type(line) is str:
            line = line.decode('utf-8')

        # Find a service to accept and process the given line
        # TODO: could change search order of services based on their num of entries.
        # i.e. if sshd has 10k entries and smtp has 100, make sure sshd is checked for a match first.
        for service in self.services:
            if service.match_line(line):
                service.process_line(line)
                break
