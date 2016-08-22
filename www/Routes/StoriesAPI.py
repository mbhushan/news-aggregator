'''
Created on Dec 6, 2014

@author: rsingh
'''

from flask import request, jsonify
from flask.views import MethodView

import arrow
import time
from NSLib.Config import config
from NSLib.db.News.NewsArticle import NewsArticle
from flask_login import current_user
from NSLib.Logger import Logger

class StoriesAPI(MethodView):

    def get(self, storyId):
        log = Logger.getLogger(Logger.LOGGER_WEBSITE)
        newsArticle = NewsArticle(config)
        if storyId:
            try:
                story = newsArticle.getById(storyId)
                if story:
                    return jsonify({'story': newsArticle.formatStory(story)})

            except:
                pass

            #no story found
            return jsonify({'story': None})

        t = request.args.get('t')
        try:
            t = int(t)
        except:
            t = None

        articles = newsArticle.findByTime(t)

        if articles:
            ts = articles[-1]['published']
        else:
            ts = None

        resp = []
        for article in articles:
            resp.append(newsArticle.formatStory(article))

        return jsonify({'stories': resp, 't': ts})
