'''
Created on Nov 4, 2014

@author: rsingh
'''

'''
Created on 22-Nov-2012

@author: rsingh
'''

import logging.config
import os


class Logger:
    '''
    Use Logger.getLogger(GazeLogger.LOGGER_WEBSITE) to get a pre-configured logger
    '''

    LOGGER_WEBSITE = 'website'
    LOGGER_ADMIN = 'admin'
    LOGGER_COMMON = 'common'
    LOGGER_CONSOLE = 'console'

    __LOGGER_CONFIG = 'logger.conf'
    __LOG_DIRECTORY = '/var/log/nationstory/'

    def __init__(self, name):
        #create the needed directory if not present
        if not os.path.exists(self.__LOG_DIRECTORY):
            os.makedirs(self.__LOG_DIRECTORY, 0755)

        #load the config file
        logging.config.fileConfig(os.path.dirname(os.path.abspath(__file__)) + '/' + self.__LOGGER_CONFIG)

        # create logger
        self.logger = logging.getLogger(name)

    @staticmethod
    def getLogger(name):
        gazeLogger = Logger(name)
        return gazeLogger.logger


