'''
Created on Mar 1, 2015

@author: rsingh
'''

from NSLib.Config import config
from NSLib.db.MongoInit import MongoInit
from NSLib.MiscFunctions import hypenify

mongo = MongoInit(config)

cursor = mongo.newsArticlesCollection.find()

for row in cursor:
    tags = row['tags']

    if len(tags) > 0:
        finalTags = []
        for tag in tags:
            finalTags.append(hypenify(tag))

        mongo.newsArticlesCollection.update({'_id': row['_id']}, {'$set': {'tags': finalTags}})

cursor = mongo.pinnedTopicCollection.find()
for row in cursor:
    topics = row['topics']

    if len(topics) > 0:
        finalTopics = []
        for topic in topics:
            topic['name'] = hypenify(topic['name'])
            finalTopics.append(topic)

        mongo.pinnedTopicCollection.update({'_id': row['_id']}, {'$set': {'topics': finalTopics}})

