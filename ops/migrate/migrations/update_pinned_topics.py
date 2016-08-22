'''
Created on Dec 27, 2014

@author: rsingh
'''

from NSLib.db.MongoInit import MongoInit
from NSLib.Config import config

if __name__ == '__main__':
    #exit()
    mongo = MongoInit(config)
    rows = mongo.pinnedTopicCollection.find()
    for row in rows:
        topics = row['topics']
        newTopics = []
        for t in topics:
            newTopics.append({'name': t, 'last_seen': 1420050600})

        mongo.pinnedTopicCollection.update({'_id': row['_id']}, {'$set': {'topics': newTopics}})

