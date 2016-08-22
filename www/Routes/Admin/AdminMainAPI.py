'''
Created on 29-Jan-2013

@author: roshan
'''
from flask.views import MethodView
from flask import render_template

from NSLib.Config import config
from flask_login import current_user
from www.decorator import admin_user_required
from flask import current_app

class AdminMainAPI(MethodView):

    decorators = [admin_user_required]

    def get(self, path=None):
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

        return render_template('admin.html', userSettings=userSettings, loggedIn=loggedIn,
                               appSettings=appSettings)