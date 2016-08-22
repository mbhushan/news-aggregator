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

class TagsAPI(MethodView):

    decorators = [admin_user_required]

    def get(self):
        q = request.args.get('q')
        if q and q != '':
            nt = NewsTags(config)
            allTags = nt.search(q)

            return jsonify(stringify(allTags))

        return jsonify({'status': 400, 'errorCode': 1001, 'message': errorCodeManager.getMessage(1001)}), 400

    def put(self):
        _id = request.json.get('_id')
        tags = request.json.get('tags')
        case_sensitive = request.json.get('case_sensitive', False)

        if not _id or not tags or _id.strip() == '' or len(tags) == 0:
            return jsonify({'status': 400, 'errorCode': 1001, 'message': errorCodeManager.getMessage(1001)}), 400

        nt = NewsTags(config)
        tags = [tag.strip() for tag in tags]
        row = nt.update(_id.strip(), tags, case_sensitive)
        return jsonify(row)

    def post(self):
        _id = request.json.get('_id')
        tags = request.json.get('tags')
        case_sensitive = request.json.get('case_sensitive', False)

        if not _id or not tags or _id.strip() == '' or len(tags) == 0:
            return jsonify({'status': 400, 'errorCode': 1001, 'message': errorCodeManager.getMessage(1001)}), 400

        tags = [tag.strip() for tag in tags]

        nt = NewsTags(config)
        row = nt.add(_id.strip(), tags, case_sensitive)
        return jsonify(stringify(row))

    def delete(self):
        _id = request.json.get('_id')
        nt = NewsTags(config)
        nt.remove(_id)
        return jsonify({'status': 200})
