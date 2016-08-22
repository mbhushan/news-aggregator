#!/usr/bin/python
'''
Created on 31-Jan-2013

@author: rsingh
'''

import feedparser, json
from goose import Goose
from time import mktime
import time
import urllib2

from NSLib.Config import config
from NSLib.Logger import Logger
from NSLib.db.News.ArticlesQueue import ArticlesQueue
from NSLib.db.News.NewsArticle import NewsArticle
from NSLib.db.News.NewsSource import NewsSource
import multiprocessing as mp
import requests
from Downloader import Downloader

log = Logger.getLogger(Logger.LOGGER_CONSOLE)

def process(groups):
    d = Downloader()
    curTime = int(time.time())

    for source in groups:
        try:
            d.downloadFeed(source)

            nsource = NewsSource(config)
            nsource.setUpdated(source['_id'], curTime)
        except:
            log.info('process failed')

if __name__ == '__main__':
    newsSources = NewsSource(config)
    processCount = newsSources.countDistinctGroups()
    pool = mp.Pool(processes=processCount+2)

    while True:
        groups = newsSources.getNewSources()
        pool.map(process, groups)
        log.info('**** long sleep ***')
        time.sleep(300)
