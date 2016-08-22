'''
Created on 31-Jan-2013

@author: rsingh
'''

import redis

class RedisInit(object):

    DB_DEFAULT = 0
    RAW_FEED_QUEUE = 'raw_feed_queue'

    def __init__(self, config=None, host=None, port=None, db = DB_DEFAULT):
        if config:
            host = config.mongoConfig.HOST
            port = config.mongoConfig.PORT
        elif host is not None and port is not None:
            pass
        else:
            raise ValueError("No config or host/port pair received")

        self.redis = redis.StrictRedis(host, port, db)

