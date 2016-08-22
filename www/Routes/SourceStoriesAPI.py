'''
Created on Apr 6, 2015

@author: rsingh
'''
from flask import request, jsonify
from NSLib.Config import config
from NSLib.db.News.NewsArticle import NewsArticle
from flask.views import MethodView

class SourceStoriesAPI(MethodView):

    def get(self, source):
        t = request.args.get('t')
        try:
            t = int(t)
        except:
            t = None

        na = NewsArticle(config)
        newsSource = na.getSourceByGroupName(source)

        if newsSource:

            articles = na.findBySource(newsSource['_id'], t)

            if articles:
                ts = articles[-1]['published']
            else:
                ts = None

            resp = []
            for article in articles:
                resp.append(na.formatStory(article))

            return jsonify({'stories': resp, 't': ts})

        return jsonify({'status': 400, 'errorCode': 1001, 'message': 'Source does not exist'}), 400

