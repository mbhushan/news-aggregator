'''
Created on 30-Jan-2013

@author: rsingh
'''

import os
from ConfigParser import ConfigParser
from NSLib.Config.ConfigHelpers import *

class Config(object):

    __CONFIG_FILE = '/etc/nationstory/config.ini'

    def __init__(self):
        parser = ConfigParser()
        parser.read(self.__CONFIG_FILE)

        self.serverConfig = ServerConfig(parser)
        self.redisConfig = RedisConfig(parser)
        self.mongoConfig = MongoConfig(parser)
        self.facebookConfig = FacebookConfig(parser)
        self.twitterConfig = TwitterConfig(parser)
        self.googleConfig = GoolgeConfig(parser)
        self.awsConfig = AWSConfig(parser)

config = Config()