""" Contains definitions for log line processing
"""
import re

from datetime import datetime
from guardiand.logger.logger import Logger

class Entry(object):
    """ Parses and stores information of a log entry (line)

    Transforms a log line string into a structured object for simplified
    processing.

    NOTE: need to decide how to store entries across runs and without
    eventually consuming all memory. (database?)
    """

    def __init__(self, line):
        self.logger = Logger('entry')
        self.logger.info('created entry: ' + line)
        self.line_str = line
        self.parse(line)

    def parse(self, line):
        """ Extracts the information from the line

        Parses the line, calling the necessary methods to extract our desired
        information, such as timestamp, source IP, and word frequency.
        """
        self.words = line.split(' ')

        # Extract timestamp (first 15 chars of line)
        self.timestamp = self.read_timestamp(line[0:15])

        # Extract IP
        self.ip_addr = self.read_ip_addr(line)

    def read_ip_addr(self, line):
        pass

    def read_timestamp(self, datestr):
        """ Transforms a date string into a python datetime object

        Params:
            datestr A string representing a date like "Aug  4 19:41:53"

        Returns:
            a datetime object representing the given date
        """
        # TODO: there has to be a better way of doing this...
        strlist = list(datestr)
        if strlist[4] == ' ':
            strlist[4] = '0'
        datestr = ''.join(strlist)
        timestamp = datetime.strptime(datestr, '%b %d %H:%M:%S')\
                            .replace(year=datetime.today().year)
        return timestamp
