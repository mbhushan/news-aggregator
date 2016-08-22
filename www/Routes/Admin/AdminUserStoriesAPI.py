'''
Created on Feb 28, 2015

@author: rsingh
'''

from flask import request
from flask.views import MethodView
from www.decorator import admin_user_required

from NSLib.Config import config
from NSLib.MiscFunctions import stringify, jsonify
from NSLib.ErrorCodes.ErrorCodeManager import errorCodeManager
from NSLib.db.News.NewsTags import NewsTags
from NSLib.db.UserStories.UserStories import UserStories
from flask_login import current_user

class AdminUserStoriesAPI(MethodView):

    decorators = [admin_user_required]

    def get(self):
        t = request.args.get('t')
        status = request.args.get('status')

        try:
            t = int(t)
        except:
            t = None

        userStories = UserStories(config)
        stories = userStories.findAll(t, status)

        if stories:
            ts = stories[-1]['last_updated']
            stories = stringify(stories)
        else:
            ts = None

        return jsonify({'stories': stories, 't': ts})

    def post(self):
        _id = request.json.get('_id')
        action = request.json.get('action')
        userStories = UserStories(config)

        if action == 'approve':
            userStories.setStatus(_id, userStories.STATUS_APPROVED, current_user.username)
        else:
            userStories.setStatus(_id, userStories.STATUS_DISAPPROVED, current_user.username)

        return jsonify({'status': 200})

