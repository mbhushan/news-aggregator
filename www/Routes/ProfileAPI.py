'''
Created on Dec 27, 2014

@author: rsingh
'''
from flask.views import MethodView
from flask import request, jsonify, current_app

import re
from NSLib.Config import config
from flask_login import current_user
from werkzeug.local import LocalProxy
from www.decorator import authenticated_user_required,\
    _get_unauthorized_response
from flask.helpers import flash

_security = LocalProxy(lambda: current_app.extensions['security'])
_datastore = LocalProxy(lambda: _security.datastore)

class ProfileAPI(MethodView):

    def get(self, username):
        user = _datastore.search_user({'username': username})
        if user:
            details = {'username': user.username, 'name': user.name, 'profile_pic': user.profile_pic, 'bio': user.bio,
                       'website': user.website, 'facebook_profile': user.facebook_profile,
                       'twitter_profile': user.twitter_profile}

            return jsonify({'user': details})
        else:
            return jsonify({'status': 400, 'message': 'User does not exist.'}), 400

    def post(self, username=None):
        if not current_user.is_authenticated():
            return _get_unauthorized_response()

        username = request.form.get("username")
        name = request.form.get("name")
        bio = request.form.get("bio")
        website = request.form.get("website")
        facebook_profile = request.form.get("facebook_profile")
        twitter_profile = request.form.get("twitter_profile")

        if not username or not self.check_username(username):
            return jsonify({'status': 400, 'message': 'Username can only contain alphablets or numbers.'}), 400

        if not name or name.strip() == '':
            return jsonify({'status': 400, 'message': 'Name can not be empty.'}), 400

        name = name.strip()
        username = username.strip()

        user = _datastore.find_user(**{'id': current_user.id})

        if user.username == username:
            pass
        else:
            exists = _datastore.search_user({'username': username})
            if exists:
                return jsonify({'status': 400, 'message': 'This username is not available.'}), 400

        user.username = username
        user.name = name
        user.bio = bio
        user.website = website
        user.facebook_profile = facebook_profile
        user.twitter_profile = twitter_profile

        _datastore.put(user)

        flash("Your profile has been updated.", "success")
        return jsonify({'status': 200})

    def check_username(self, username):
        if re.match("^[a-z0-9_]+$", username):
            return True

        return False
