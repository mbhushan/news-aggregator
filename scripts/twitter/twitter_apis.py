import twitter
import json


def authorize():
    CONSUMER_KEY = 'aCBjyXAOzjj1xQ1G6lIQhBocr'
    CONSUMER_SECRET = 'HnUJSv8Gfei9u1y3l7o7a8vnZZMkMci1UWX8z3ovzRuEGxpy0g'
    OAUTH_TOKEN = '21769507-oogia3xOf48sn96DqV5Mf4qb3a83cevz22242ABeT'
    OAUTH_TOKEN_SECRET = '9TghxlZgwOtP8fila8IPDhywedAAFAJnjjKqcfomnTSnh'

    auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET,
                               CONSUMER_KEY, CONSUMER_SECRET)

    twitter_api = twitter.Twitter(auth=auth)

    print twitter_api
    return twitter_api


def getTrending(woeid):
    tapi = authorize()
    trends = tapi.trends.place(_id=woeid)
    return trends


def prettyOutput(trends):
    print json.dumps(trends, indent=1)


def main():
    IND_WOEID = 23424848
    indTrend = getTrending(IND_WOEID)
    print "India Trends", prettyOutput(indTrend)

if __name__ == '__main__':
    main()
