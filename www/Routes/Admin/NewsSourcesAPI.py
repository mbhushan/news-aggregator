'''
Created on Feb 28, 2015

@author: rsingh
'''

from flask import request
from flask.views import MethodView
from www.decorator import admin_user_required

from NSLib.db.News.NewsSource import NewsSource
from NSLib.Config import config
from NSLib.MiscFunctions import stringify, jsonify
from NSLib.ErrorCodes.ErrorCodeManager import errorCodeManager
import re
import requests
from BeautifulSoup import BeautifulSoup

class NewsSourcesAPI(MethodView):

    decorators = [admin_user_required]

    def get(self):
        ns = NewsSource(config)
        allSources = ns.getAll()

        return jsonify(stringify(allSources))

    def put(self):
        source = request.json
        ns = NewsSource(config)
        ns.update(source)
        return jsonify(source)

    def post(self):
        display_name = request.json.get('display_name')
        group = request.json.get('group')
        name = request.json.get('name')

        url = request.json.get('url')
        logo = request.json.get('logo')
        headline = request.json.get('headline', False)
        bulk_urls = request.json.get('bulk_urls')
        pattern = request.json.get('pattern')
        test = request.json.get('test')

        if test:
            res = self.validate(url, pattern)
            return jsonify({'result': res})

        source_type = int(request.json.get('source_type'))

        if source_type not in [1,2,3]:
            return jsonify({'status': 400, 'errorCode': 1001, 'message': errorCodeManager.getMessage(1001)}), 400

        ns = NewsSource(config)

        if url:
            _id = ns.add(name, url, source_type, display_name, group, logo, headline, pattern)
            return jsonify(stringify(ns.get(_id)))
        elif bulk_urls:
            sources = ns.addBulk(name, bulk_urls, source_type, display_name, group, logo, headline)
            return jsonify(stringify(sources))

    def delete(self):
        _id = request.json.get('_id')
        ns = NewsSource(config)
        ns.delete(_id)
        return jsonify({'status': 200})

    def validate(self, url, pattern):
        r = requests.get(url)
        reg = re.compile(pattern, re.IGNORECASE)

        if r.status_code == 200:
            matched = []
            soup = BeautifulSoup(r.text)
            for link in soup.findAll('a'):
                link_str = str(link.get('href'))

                if reg.search(link_str):
                    matched.append(link_str)

            if matched:
                return ", ".join(matched)
            else:
                return "No match found"

        else:
            return 'failed to fetch html'
