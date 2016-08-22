'''
Created on Apr 10, 2015

@author: rsingh
'''
import time

from NSLib.db.MongoInit import MongoInit
from NSLib.db.AutoIncStore import AutoIncStore
import arrow

class CommentStore(object):

    VALID_CONTENT_TYPES = ['video_card', 'story', 'opinion']

    CONTENT_STORY = 1

    STATUS_PUBLISHED = 1
    STATUS_DELETED = 2
    STATUS_UNDER_MODERATION = 3

    FLAG_OK = 0
    FLAG_SPAM = 1
    FLAG_HATEFUL = 2
    FLAG_SPAM = 3
    FLAG_BULLYING = 4

    def __init__(self, config):
        self.config = config
        self.mongo = MongoInit(config)

    def add(self, contentId, contentType, text, userId, parentId=None):
        row = {'content_id': contentId, 'content_type': contentType,
               'text': text, 'user_id': userId, 'parentId': parentId,
               'published': int(time.time()), 'status': self.STATUS_PUBLISHED,
               'upvotes':0, 'downvotes': 0, 'votes': 0, 'flag': self.FLAG_OK}

        ais = AutoIncStore(self.config)
        row['_id'] = ais.getNext('comment_id')

        return self.mongo.commentsCollection.insert(row)

    def getById(self, _id):
        return self.mongo.commentsCollection.find_one({'_id': _id})

    def loadCommentByContent(self, contentId, contentType=CONTENT_STORY):
        comments = list(self.mongo.commentsCollection.find({'content_id': contentId, 'content_type': contentType}).sort('published', -1).limit(15))
        return comments

    def format(self, comment):
        user = self._getUser(comment['user_id'])
        if not user:
            user = {'name': 'Nationstory user', 'user_id': 0, 'username': 'Nationstory user'}
        resp = {'text': comment['text'], 'published': arrow.get(comment['published']).humanize(),
                'user_id': comment['user_id'], 'name': user['username'], 'profile_pic': '/static/img/anonUser.jpg'}

        return resp

    def _getUser(self, userId):
        return self.mongo.userCollection.find_one({'_id': userId})
