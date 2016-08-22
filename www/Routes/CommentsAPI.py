'''
Created on Dec 6, 2014

@author: rsingh
'''

from flask import request, jsonify
from flask.views import MethodView

from NSLib.Config import config
from NSLib.db.News.NewsArticle import NewsArticle
from flask_login import current_user
from NSLib.Logger import Logger
from NSLib.db.Engagement.CommentStore import CommentStore
from NSLib.Security.TypeChecker import is_int
from NSLib.ErrorCodes.ErrorCodeManager import errorCodeManager
from NSLib.db.News.VideoCards import VideoCards
import time

class CommentsAPI(MethodView):

    def get(self):
        log = Logger.getLogger(Logger.LOGGER_WEBSITE)

        contentId = request.args.get('id')
        contentType = request.args.get('type')

        commentStore = CommentStore(config)

        if not contentId or contentType not in commentStore.VALID_CONTENT_TYPES:
            return jsonify({'status': 400, 'errorCode': 1001, 'message': errorCodeManager.getMessage(1001)}), 400

        if contentType == 'video_card':
            if not is_int(contentId):
                return jsonify({'status': 400, 'errorCode': 1001, 'message': errorCodeManager.getMessage(1001)}), 400

            contentId = int(contentId)

        comments = commentStore.loadCommentByContent(contentId, contentType)
        comments = [commentStore.format(comment) for comment in comments]

        if len(comments) < 20 and contentType == 'video_card':
            videoCards = VideoCards(config)
            row = videoCards.get(contentId)

            if row:
                yt_comments = [videoCards.formatComment(comment) for comment in row['comments']]
            else:
                yt_comments = []

            comments.extend(yt_comments)

        return jsonify({'comments': comments})

    def post(self):
        contentId = request.json.get('id')
        contentType = request.json.get('type')
        text = request.json.get('text')

        if not contentId or not contentType:
            return jsonify({'status': 400, 'errorCode': 1001, 'message': errorCodeManager.getMessage(1001)}), 400

        if text is None or text.strip() == '':
            return jsonify({'status': 400, 'errorCode': 1001, 'message': 'Comment can not be empty'}), 400

        if not current_user.is_authenticated():
            return jsonify({'status': 400, 'errorCode': 1001, 'message': 'You need to be logged in to post comment.'}), 400

        commentStore = CommentStore(config)
        text = text.strip()
        _id = commentStore.add(contentId, contentType, text, int(current_user.id))

        return jsonify({'comment': commentStore.format(commentStore.getById(_id))})


