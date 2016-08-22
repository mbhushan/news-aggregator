'''
Created on Apr 21, 2015

@author: rsingh
'''

from flask import request, jsonify
from flask.views import MethodView

from NSLib.Config import config
from flask_login import current_user
from NSLib.Security.TypeChecker import is_empty_string
from NSLib.ErrorCodes.ErrorCodeManager import errorCodeManager
from NSLib.db.UserStories.UserStories import UserStories
from www.decorator import authenticated_user_required

class UserStoriesAPI(MethodView):

    decorator = [authenticated_user_required]

    def get(self, storyId):
        userStories = UserStories(config)
        story = userStories.findById(storyId)

        if not story:
            return jsonify({'status': 400, 'errorCode': 1001, 'message': 'No such story'}), 400

        if story['user_id'] != int(current_user.id):
            return jsonify({'status': 400, 'errorCode': 1001, 'message': 'You do not have the necessary permission.'}), 400

        story['_id'] = str(story['_id'])
        return jsonify({'story': story})

    def post(self):
        action = request.json.get('action')
        _id = request.json.get('_id')
        title = request.json.get('title')
        body = request.json.get('body')
        coverPic = request.json.get('cover_pic')
        tags = request.json.get('tags', [])

        if action not in ['publish', 'draft']:
            return jsonify({'status': 400, 'errorCode': 1001, 'message': errorCodeManager.getMessage(1001)}), 400

        if is_empty_string(title) or is_empty_string(body):
            return jsonify({'status': 400, 'errorCode': 1001, 'message': errorCodeManager.getMessage(1001)}), 400

        userStories = UserStories(config)
        userId = int(current_user.id)

        if _id is None:
            if action == 'draft':
                status = userStories.STATUS_DRAFT
                draft = {'title': title, 'body': body, 'cover_pic': coverPic, 'tags': tags}
                _id = userStories.add(userId, None, None, None, None, draft, status)

            if action == 'publish':
                status = userStories.STATUS_APPROVED
                _id = userStories.add(userId, title, body, coverPic, tags, None, status)
        else:
            #check if user owns this article
            article = userStories.findById(_id)
            if not (article and article['user_id'] == userId):
                return jsonify({'status': 400, 'errorCode': 1001, 'message': 'You do not have the necessary permission.'}), 400

            if action == 'draft':
                status = userStories.STATUS_DRAFT
                draft = {'title': title, 'body': body, 'cover_pic': coverPic, 'tags': tags}
                userStories.update(_id, userId, None, None, None, None, draft, status)

            if action == 'publish':
                status = userStories.STATUS_APPROVED
                userStories.update(_id, userId, title, body, coverPic, tags, None, status)

        return jsonify({'status': 200, '_id': str(_id)})

    def delete(self, storyId):
        userStories = UserStories(config)
        story = userStories.findById(storyId)

        if story:
            if story['user_id'] != int(current_user.id):
                return jsonify({'status': 400, 'errorCode': 1001, 'message': 'You do not have the necessary permission.'}), 400

            userStories.deleteById(storyId)
            return jsonify({'status': 200})

        return jsonify({'status': 400, 'errorCode': 1001, 'message': 'No such story'}), 400
