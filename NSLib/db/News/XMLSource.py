'''
Created on Apr 6, 2015

@author: rsingh
'''
from NSLib.db.MongoInit import MongoInit
import time

class XMLSource(object):

    STATUS_PENDING = 1
    STATUS_PROCESSED = 2

    def __init__(self, config):
        self.config = config
        self.mongo = MongoInit(config)

    def add(self, name, filePath):
        row = {'group': name, 'path': filePath, 'status': self.STATUS_PENDING, 'added': int(time.time())}
        self.mongo.newsXmlSourceCollection.insert(row)

    def getPendingRows(self):
        return list(self.mongo.newsXmlSourceCollection.find({'status': self.STATUS_PENDING}))

    def setProcessed(self, _id):
        self.mongo.newsXmlSourceCollection.update({'_id': _id}, {'$set': {'status': self.STATUS_PROCESSED}})

    def getSourceDetail(self, name):
        return self.mongo.newsSourceCollection.find_one({'group': name})

