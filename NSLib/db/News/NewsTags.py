'''
Created on Feb 28, 2015

@author: rsingh
'''
from NSLib.db.MongoInit import MongoInit

class NewsTags(object):

    def __init__(self, config):
        self.config = config
        self.mongo = MongoInit(config)

    def search(self, term):
        query = {'$or': [{'_id': {'$regex': term, '$options': 'i'}},
                        {'tags': {'$regex': term, '$options': 'i'}}]}

        tags = list(self.mongo.tagsCollection.find(query))
        cityTags = list(self.mongo.indianCitiesTagsCollection.find({'_id': {'$regex': term, '$options': 'i'}}))
        stateTags = list(self.mongo.indianStatesTagsCollection.find({'_id': {'$regex': term, '$options': 'i'}}))

        tags.extend(cityTags)
        tags.extend(stateTags)
        return tags

    def add(self, _id, tags, case_sensitive=False):
        self.mongo.tagsCollection.insert({'_id': _id, 'tags': tags, 'case_sensitive': case_sensitive})
        return {'_id': _id, 'tags': tags, 'case_sensitive': case_sensitive}

    def update(self, _id, tags, case_sensitive=False):
        self.mongo.tagsCollection.update({'_id': _id}, {'$set': {'tags': tags, 'case_sensitive': case_sensitive}})
        return {'_id': _id, 'tags': tags, 'case_sensitive': case_sensitive}

    def remove(self, _id):
        self.mongo.tagsCollection.remove({'_id': _id})

