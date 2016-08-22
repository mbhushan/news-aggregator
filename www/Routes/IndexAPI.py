'''
Created on 29-Jan-2013

@author: roshan
'''

from flask.views import MethodView
from flask import render_template, current_app,session
from werkzeug import abort, LocalProxy
from flask_login import current_user

from NSLib.Config import config
from NSLib.db.News.NewsArticle import NewsArticle
from NSLib.db.User.PinnedTopics import PinnedTopics
from NSLib.db.News.Weather import Weather
from NSLib.db.News.VideoCards import VideoCards
from NSLib.MiscFunctions import getLocationTopics, statesCities
from datetime import datetime

from www.decorator import locate_user
from NSLib.db.UserStories.UserStories import UserStories

class IndexAPI(MethodView):

    decorators = [locate_user]

    def get(self, path=None, tag=None, storyId=None, username=None):
        userSettings = {}
        loggedIn = False

        newsArticle = NewsArticle(config)

        if path and path not in ['all', 'contact', 'about', 'aboutus', 'write', 'opinions']:
            if not newsArticle.getSourceByGroupName(path):
                abort(404)

        topics = getLocationTopics(session['city'], session['region'], session['regionCode'])
        topics = [{'name': topic, 'count': newsArticle.getDailyCount(topic)} for topic in topics]
        userSettings['location_topics'] = topics

        videoCards = VideoCards(config)
        userSettings['video_cards'] = videoCards.getAll(1)

        articles = newsArticle.findHeadlinesByTime()
        if articles:
            ts = articles[-1]['published']
        else:
            ts = None

        resp = []
        for article in articles:
            resp.append(newsArticle.formatStory(article))

        headlines = {'stories': resp, 't': ts}

        if current_user.is_authenticated():
            loggedIn = True

            userSettings['id'] = int(current_user.id)
            userSettings['username'] = current_user.username or ""

            if userSettings['username'] == '':
                userSettings['suggested'] = self.getUsernameSuggestion(current_user)

            userSettings['email'] = current_user.email
            userSettings['name'] = current_user.name
            userSettings['bio'] = current_user.bio
            userSettings['profile_pic'] = current_user.profile_pic
            userSettings['website'] = current_user.website
            userSettings['twitter_profile'] = current_user.twitter_profile
            userSettings['facebook_profile'] = current_user.facebook_profile

            pinnedTopics = PinnedTopics(config)
            pinnedUserTopics = pinnedTopics.getTopics(userSettings['id'])

            if pinnedUserTopics:
                for pinnedTopic in pinnedUserTopics:
                    pinnedTopic['count'] = newsArticle.countTaggedStories(pinnedTopic['name'], pinnedTopic['last_seen'])
                    if pinnedTopic['count'] > 99:
                        pinnedTopic['count'] = '99+'

                userSettings['topics'] = pinnedUserTopics
            else:
                userSettings['topics'] = []
        else:
            userSettings['topics'] = topics


        trendingTags = newsArticle.getTrendingTags()
        userSettings['trending'] = trendingTags
        weather = Weather(config)

        weatherData = weather.get(statesCities['states'][session['regionCode']][0].lower())

        userStories = UserStories(config)
        opinions = userStories.getFive()
        opinions = [userStories.format(story, userSettings.get('id')) for story in opinions]


        appSettings = {'facebook': config.facebookConfig.CONSUMER_KEY,
                       'google': config.googleConfig.CONSUMER_KEY,
                       'app_url': config.serverConfig.APP_URL,
                       'ver': current_app.config['INIT_TIME'],
                       'weather': weatherData,
                       'headlines': headlines,
                       'opinions': opinions}

        return render_template('home.html', userSettings=userSettings, loggedIn=loggedIn,
                               appSettings=appSettings, regionCode=session['regionCode'])

    def getUsernameSuggestion(self, current_user):
        _security = LocalProxy(lambda: current_app.extensions['security'])
        _datastore = LocalProxy(lambda: _security.datastore)

        username = current_user.name.lower().strip().replace(' ', '_')
        if username == '':
            now = datetime.utcnow()
            username = 'nsuser%s' % now.strftime('%Y%m%d')

        count = 1

        while True:
            if _datastore.search_user({'username': username}):
                username = '%s_%s' % (username, count)
                count += 1
            else:
                break

        current_user.username = username
        _datastore.put(current_user)

        return username



