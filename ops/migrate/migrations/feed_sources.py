'''
Created on Jun 27, 2013

@author: rsingh
'''

from NSLib.Config import config
from NSLib.db.News.NewsSource import NewsSource
from NSLib.db.News.NewsArticle import NewsArticle
from NSLib.db.News.ArticlesQueue import ArticlesQueue

if __name__ == '__main__':
    newsSource = NewsSource(config)
    newsSource.setIndex()
    newsSource.add('IBN Live India', 'http://ibnlive.in.com/ibnrss/rss/india/india.xml', newsSource.TYPE_LINKS)
    newsSource.add('IBN Live Top', 'http://ibnlive.in.com/ibnrss/top.xml', newsSource.TYPE_LINKS)
    newsSource.add('IBN Live South', 'http://ibnlive.in.com/ibnrss/rss/ibnsouth/ibnsouth.xml', newsSource.TYPE_LINKS)

    newsSource.add('NDTV Top News', 'http://feeds.feedburner.com/NdtvNews-TopStories', newsSource.TYPE_LINKS)
    newsSource.add('NDTV India', 'http://feeds.feedburner.com/ndtv/Lsgd', newsSource.TYPE_LINKS)
    newsSource.add('NDTV Latest', 'http://feeds.feedburner.com/NDTV-LatestNews', newsSource.TYPE_LINKS)

    newsArticle = NewsArticle(config)
    newsArticle.setIndex()

    articlesQueue = ArticlesQueue(config)
    articlesQueue.setIndex()
