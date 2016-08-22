'''
Created on Apr 21, 2015

@author: rsingh
'''
from NSLib.db.MongoInit import MongoInit
from NSLib.db.Engagement.RecommendStore import RecommendStore
import time
from bson.objectid import ObjectId
import arrow
from werkzeug import LocalProxy
from flask.globals import current_app

class UserStories(object):

    STATUS_DRAFT = 0
    STATUS_PUBLISHED = 1 #this is not used anymore, user approved
    STATUS_APPROVED = 2
    STATUS_DISAPPROVED = 3

    def __init__(self, config):
        self.config = config
        self.mongo = MongoInit(config)

    def add(self, userId, title, body, coverPic, tags, draft, status):
        row = {'user_id': userId, 'title': title, 'body': body, 'cover_pic': coverPic,
               'tags':tags, 'draft': draft, 'status': status, 'last_updated': int(time.time()),
               'added': int(time.time())}

        if status == self.STATUS_APPROVED:
            row['published'] = int(time.time())

        _id = self.mongo.userStoriesCollection.insert(row)
        return _id

    def update(self, _id, userId, title, body, coverPic, tags, draft, status):
        savedRow = self.mongo.userStoriesCollection.find_one({'_id': ObjectId(_id)})

        if title and body:
            row = {'title': title, 'body': body, 'last_updated': int(time.time()),
                   'cover_pic': coverPic,'tags':tags}

        elif draft:
            row = {'draft': draft, 'last_updated': int(time.time())}

        if status == self.STATUS_APPROVED:
            #remove draft once published
            row['draft'] = None
            row['status'] = self.STATUS_APPROVED

            if savedRow['status'] == self.STATUS_DRAFT:
                row['published'] = int(time.time())

        self.mongo.userStoriesCollection.update({'_id': ObjectId(_id)}, {'$set': row})

    def getFive(self):
        return list(self.mongo.userStoriesCollection.find({'status': self.STATUS_APPROVED}).sort('published', -1).limit(5))

    def setStatus(self, _id, status, adminUser):
        self.mongo.userStoriesCollection.update({'_id': ObjectId(_id)}, {'$set': {'status': status, 'admin_user': adminUser}})

    def findById(self, _id):
        return self.mongo.userStoriesCollection.find_one({'_id': ObjectId(_id)})

    def deleteById(self, _id):
        return self.mongo.userStoriesCollection.remove({'_id': ObjectId(_id)})

    def findByUser(self, userId, ts=None, allPosts=False, count=20):
        if ts:
            if allPosts:
                query = {'user_id': userId, 'added': {'$lt': ts}}
            else:
                query = {'user_id': userId, 'published': {'$lt': ts}}
        else:
            query = {'user_id': userId}

        if not allPosts:
            query['status'] = self.STATUS_APPROVED
            return list(self.mongo.userStoriesCollection.find(query).sort('published', -1).limit(count))

        else:
            #for opinion owner
            return list(self.mongo.userStoriesCollection.find(query).sort('added', -1))

    def findAllPublished(self, ts=None, count=20):
        query = {'status': self.STATUS_APPROVED}
        if ts:
            query['published'] = {'$lt': ts}

        return list(self.mongo.userStoriesCollection.find(query).sort('published', -1).limit(count))


    def findAll(self, ts=None, status=None):
        if ts:
            query = {'published': {'$lt': ts}}
        else:
            query = {}

        if status:
            query['status'] = status

        return list(self.mongo.userStoriesCollection.find(query).sort('last_updated', -1))

    def format(self, story, currentUser=None):
        resp = {}
        if not story['tags']:
            story['tags'] = []

        resp['_id'] = str(story['_id'])
        resp['user_id'] = story['user_id']

        _security = LocalProxy(lambda: current_app.extensions['security'])
        _datastore = LocalProxy(lambda: _security.datastore)
        author = _datastore.search_user({'_id': resp['user_id']})

        if author:
            resp['author_name'] = author.name
            resp['author_username'] = author.username
        else:
            resp['author_name'] = 'NationStory user'
            resp['author_username'] = ''

        recommendStore = RecommendStore(self.config)
        resp['recommendation'] = recommendStore.getRecommendationCount(resp['_id'], 'opinion')

        if currentUser:
            resp['has_recommended'] = recommendStore.hasRecommended(resp['_id'], 'opinion', currentUser)
        else:
            resp['has_recommended'] = False

        if story['status'] == 0:
            resp['status'] = 'Draft'
        elif story['status'] == 1:
            resp['status'] = 'Pending approval'
        elif story['status'] == 2:
            resp['status'] = 'Published'
        elif story['status'] == 3:
            resp['status'] = 'Under moderation'

        if story['status'] == self.STATUS_DRAFT:
            published = story.get('last_updated')
            draft = story['draft']
            resp['title'] = draft['title']
            resp['published_ts'] = published
            resp['published'] = arrow.get(published).humanize()
            resp['tags'] = list(set(draft['tags']))[:5]
            resp['photo'] = draft['cover_pic']
            resp['body'] = draft['body']

        else:
            published = story.get('published')
            resp['title'] = story['title']
            resp['published_ts'] = published
            resp['published'] = arrow.get(published).humanize()
            resp['tags'] = list(set(story['tags']))[:5]
            resp['photo'] = story['cover_pic']
            resp['body'] = story['body']

        return resp
