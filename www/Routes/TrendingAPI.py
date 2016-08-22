'''
Created on Apr 3, 2015

@author: rsingh
'''

from flask.views import MethodView

from flask import jsonify

from NSLib.Config import config
from NSLib.db.News.NewsArticle import NewsArticle



class TrendingAPI(MethodView):

    def get(self):
        newsArticle = NewsArticle(config)


        trendingTags = newsArticle.getTrendingTags()
        return jsonify({'topics': trendingTags})