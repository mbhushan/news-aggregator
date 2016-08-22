'''
Created on Dec 6, 2014

@author: rsingh
'''

from flask import request, jsonify, session
from flask.views import MethodView
from flask_login import current_user

from NSLib.db.User.PinnedTopics import PinnedTopics
from NSLib.Config import config
from NSLib.ErrorCodes.ErrorCodeManager import errorCodeManager

from www.decorator import authenticated_user_required, locate_user
from NSLib.db.News.NewsArticle import NewsArticle
from NSLib.MiscFunctions import getLocationTopics

class PinnedTopicAPI(MethodView):

    decorators = [authenticated_user_required]

    def post(self):
        topic = request.json.get('topic')
        action = request.json.get('action')
        if topic == None or topic is '' or action not in ['add', 'remove']:
            return jsonify({'status': 400, 'errorCode': 1001, 'message': errorCodeManager.getMessage(1001)}), 400

        uid = int(current_user.id)

        pinnedTopics = PinnedTopics(config)
        if action == 'add':
            pinnedTopics.add(uid, topic)
        else:
            pinnedTopics.remove(uid, topic)

        return jsonify({'status': 200})

class PinnedTopicPublicAPI(MethodView):
    decorators = [locate_user]

    def get(self):
        userSettings = {}
        loggedIn = False

        pinnedUserTopics = []
        newsArticle = NewsArticle(config)
        if current_user.is_authenticated():
            loggedIn = True

            userSettings['id'] = int(current_user.id)
            userSettings['username'] = current_user.username or ""

            pinnedTopics = PinnedTopics(config)
            pinnedUserTopics = pinnedTopics.getTopics(userSettings['id'])

            if pinnedTopics:

                for pinnedTopic in pinnedUserTopics:
                    pinnedTopic['count'] = newsArticle.countTaggedStories(pinnedTopic['name'], pinnedTopic['last_seen'])
                    if pinnedTopic['count'] > 99:
                        pinnedTopic['count'] = '99+'
        else:
            pinnedUserTopics = getLocationTopics(session['city'], session['region'], session['regionCode'])
            pinnedUserTopics = [{'name': topic, 'count': newsArticle.getDailyCount(topic)} for topic in pinnedUserTopics]

        return jsonify({'topics': pinnedUserTopics})


