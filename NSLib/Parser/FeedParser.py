import feedparser


class FeedParser:

    def __init__(self):
        self.urls = [
            "https://www.google.co.in/trends/hottrends/atom/feed?pn=p3",
            ]

    def initFeedData(self):
        titles = set([])
        for atom in self.urls:
            dat = feedparser.parse(atom)
            for i in range(len(dat.entries)):
                val = dat.entries[i].title
                val = val.encode("ascii")
                titles.add(val)
        return titles

    def getTrendingTitles(self):
        tags = self.initFeedData()
        return tags
