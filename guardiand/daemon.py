import subprocess

from guardiand.services.service import Service
from guardiand.logger.logger import Logger

class GuardianDaemon(object):
    """
    """

    logger = Logger('daemon')

    def __init__(self):
        pass

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

        # Tail the specified log file
        filename = '/var/log/secure'
        f = subprocess.Popen(['tail', '-F', filename],
            stdout = subprocess.PIPE, stderr = subprocess.PIPE)

        # Main event loop: reads lines from the specified log file
        while True:
            line = f.stdout.readline()
            self.parse_line(line)

    def initialize_services(self):
        """ Detects services and initializes them as needed

        Detects the status of all services for this instance of guardian, and
        enables them as needed.
        """
        services = list()

        # TODO: add functionality to actually detect/init services
        # hard-code sshd service to be automatically created
        services.append(Service("ssh", "sshd"))

        return services

    def parse_line(self, line):
        """
        """

        # Find a service to accept and process the given line
        for service in self.services:
            if service.match_line(line):
                return

        # Didn't find a service to process the line, let's just print it
        print("No service found matching:: " + line)
