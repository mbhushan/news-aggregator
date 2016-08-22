'''
Created on Dec 7, 2014

@author: rsingh
'''

from flask import request, jsonify
from flask.views import MethodView
from flask_login import current_user

from NSLib.Config import config
from NSLib.db.News.NewsArticle import NewsArticle
from NSLib.db.User.PinnedTopics import PinnedTopics

class TagStoriesAPI(MethodView):

    def get(self, tagId):
        newsArticle = NewsArticle(config)
        source = request.args.get('source')

        t = request.args.get('t')
        try:
            t = int(t)
        except:
            t = None

        if tagId == 'entertainment':
            tagId = 'movies'

        if source == 'discover':
            articles = newsArticle.findByTag(tagId, t, photosOnly=False)
        else:
            articles = newsArticle.findByTag(tagId, t)

        relatedTags = newsArticle.getRelatedTags(tagId)

        if articles:
            ts = articles[-1]['published']
        else:
            ts = None

        resp = []
        for article in articles:
            resp.append(newsArticle.formatStory(article, source=source))

        if current_user.is_authenticated():
            pinnedTopics = PinnedTopics(config)
            pinnedTopics.setLastSeen(int(current_user.id), tagId)

        return jsonify({'stories': resp, 't': ts, 'related_tags': relatedTags})
