'''
Created on Feb 15, 2015

@author: rsingh
'''

from NSLib.Config import config
from NSLib.db.News.NewsSource import NewsSource
import json

if __name__ == '__main__':
    newsSource = NewsSource(config)
    newsSource.setIndex()
    newsSource.mongo.newsSourceCollection.remove({}, multi=True)

    f = open('sources.json')
    sources = json.load(f)

    for item in sources:
        if item['type'] == 'links':
            sourceType = newsSource.TYPE_LINKS
        else:
            sourceType = newsSource.TYPE_ARTICLES

        newsSource.add(item['name'], item['url'], sourceType, item['display_name'], item['group'])