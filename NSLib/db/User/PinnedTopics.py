'''
Created on Jan 31, 2015

@author: rsingh
'''
from NSLib.db.MongoInit import MongoInit
import time

class PinnedTopics(object):

    def __init__(self, config):
        self.config = config
        self.mongo = MongoInit(config)

    def add(self, uid, topic):
        row = self.mongo.pinnedTopicCollection.find_one({'_id': uid})
        if row:
            topics = row['topics']
            for tp in topics:
                if tp['name'] == topic:
                    return

        else:
            topics = []

        topics.append({'name': topic, 'last_seen': int(time.time())})
        self.mongo.pinnedTopicCollection.update({'_id': uid}, {'$set': {'topics': topics}}, upsert=True)

    def remove(self, uid, topic):
        row = self.mongo.pinnedTopicCollection.find_one({'_id': uid})
        if row:
            finalTopics = []
            topics = row['topics']
            for tp in topics:
                if tp['name'] != topic:
                    finalTopics.append(tp)

            self.mongo.pinnedTopicCollection.update({'_id': uid}, {'$set': {'topics': finalTopics}})

    def getTopics(self, uid):
        row = self.mongo.pinnedTopicCollection.find_one({'_id': uid})
        if not row:
            return None
        return row['topics']

    def isTopicPinned(self, uid, topic):
        topics = self.getTopics(uid)
        if topics and topic.has_key(topic):
            return True

        return False

    def setLastSeen(self, uid, topic):
        row = self.mongo.pinnedTopicCollection.find_one({'_id': uid})
        if row:
            topics = row['topics']
            for tp in topics:
                if topic == tp['name']:
                    tp['last_seen'] = int(time.time())
                    self.mongo.pinnedTopicCollection.update({'_id': uid}, {'$set': {'topics': topics}})
                    break

