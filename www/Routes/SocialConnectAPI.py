'''
Created on Dec 14, 2014

@author: rsingh
'''

from flask import request, abort, redirect, flash, session, current_app, after_this_request
from flask.views import MethodView
from flask.ext.login import current_user, login_user
import twitter
import urlparse
import urllib

from NSLib.Config import config
from werkzeug import LocalProxy
from www.login.models import User
from NSLib.MiscFunctions import get_unique_string
from flask.ext.principal import identity_changed, Identity
from flask_security.views import _commit
from flask_security.confirmable import confirm_user
import requests
import facebook
import json
from flask.json import jsonify
from datetime import datetime

# Convenient references
_security = LocalProxy(lambda: current_app.extensions['security'])

_datastore = LocalProxy(lambda: _security.datastore)

class SocialConnectAPI(MethodView):

    def get(self, sn):
        if sn == 'twitter':
            #user denied permission or necessary params did not come in
            if request.args.has_key('denied') or not request.args.has_key('oauth_verifier'):
                flash("We were not able to connect your twitter account.", "error")
                return redirect('/login')

            request_token = session['twitter_token']
            token = twitter.oauth.Token(request_token['oauth_token'], request_token['oauth_token_secret'])
            token.set_verifier(request.args.get('oauth_verifier'))

            consumer = twitter.oauth.Consumer(config.twitterConfig.CONSUMER_KEY, config.twitterConfig.CONSUMER_SECRET)
            client = twitter.oauth.Client(consumer, token)

            resp, content = client.request(twitter.ACCESS_TOKEN_URL, "POST")
            del session['twitter_token']

            if content != None or content != "" :
                access_token = dict(urlparse.parse_qsl(content))

                if access_token.has_key('screen_name') and access_token.has_key('oauth_token'):
                    user = _datastore.search_user({'social_connections.provider': 'twitter', 'social_connections.id': access_token['user_id']})

                    if not user:
                        user = _datastore.create_user(**{'email': 'user_%s@nationstory.com' % get_unique_string(),
                                            'password': get_unique_string(),
                                            'social_connections': [{'provider': 'twitter',
                                                                    'id': access_token['user_id'],
                                                                    'access_token': access_token['oauth_token'],
                                                                    'oauth_token_secret': access_token['oauth_token_secret'],
                                                                    'username': access_token['screen_name']}]})
                        confirm_user(user)
                        flash("Your twitter account has been connected successfully!", "success")

                    login_user(user)
                    identity_changed.send(current_app._get_current_object(),
                                          identity=Identity(user.id))

                else:

                    flash("Something went wrong while trying to connect your twitter account.", "error")
            else:
                flash("Something went wrong while trying to connect your twitter account.", "error")

        elif sn == 'facebook':
            if request.args.get('error') or not request.args.get('code'):
                flash("We were not able to connect your facebook account.", "error")
                return redirect('/login')

            callbackURL = config.serverConfig.APP_URL + '/register/facebook'
            resp = facebook.get_access_token_from_code(request.args.get('code'), callbackURL,
                                                       config.facebookConfig.CONSUMER_KEY,config.facebookConfig.CONSUMER_SECRET)

            graphApi = facebook.GraphAPI(resp['access_token'])
            result = graphApi.get_object("me")

            user = _datastore.search_user({'social_connections.provider': 'facebook', 'social_connections.id': result['id']})
            if not user:
                user = _datastore.create_user(**{'email': 'user_%s@nationstory.com' % get_unique_string(),
                                            'password': get_unique_string(),
                                            'social_connections': [{'provider': 'facebook',
                                                                    'id': result['id'],
                                                                    'access_token': resp['access_token'],
                                                                    'username': result['name']}]})
                flash("Your facebook account has been connected successfully!", "success")
                confirm_user(user)

            login_user(user)
            identity_changed.send(current_app._get_current_object(),
                                  identity=Identity(user.id))

        return redirect('/')

    def post(self, sn):
#         if sn == 'twitter':
#             consumer = twitter.oauth.Consumer(config.twitterConfig.CONSUMER_KEY, config.twitterConfig.CONSUMER_SECRET)
#             client = twitter.oauth.Client(consumer)
#             callbackURL = config.serverConfig.APP_URL + '/register/twitter'
#
#             resp, content = client.request(twitter.REQUEST_TOKEN_URL, 'POST',body=urllib.urlencode({'oauth_callback':callbackURL}))
#
#             if resp['status'] != '200':
#                 return "Failed to connect twitter"
#             else:
#                 request_token = dict(urlparse.parse_qsl(content))
#                 session['twitter_token'] = request_token
#                 session.modified = True
#                 redirect_url = "%s?oauth_token=%s" % (twitter.AUTHORIZATION_URL, request_token['oauth_token'])
#                 return redirect(redirect_url, 302)

        if sn == 'facebook':
            access_token = request.form.get('token')
            if access_token == None or access_token == '':
                return jsonify({'status': 400}), 400

            try:
                graphApi = facebook.GraphAPI(access_token)
                result = graphApi.get_object("me")
            except:
                return jsonify({'status': 400}), 400

            #if fb account is already connected
            user = _datastore.search_user({'social_connections.provider': 'facebook', 'social_connections.id': result['id']})
            if not user:
                #if email is already connected
                user = _datastore.search_user({'email': result['email']})

                if user:
                    user.social_connections.append({'provider': 'facebook',
                                                'id': result['id'],
                                                'access_token': access_token,
                                                'name': result['name']})
                    _datastore.put(user)
                #new user
                else:
                    user = _datastore.create_user(**{'email': result['email'],
                                            'password': get_unique_string(),
                                            'name': result['name'],
                                            'profile_pic': 'https://graph.facebook.com/%s/picture?type=large' % result['id'],
                                            'social_connections': [{'provider': 'facebook',
                                                                    'id': result['id'],
                                                                    'access_token': access_token,
                                                                    'name': result['name']}]})
                    confirm_user(user)

                flash("Your facebook account has been connected successfully!", "success")

            login_user(user)
            self.track(user)
            identity_changed.send(current_app._get_current_object(),
                                      identity=Identity(user.id))

            return jsonify({'status': 200})


        elif sn == 'google':
            access_token = request.form.get('token')
            if access_token == None or access_token == '':
                return jsonify({'status': 400}), 400

            url = 'https://www.googleapis.com/plus/v1/people/me?access_token=%s' % access_token

            resp = requests.get(url)
            if resp.status_code == 200:
                details = json.loads(resp.text)

                if details.has_key('error'):
                    return jsonify({'status': 400}), 400

                #if google account already connected
                user = _datastore.search_user({'social_connections.provider': 'google', 'social_connections.id': details['id']})
                if not user:
                    email = details['emails'][0]['value']
                    for e in details['emails']:
                        if e['type'] == 'account':
                            email = e['value']
                            break

                    #check if email already exists
                    user = _datastore.search_user({'email': email})
                    if user:
                        user.social_connections.append({'provider': 'google',
                                                    'id': details['id'],
                                                    'access_token': access_token,
                                                    'name': details['displayName']})
                        _datastore.put(user)

                    #new user
                    else:
                        profile_pic = details['image']['url']
                        profile_pic = profile_pic.split('?')[0]

                        user = _datastore.create_user(**{'email': email,
                                                'password': get_unique_string(),
                                                'name': details['displayName'],
                                                'profile_pic': profile_pic,
                                                'social_connections': [{'provider': 'google',
                                                                        'id': details['id'],
                                                                        'access_token': access_token,
                                                                        'name': details['displayName']}]})


                        confirm_user(user)
                    flash("Your google account has been connected successfully!", "success")

                login_user(user)
                self.track(user)
                identity_changed.send(current_app._get_current_object(),
                                      identity=Identity(user.id))

                return jsonify({'status': 200})

        return jsonify({'status': 400}), 400

    def track(self, user):
        if _security.trackable:
            if 'X-Forwarded-For' not in request.headers:
                remote_addr = request.remote_addr or 'untrackable'
            else:
                remote_addr = request.headers.getlist("X-Forwarded-For")[0]

            old_current_login, new_current_login = user.current_login_at, datetime.utcnow()
            old_current_ip, new_current_ip = user.current_login_ip, remote_addr

            user.last_login_at = old_current_login or new_current_login
            user.current_login_at = new_current_login
            user.last_login_ip = old_current_ip or new_current_ip
            user.current_login_ip = new_current_ip
            user.login_count = user.login_count + 1 if user.login_count else 1

            _datastore.put(user)
