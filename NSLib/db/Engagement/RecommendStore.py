'''
Created on Apr 25, 2015

@author: rsingh
'''
from NSLib.db.MongoInit import MongoInit

class RecommendStore(object):

    VALID_CONTENT_TYPES = ['video_card', 'story', 'opinion']

    def __init__(self, config):
        self.config = config
        self.mongo = MongoInit(config)

    def recommend(self, contentId, contentType, userId):
        self.mongo.recommendationCollection.update({'content_id': contentId, 'content_type': contentType},
                                                   {'$addToSet': {'users': userId}, '$inc': {'count': 1}}, upsert=True)

    def undoRecommend(self, contentId, contentType, userId):
        self.mongo.recommendationCollection.update({'content_id': contentId, 'content_type': contentType},
                                                   {'$pull': {'users': userId}, '$inc': {'count': -1}}, upsert=True)

    def getRecommendationCount(self, contentId, contentType):
        row = self.mongo.recommendationCollection.find_one({'content_id': contentId, 'content_type': contentType})
        if row:
            return row['count']

        return 0

    def hasRecommended(self, contentId, contentType, userId):
        if self.mongo.recommendationCollection.find_one({'content_id': contentId, 'content_type': contentType,
                                                      'users': userId}):
            return True

        return False


