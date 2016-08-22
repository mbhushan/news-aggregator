from FeedParser import FeedParser


def main():
    fp = FeedParser()
    trending = fp.getTrendingTitles()
    for t in trending:
        print t + "\n"

if __name__ == '__main__':
    main()
