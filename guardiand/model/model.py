""" Model representation based on the given data set """
from collections import Counter

from guardiand.logger.logger import Logger

def find_model(name):
    return False

def create_model(name):
    return Model(name, list())

class Model(object):
    """
    """
    def __init__(self, name, data):
        """ Initializes a new model object
        """
        self.name = name
        self.logger = Logger(name + ' model')
        if not type(data) is list:
            data = list()
            self.logger.warning('created empty list to init model')
        self.data = data
        self.bag_of_words = Counter()

    def add_entry(self, entry):
        """
        """
        self.data.append(entry)
        for word in entry.words:
            self.bag_of_words[word] += 1

    def is_malicious(self, entry):
        """ Classifies an entry as malicious or non malicious

        Params:
            entry The entry to classify

        Returns:
            True if the entry is an attack, False otherwise
        """
        # TODO: add classification of lines
        # self.data represents all lines
