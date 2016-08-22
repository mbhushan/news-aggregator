'''
Created on Oct 28, 2014

@author: rsingh
'''

from NSLib.db.MongoInit import MongoInit
import time
from bson.objectid import ObjectId
import pymongo
import re

class NewsSource(object):

    TYPE_ARTICLES = 1
    TYPE_LINKS = 2
    TYPE_WEBSITE = 3

    def __init__(self, config):
        self.mongo = MongoInit(config)

    def add(self, name, url, sourceType, displayName, group, logo, headline, pattern=None):
        row = {'name': name, 'url': url, 'source_type': sourceType, 'added': int(time.time()), 'last_updated': None,
               'display_name': displayName, 'group': group, 'logo': logo, 'headline': headline, 'pattern': pattern}

        return self.mongo.newsSourceCollection.insert(row)

    def addBulk(self, name, bulk_urls, sourceType, displayName, group, logo, headline):
        added = []
        bulk_urls = re.split('\n', bulk_urls.strip())

        for url in bulk_urls:
            url = url.strip()
            if url != "" and not self.mongo.newsSourceCollection.find_one({'url':url}):
                added.append(self.add(name, url, sourceType, displayName, group, logo, headline))

        sources = [self.get(_id) for _id in added]
        return sources

    def get(self, _id):
        return self.mongo.newsSourceCollection.find_one({'_id': _id})

    def setUpdated(self, _id, last_updated=None):
        if not last_updated:
            last_updated = int(time.time())

        return self.mongo.newsSourceCollection.update({'_id': ObjectId(_id)},
                                               {'$set': {'last_updated': last_updated}})

    def delete(self, _id):
        return self.mongo.newsSourceCollection.remove({'_id': ObjectId(_id)})

    def getAllSources(self, priority=3):
        query = {'source_type':{'$in': [self.TYPE_ARTICLES, self.TYPE_LINKS]}}
        if priority == 1:
            query['headline'] = True
        else:
            query['headline'] = False
        allSources = list(self.mongo.newsSourceCollection.find(query))

        groups = {}

        for source in allSources:
            if not groups.has_key(source['group']):
                groups[source['group']] = []

            groups[source['group']].append(source)

        return groups.values()

    def getNewSources(self):
        allSources = list(self.mongo.newsSourceCollection.find({'last_updated': None}))
        groups = {}

        for source in allSources:
            if not groups.has_key(source['group']):
                groups[source['group']] = []

            groups[source['group']].append(source)

        return groups.values()

    def countDistinctGroups(self):
        res = self.mongo.newsSourceCollection.distinct('group')
        return len(res)

    def setIndex(self):
        self.mongo.newsSourceCollection.ensure_index([('url', pymongo.ASCENDING)], unique=True)

    def getAll(self):
        return list(self.mongo.newsSourceCollection.find())

    def getFeedSources(self):
        return list(self.mongo.newsSourceCollection.find({'source_type': {'$in': [self.TYPE_ARTICLES, self.TYPE_LINKS]}}))

    def getWebsiteSources(self):
        return list(self.mongo.newsSourceCollection.find({'source_type': self.TYPE_WEBSITE}))

    def update(self, source):
        row = {'name': source['name'], 'url': source['url'], 'source_type': int(source['source_type']),
               'display_name': source['display_name'], 'group': source['group'],
               'logo': source['logo'], 'headline': source.get('headline', False), 'pattern': source.get('pattern')}

        self.mongo.newsSourceCollection.update({'_id': ObjectId(source['_id'])}, {'$set': row})
