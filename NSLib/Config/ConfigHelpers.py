'''
Created on 30-Jan-2013

@author: rsingh
'''

from ConfigParser import Error

class ServerConfig(object):
    def __init__(self, parser):
        try:
            self.APP_URL = parser.get('Server', 'app_url')
            self.LOCAL_STORAGE = parser.get('Server', 'local_storage')
        except Error as e:
            print "Failed to parse config ", e.message

class RedisConfig(object):
    def __init__(self, parser):
        try:
            self.HOST = parser.get('Redis', 'Host')
            self.PORT = parser.getint('Redis', 'Port')
        except Error as e:
            print "Failed to parse config ", e.message

class MongoConfig(object):
    def __init__(self, parser):
        try:
            self.HOST = parser.get('Mongo', 'Host')
            self.PORT = parser.getint('Mongo', 'Port')
        except Error as e:
            print "Failed to parse config ", e.message

class FacebookConfig(object):
    def __init__(self, parser):
        try:
            self.CONSUMER_KEY = parser.get('Facebook', 'consumer_key')
            self.CONSUMER_SECRET = parser.get('Facebook', 'consumer_secret')
        except Error as e:
            print "Failed to parse config ", e.message


class TwitterConfig(object):
    def __init__(self, parser):
        try:
            self.CONSUMER_KEY = parser.get('Twitter', 'consumer_key')
            self.CONSUMER_SECRET = parser.get('Twitter', 'consumer_secret')
        except Error as e:
            print "Failed to parse config ", e.message

class GoolgeConfig(object):
    def __init__(self, parser):
        try:
            self.CONSUMER_KEY = parser.get('Google', 'consumer_key')
            self.CONSUMER_SECRET = parser.get('Google', 'consumer_secret')
        except Error as e:
            print "Failed to parse config ", e.message

class AWSConfig(object):
    def __init__(self, parser):
        try:
            self.ACCESS_KEY = parser.get('AWS', 'access_key')
            self.ACCESS_SECRET = parser.get('AWS', 'access_secret')
        except Error as e:
            print "Failed to parse config ", e.message

