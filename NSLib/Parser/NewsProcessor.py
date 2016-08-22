from NSLib.db.News.ArticlesQueue import ArticlesQueue
from NSLib.db.News.NewsArticle import NewsArticle
from NSLib.Config import config
from NSLib.Parser.TagParser import TagParser
from NSLib.Logger import Logger

class NewsProcessor:

    def __init__(self):
        self.arq = ArticlesQueue(config)
        self.newsAr = NewsArticle(config)
        self.log = Logger.getLogger(Logger.LOGGER_CONSOLE)

    def newsProcess(self):
        rdata = self.arq.getRawData()
        try:
            if rdata:
                self.log.info("Processing  %s" % str(rdata['_id']))
                tData = rdata['title']
                cData = rdata['content']

                tparser = TagParser(tData, True)
                titleTags, cityTags, stateTags = tparser.getTags()

                titleTags = list(set(titleTags)) #remove duplicates
                self.newsAr.add(rdata['metadata'], titleTags, cityTags, stateTags)

                self.arq.delete(rdata['_id'])
                return True
        except:
            self.log.exception("Failed to process news article %s", str(rdata['_id']))
        return False