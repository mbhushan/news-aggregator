'''
Created on 29-Jan-2013

@author: roshan
'''
from flask.views import MethodView
from flask import render_template

from NSLib.Config import config
from flask.globals import session
from flask_login import current_user
from NSLib.db.News.Weather import Weather
from www.decorator import locate_user
from NSLib.MiscFunctions import statesCities
from werkzeug import redirect


class DiscoverAPI(MethodView):
    decorators = [locate_user]

    def get(self, regionCode=None):
        if regionCode and not statesCities['states'].has_key(regionCode):
            return redirect('/discover')

        userSettings = {}
        loggedIn = False
        weather = Weather(config)
        weatherData = weather.getAll()

        if regionCode and statesCities['states'].has_key(regionCode):
            userSettings['regionCode'] = regionCode
        else:
            userSettings['regionCode'] = session.get('regionCode')

        if current_user.is_authenticated():
            userSettings['id'] = current_user.id
            userSettings['username'] = current_user.username or ""

            loggedIn = True

        appSettings = {'facebook': config.facebookConfig.CONSUMER_KEY,
                       'google': config.googleConfig.CONSUMER_KEY}

        return render_template('discover.html', userSettings=userSettings, loggedIn=loggedIn,
                               appSettings=appSettings, weatherData=weatherData)

