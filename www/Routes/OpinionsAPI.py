'''
Created on Apr 21, 2015

@author: rsingh
'''

from flask import request, jsonify, current_app
from flask.views import MethodView

from NSLib.Config import config
from flask_login import current_user
from NSLib.Logger import Logger
from NSLib.Security.TypeChecker import is_empty_string
from NSLib.ErrorCodes.ErrorCodeManager import errorCodeManager
from NSLib.db.UserStories.UserStories import UserStories
from werkzeug import LocalProxy
from NSLib.db.Engagement.RecommendStore import RecommendStore
import time

class OpinionsAPI(MethodView):

    def get(self, username=None):

        _security = LocalProxy(lambda: current_app.extensions['security'])
        _datastore = LocalProxy(lambda: _security.datastore)

        t = request.args.get('t')
        try:
            t = int(t)
        except:
            t = None

        curUser = None
        if current_user.is_authenticated():
            curUser = int(current_user.id)

        userStories = UserStories(config)

        allPosts = False #used when user is viewing his profile
        if username:
            user = _datastore.search_user({'username': username})
            if not user:
                return jsonify({'status': 400,'errorCode': 1001, 'message': 'User does not exist'}), 400


            allPosts = False
            if current_user.is_authenticated() and user.id == curUser:
                allPosts = True

            stories = userStories.findByUser(int(user.id), t, allPosts)
        else:
            stories = userStories.findAllPublished(t)

        if stories:
            if allPosts:
                ts = stories[-1]['added']
            else:
                ts = stories[-1]['published']
        else:
            ts = None

        stories = [userStories.format(story, curUser) for story in stories]

        return jsonify({'stories': stories, 't': ts})

class OpinionItemAPI(MethodView):

    def get(self, storyId):
        _security = LocalProxy(lambda: current_app.extensions['security'])
        _datastore = LocalProxy(lambda: _security.datastore)

        userStories = UserStories(config)
        story = userStories.findById(storyId)

        currentUserId = None
        if current_user.is_authenticated():
            currentUserId = int(current_user.id)

        #story does not exist and not story owner and unpublished
        if not story or (story['user_id'] != currentUserId and story['status'] != userStories.STATUS_APPROVED):
            return jsonify({'status': 400,'errorCode': 1001, 'message': 'Opinion does not exist'}), 400

        else:
            user = _datastore.search_user({'_id': story['user_id']})
            details = {'username': user.username, 'name': user.name, 'profile_pic': user.profile_pic, 'bio': user.bio,
                       'website': user.website, 'facebook_profile': user.facebook_profile,
                       'twitter_profile': user.twitter_profile}

            return jsonify({'story': userStories.format(story, currentUserId), 'user': details})


    def post(self, storyId):
        if not current_user.is_authenticated():
            return jsonify({'status': 400,'errorCode': 1001, 'message': 'Please log in to recommend this story.'}), 400

        recommendStore = RecommendStore(config)
        if recommendStore.hasRecommended(storyId, 'opinion', int(current_user.id)):
            return jsonify({'status': 200})

        else:
            recommendStore.recommend(storyId, 'opinion', int(current_user.id))

        return jsonify({'status': 200})


