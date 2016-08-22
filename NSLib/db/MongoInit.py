'''
Created on 31-Jan-2013

@author: rsingh
'''

import pymongo

class MongoInit(object):
    '''Base class for mongo'''
    def __init__(self, config=None, host=None, port=None):
        if config:
            host = config.mongoConfig.HOST
            port = config.mongoConfig.PORT

        elif host is not None and port is not None:
            pass

        else:
            raise ValueError("No config or host/port pair received")

        self.mongoConnection = pymongo.MongoClient(host, port)

        self.mongodb = self.mongoConnection['nation_story']
        self.userCollection = self.mongodb['user']
        self.configCollection = self.mongodb['config']
        self.pinnedTopicCollection = self.mongodb['pinned_topics']
        self.autoIncStoreCollection = self.mongodb['auto_inc_store']


        self.newsSourceDb = self.mongoConnection['news_source']
        self.newsSourceCollection = self.newsSourceDb['sources']
        self.newsXmlSourceCollection = self.newsSourceDb['xml_sources']
        self.newsArticlesCollection = self.newsSourceDb['articles']
        self.articlesQueueCollection = self.newsSourceDb['articles_queue']
        self.weatherCollection = self.newsSourceDb['weather']
        self.videoCardCollection = self.newsSourceDb['video_cards']


        self.tagsDb = self.mongoConnection['tags']
        self.tagsCollection = self.tagsDb['tags']
        self.indianCitiesTagsCollection = self.tagsDb['indian_cities']
        self.indianStatesTagsCollection = self.tagsDb['indian_states']

        self.userStoriesDb = self.mongoConnection['user_stories']
        self.userStoriesCollection = self.userStoriesDb['stories']

        #comments
        self.engagementDb = self.mongoConnection['engagement']
        self.commentsCollection = self.engagementDb['comments']
        self.recommendationCollection = self.engagementDb['recommendations']

    def __del__(self):
        try:
            self.mongodbConnection.close()
        except:
            pass
