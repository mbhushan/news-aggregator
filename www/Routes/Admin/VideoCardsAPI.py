'''
Created on Apr 7, 2015

@author: rsingh
'''

from flask import request
from flask.views import MethodView
from www.decorator import admin_user_required

from NSLib.Config import config
from NSLib.MiscFunctions import stringify, jsonify
from NSLib.ErrorCodes.ErrorCodeManager import errorCodeManager
from NSLib.db.News.VideoCards import VideoCards

class VideoCardsAPI(MethodView):

    decorators = [admin_user_required]

    def get(self):
        vc = VideoCards(config)
        allSources = vc.getAll(1)

        return jsonify(stringify(allSources))

    def put(self):
        source = request.json
        vc = VideoCards(config)
        vc.edit(int(source.get('_id')), source.get('name'), source.get('url'), source.get('thumbnail'), source.get('description'))
        return jsonify(source)

    def post(self):
        name = request.json.get('name')
        url = request.json.get('url')
        thumbnail = request.json.get('thumbnail')
        description = request.json.get('description')

        vc = VideoCards(config)
        row = vc.add(name, url, thumbnail, description)
        return jsonify(row)

    def delete(self):
        _id = request.json.get('_id')
        vc = VideoCards(config)
        vc.remove(int(_id))

        return jsonify({'status': 200})



