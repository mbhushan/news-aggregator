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

class TagSearchAPI(MethodView):

    def get(self):
        q = request.args.get('q')
        if q and q != '':
            nt = NewsTags(config)
            allTags = nt.search(q)

            return jsonify({'results': self.formatTags(allTags)})

        return jsonify({'results': []})

    def formatTags(self, tags):
        for tag in tags:
            tag['name'] = tag['_id']
            tag['tag'] = tag['tags'][0]

        finalTags = []
        for tag in tags:
            found = False
            for ft in finalTags:
                if tag['tag'] == ft['tag']:
                    if len(tag['name']) > len(ft['name']):
                        ft['name'] = tag['name']

                    found = True
                    break

            if not found:
                finalTags.append({'tag': tag['tag'], 'name': tag['name']})

        return finalTags