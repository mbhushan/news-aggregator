'''
Created on Mar 4, 2015

@author: rsingh
'''

from NSLib.Config import config
from NSLib.db.MongoInit import MongoInit
import time

now = int(time.time())
mongo = MongoInit(config)
rows = list(mongo.newsArticlesCollection.find({'published': {'$gte': now}}))
print len(rows)

for row in rows:
    mongo.newsArticlesCollection.update({'_id': row['_id']}, {'$set': {'published': now}})
