'''
Created on Apr 7, 2015

@author: rsingh
'''
from NSLib.db.MongoInit import MongoInit

class AutoIncStore(object):

    def __init__(self, config):
        self.config = config
        self.mongo = MongoInit(config)

    def getNext(self, key):
        self.mongo.autoIncStoreCollection.update({'_id': key}, {'$inc': {'value': 1}}, upsert=True)
        res = self.mongo.autoIncStoreCollection.find_one({'_id': key})
        if res:
            return res['value']

        return None



