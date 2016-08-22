#!/usr/bin/python
'''
Created on 31-Jan-2013

@author: rsingh
'''

import feedparser, json
from goose import Goose
from time import mktime
import time

from NSLib.Config import config
from NSLib.Logger import Logger
from NSLib.db.News.ArticlesQueue import ArticlesQueue
from NSLib.db.News.NewsArticle import NewsArticle
from NSLib.db.News.NewsSource import NewsSource
import multiprocessing as mp
import requests
import sys
from NSLib.db.News.XMLSource import XMLSource

log = Logger.getLogger(Logger.LOGGER_CONSOLE)

class Downloader():

    def __init__(self):
        self.articlesQueue = ArticlesQueue(config)
        self.newsArticle = NewsArticle(config)
        self.goose = Goose({'browser_user_agent': 'Mozilla/5.0 (X11; Linux x86_64)'})

    def downloadFeed(self, source):
        d = feedparser.parse(source['path'])
        log.info("Processing %s" % source['path'])
        entries = d['entries']

        for entry in entries[:20]:
            #print entry
            try:
                rawData = {}
                if hasattr(entry, 'id'):
                    rawData['feed_id'] = entry.id
                else:
                    rawData['feed_id'] = entry.link

                rawData['title'] = entry.title

                curTime = int(time.time())
                if hasattr(entry, 'published_parsed'):
                    rawData['published'] = mktime(entry.published_parsed)

                    #handle this weird case of timestamp greater than now
                    if rawData['published'] > curTime:
                        rawData['published'] = curTime - 60

                else:
                    rawData['published'] = curTime - 60


                #setting current link value, used for checking dupes will be overridden later
                rawData['link'] = entry.link

                # if already processed, don't process again
                if self.newsArticle.checkIfAlreadyPresent(rawData, source):
                    continue

                rawData['summary'] = self.goose.extract(raw_html = entry.summary).cleaned_text
                rawData['link'], rawData['content'], rawData['photo'] = self._extractContent(entry.link)

                if rawData['link'] is None:
                    continue

                rawData['feed_source'] = source['_id']
                log.info("feed link %s" % rawData['feed_id'])

                metadata = {'feed_id': rawData.get('feed_id'), 'link': rawData.get('link'), 'published': rawData.get('published'),
                                      'title': rawData.get('title'), 'summary': rawData.get('summary'), 'photo': rawData.get('photo'),
                                      'source_id': source['_id']}

                self.articlesQueue.add(rawData['title'], rawData.get('content'), metadata)
                time.sleep(6)
            except:
                log.exception('failed to processes %s' % entry.link)



    def _extractContent(self, url):
        retry = 1

        while True:
            r = requests.get(url, allow_redirects = True, headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64)'})
            if r.status_code != 200:
                log.error("URL not retrieved %s, code %s" % (url, r.status_code))
                time.sleep(60)
                retry += 1
            else:
                break

            if retry == 3:
                return None, None, None

        raw_html = r.text
        article = self.goose.extract(raw_html=raw_html)

        text, photo = None, None
        if article.title:
            text = article.cleaned_text

        if article.top_image and article.top_image.src and \
            ( article.top_image.src.startswith('http://') or article.top_image.src.startswith('https://')) and \
            article.top_image.width > 150 and article.top_image.height > 150:

            photo = article.top_image.src

        return r.url, text, photo

if __name__ == '__main__':
    xmlSources = XMLSource(config)
    d = Downloader()

    while True:
        startTime = time.time()
        rows = xmlSources.getPendingRows()

        for row in rows:
            detail = xmlSources.getSourceDetail(row['group'])
            detail['path'] = row['path']
            d.downloadFeed(detail)
            xmlSources.setProcessed(row['_id'])

        log.info('**** long sleep ***')
        log.info('** took %s ' % (time.time() - startTime))
        time.sleep(300)

