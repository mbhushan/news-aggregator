'''
Created on Nov 29, 2014

@author: rsingh
'''
from NSLib.db.MongoInit import MongoInit
import time
import pymongo

class ArticlesQueue(object):

    def __init__(self, config):
        self.mongo = MongoInit(config)

    def setIndex(self):
        self.mongo.articlesQueueCollection.ensure_index([('metadata.feed_id', pymongo.ASCENDING)], unique=True)

    def add(self, title, content, metadata):
        self.mongo.articlesQueueCollection.insert({'title': title, 'content': content,
                                                   'metadata': metadata, 'timestamp': int(time.time()),
                                                   'processed': False})

    def getRawData(self):
        rows = list(self.mongo.articlesQueueCollection.find({'processed': False}).sort('timestamp', -1).limit(1))
        if rows:
            return rows[0]

    def delete(self, _id):
        self.mongo.articlesQueueCollection.update({'_id': _id}, {'$set': {'processed': True}})
