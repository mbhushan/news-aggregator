'''
Created on Dec 27, 2014

@author: rsingh
'''

from flask import request, jsonify
from flask.views import MethodView

import arrow
import time
from NSLib.Config import config
from NSLib.db.News.NewsArticle import NewsArticle
from NSLib.ErrorCodes.ErrorCodeManager import errorCodeManager
from flask_login import current_user
from www.decorator import authenticated_user_required


class VoteAPI(MethodView):

    decorators = [authenticated_user_required]

    def post(self, storyId, voteType):
        if voteType not in ['upvote', 'downvote']:
            return jsonify({'status': 400, 'errorCode': 1001, 'message': errorCodeManager.getMessage(1001)})

        newsArticle = NewsArticle(config)
        article = newsArticle.getById(storyId)

        uid = int(current_user.id)
        upvoted = uid in article['up_votes']
        downvoted = uid in article['down_votes']

        if voteType == 'upvote' and upvoted:
            return jsonify({'status': 400, 'errorCode': 1050, 'message': errorCodeManager.getMessage(1050)})

        if voteType == 'downvote' and downvoted:
            return jsonify({'status': 400, 'errorCode': 1051, 'message': errorCodeManager.getMessage(1051)})

        votes = article['votes']
        if voteType == 'upvote':
            article['up_votes'].append(uid)
            votes += 1

            if downvoted:
                votes += 1
                article['down_votes'].remove(uid)

        else:
            article['down_votes'].append(uid)
            votes -= 1

            if upvoted:
                votes -= 1
                article['up_votes'].remove(uid)


        newsArticle.saveVotes(storyId, votes, article['up_votes'], article['down_votes'])

        resp = {'status': 200, 'votes': votes, 'upvoted': False, 'downvoted': False}

        if voteType == 'upvote':
            resp['upvoted'] = True
        else:
            resp['downvoted'] = True

        return jsonify(resp)
