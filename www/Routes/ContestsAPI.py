'''
Created on 29-Jan-2013

@author: roshan
'''

from flask.views import MethodView
from flask import render_template, current_app,session
from werkzeug import abort
from flask_login import current_user

from NSLib.Config import config
from NSLib.db.News.NewsArticle import NewsArticle
from NSLib.db.User.PinnedTopics import PinnedTopics
from NSLib.db.News.Weather import Weather
from NSLib.db.News.VideoCards import VideoCards
from NSLib.MiscFunctions import getLocationTopics, statesCities


from www.decorator import locate_user

class ContestsAPI(MethodView):

    def get(self, path=None, tag=None, storyId=None):
        userSettings = {}
        loggedIn = False


        if current_user.is_authenticated():
            loggedIn = True

            userSettings['id'] = int(current_user.id)
            userSettings['username'] = current_user.username or ""

        appSettings = {'facebook': config.facebookConfig.CONSUMER_KEY,
                       'google': config.googleConfig.CONSUMER_KEY,
                       'app_url': config.serverConfig.APP_URL,
                       'ver': current_app.config['INIT_TIME']}

        return render_template('contest.html', userSettings=userSettings, loggedIn=loggedIn,
                               appSettings=appSettings)
