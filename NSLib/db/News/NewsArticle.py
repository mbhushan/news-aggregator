'''
Created on Nov 4, 2014

@author: rsingh
'''
from NSLib.db.MongoInit import MongoInit
import pymongo
from bson.objectid import ObjectId
import arrow
import time
from NSLib.Logger import Logger
from pymongo.errors import DuplicateKeyError

class NewsArticle(object):

    def __init__(self, config):
        self.config = config
        self.mongo = MongoInit(config)
        self.sources = None
        self.log = Logger.getLogger(Logger.LOGGER_WEBSITE)

    def setIndex(self):
        self.mongo.newsArticlesCollection.ensure_index([('feed_id', pymongo.ASCENDING)], unique=True)
        self.mongo.newsArticlesCollection.ensure_index([('published', pymongo.DESCENDING)], unique=True)

    def add(self, metadata, tags, cityTags, stateTags):
        metadata['tags'] = tags
        metadata['cities'] = cityTags
        metadata['states'] = stateTags

        metadata['votes'] = 0
        metadata['up_votes'] = []
        metadata['down_votes'] = []
        try:
            return self.mongo.newsArticlesCollection.insert(metadata)
        except DuplicateKeyError:
            return None

    def get(self, count=20):
        return list(self.mongo.newsArticlesCollection.find().sort('published', -1).limit(count))

    def findByFeedId(self, feed_id):
        return self.mongo.newsArticlesCollection.find_one({'feed_id': feed_id})

    def checkIfAlreadyPresent(self, rawData, source):
        '''
        check if same news has come from various feeds in that news company
        '''
        if self.findByFeedId(rawData['feed_id']):
            return True

        if self.mongo.newsArticlesCollection.find_one({'link': rawData['link']}):
            return True

        ts = int(time.time()) - 86400
        sources = list(self.mongo.newsSourceCollection.find({'group': source['group']}))
        sourceIds = [s['_id'] for s in sources]
        if self.mongo.newsArticlesCollection.find_one({'published': {'$gt': ts}, 'source_id': {'$in': sourceIds}, 'title': rawData['title']}):
            return True

        return False

    def getById(self, _id):
        return self.mongo.newsArticlesCollection.find_one({'_id': ObjectId(_id)})

    def findByTime(self, ts=None, count=20):
        if ts:
            query = {'published': {'$lt': ts}}
        else:
            query = {}
        query['photo'] = {'$ne': None}
        return list(self.mongo.newsArticlesCollection.find(query).sort('published', -1).limit(20))

    def getHeadlinesSources(self):
        return list(self.mongo.newsSourceCollection.find({'headline': True}))

    def findHeadlinesByTime(self, ts=None, count=20):
        sources = self.getHeadlinesSources()
        soucesIds = [s['_id'] for s in sources]

        query = {'source_id':{'$in': soucesIds}}
        if ts:
            query['published'] = {'$lt': ts}
        query['photo'] = {'$ne': None}

        return list(self.mongo.newsArticlesCollection.find(query).sort('published', -1).limit(20))

    def findBySource(self, source, ts=None, count=20):

        query = {'source_id': source}
        if ts:
            query['published'] = {'$lt': ts}

#         query['photo'] = {'$ne': None}
        return list(self.mongo.newsArticlesCollection.find(query).sort('published', -1).limit(20))

    def findByTag(self, tag, ts=None, photosOnly=True, count=20):
        if ts:
            query = {'tags': tag, 'published': {'$lt': ts}}
        else:
            query = {'tags': tag}

        if photosOnly:
            query['photo'] = {'$ne': None}

        return list(self.mongo.newsArticlesCollection.find(query).sort('published', -1).limit(20))

    def countTaggedStories(self, tag, timestamp):
        query = {'tags': tag, 'published': {'$gt': timestamp}}
        return self.mongo.newsArticlesCollection.find(query).count()

    def saveVotes(self, _id, votes, up_votes, down_votes):
        self.mongo.newsArticlesCollection.update({'_id': ObjectId(_id)}, {'$set': {'votes': votes, 'up_votes': up_votes, 'down_votes': down_votes}})

    def getRelatedTags(self, tag, limit=5):
        aggResult = self.mongo.newsArticlesCollection.aggregate([{'$match': {'tags': tag}},
                                                     {'$project': {'tags': 1 } },
                                                     {'$unwind': "$tags" },
                                                     {'$group': {'_id': "$tags", 'count': { '$sum' : 1 }}},
                                                     { '$sort': { 'count': -1 } }, {'$limit': limit}])

        relatedTags = []
        if aggResult.has_key('result'):
            for r in aggResult['result']:
                if r['_id'] != tag:
                    relatedTags.append(r['_id'])

        return relatedTags

    def getTrendingTags(self, limit=10):
        aggResult = self.mongo.newsArticlesCollection.aggregate([{'$match': {'published': {'$gte': int(time.time() - 86400)}}},
                                                     {'$project': {'tags': 1 } },
                                                     {'$unwind': "$tags" },
                                                     {'$group': {'_id': "$tags", 'count': { '$sum' : 1 }}},
                                                     { '$sort': { 'count': -1 } }, {'$limit': limit}])

        trendingTags = []
        if aggResult.has_key('result'):
            for r in aggResult['result']:
                trendingTags.append({'name': r['_id'], 'count': r['count']})

        return trendingTags

    def getDailyCount(self, tag):
        ts = int(time.time()) - 172800
        query = {'tags': tag, 'published': {'$gt': ts}}
        return self.mongo.newsArticlesCollection.find(query).count()

    def _loadSources(self):
        if not self.sources:
            self.sources = {}
            allSources = list(self.mongo.newsSourceCollection.find())
            for s in allSources:
                self.sources[s['_id']] = s

        return self.sources

    def formatStory(self, article, uid=None, source=None):
        sources = self._loadSources()
        resp = {}
        resp['_id'] = str(article['_id'])
        resp['title'] = article['title']
        resp['published_ts'] = article['published']
        resp['published'] = arrow.get(article['published']).humanize()
        resp['tags'] = list(set(article['tags']))[:5]
        resp['link'] = article['link']

        if article.get('source_id') and sources.has_key(article['source_id']):
            resp['source_name'] = sources[article['source_id']]['display_name']

        if source and article.get('cities'):
            resp['cities'] = [{'name': city, 'location': self.getCityLocation(city)} for city in article['cities']]

        photo = None
        if article.get('photo'):
            photo = article.get('photo')
            if photo and not photo.startswith('http://') and not photo.startswith('https://'):
                photo = None

        elif article.has_key('source_id'):
            photo = sources[article['source_id']]['logo']
            resp['photo'] = photo

        resp['photo'] = photo

#         resp['upvoted'] = False
#         resp['downvoted'] = False
#         if uid:
#             upvoted = uid in article['up_votes']
#             downvoted = uid in article['down_votes']
#
#             resp['upvoted'] = upvoted
#             resp['downvoted'] = downvoted

        return resp

    def getCityLocation(self, city):
        city = city.replace('-', ' ')
        row = self.mongo.indianCitiesTagsCollection.find_one({'_id': city})
        if row:
            return row.get('location')
        else:
            self.log.error("Location not found: %s" % city)

        return None

    def getSourceByGroupName(self, name):
        return self.mongo.newsSourceCollection.find_one({'group': name})


