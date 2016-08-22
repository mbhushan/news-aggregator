#!/usr/bin/python
'''
Created on 31-Jan-2013

@author: rsingh
'''

from goose import Goose
import time

from NSLib.Config import config
from NSLib.Logger import Logger
from NSLib.db.News.ArticlesQueue import ArticlesQueue
from NSLib.db.News.NewsArticle import NewsArticle
from NSLib.db.News.NewsSource import NewsSource
import multiprocessing as mp
import requests
from BeautifulSoup import BeautifulSoup
import re
from urlparse import urljoin

log = Logger.getLogger(Logger.LOGGER_CONSOLE)

class WebsiteDownloader():

    def __init__(self):
        self.articlesQueue = ArticlesQueue(config)
        self.newsArticle = NewsArticle(config)
        self.goose = Goose({'browser_user_agent': 'Mozilla/5.0 (X11; Linux x86_64)'})

    def fetchAndParseLinks(self, url, pattern):
        try:
            r = requests.get(url)
            reg = re.compile(pattern, re.IGNORECASE)

            if r.status_code == 200:
                matched = []
                soup = BeautifulSoup(r.text)
                for link in soup.findAll('a'):
                    link_str = str(link.get('href'))

                    if reg.search(link_str):
                        if not link_str.startswith('http'):
                            link_str = urljoin(url, link_str)

                        matched.append(link_str)

                return matched
        except:
            log.info('Exception in proccessing %s' % url)

        return None

    def download(self, website):
        log.info("Processing %s" % website['url'])
        links = self.fetchAndParseLinks(website['url'], website['pattern'])
        links.reverse()

        for link in links:
            #print entry
            try:
                rawData = {}

                curTime = int(time.time())
                rawData['published'] = curTime - 60


                #setting current link value, used for checking dupes will be overridden later
                rawData['link'] = link
                rawData['feed_id'] = link

                # if already processed, don't process again
                if self.newsArticle.findByFeedId(link):
                    continue

                rawData['link'], rawData['title'], rawData['content'], rawData['photo'] = self._extractContent(link)

                if rawData['link'] is None or rawData['title'] is None or rawData['title'] == '':
                    continue

                log.info("feed link %s" % rawData['feed_id'])

                metadata = {'feed_id': rawData.get('feed_id'), 'link': rawData.get('link'), 'published': rawData.get('published'),
                                      'title': rawData.get('title'), 'summary': rawData.get('summary'), 'photo': rawData.get('photo'),
                                      'source_id': website['_id']}
                #print metadata
                self.articlesQueue.add(rawData['title'], rawData.get('content'), metadata)
                time.sleep(6)

            except:
                log.exception('failed to processes %s' % link)



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

        return r.url, article.title, text, photo

def process(website):
    d = WebsiteDownloader()

    try:
        d.download(website)

        newsSources = NewsSource(config)
        newsSources.setUpdated(website['_id'])
    except:
        log.exception('process failed')

if __name__ == '__main__':
    newsSources = NewsSource(config)
    processCount = len(newsSources.getWebsiteSources())
    log.info('*** Downloading %s groups ***' % processCount)
    pool = mp.Pool(processes=processCount)

    while True:
        startTime = time.time()
        sources = newsSources.getWebsiteSources()
        pool.map(process, sources)
        log.info('**** long sleep ***')
        log.info('** took %s ' % (time.time() - startTime))
        time.sleep(300)

