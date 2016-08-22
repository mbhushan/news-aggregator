'''
Created on Dec 13, 2014

@author: rsingh
'''

from functools import wraps

from flask import Response, request, session
from flask_login import current_user
from werkzeug import abort
from NSLib.MiscFunctions import getIpToLocation

_default_unauthorized_html = """
    <h1>Unauthorized</h1>
    <p>The server could not verify that you are authorized to access the URL
    requested. You either supplied the wrong credentials (e.g. a bad password),
    or your browser doesn't understand how to supply the credentials required.</p>
    """


def _get_unauthorized_response(text=None, headers=None):
    text = text or _default_unauthorized_html
    headers = headers or {}
    return Response(text, 401, headers)


def authenticated_user_required(fn):
    """Decorator that protects endpoints using token authentication. The token
    should be added to the request by the client by using a query string
    variable with a name equal to the configuration value of
    `SECURITY_TOKEN_AUTHENTICATION_KEY` or in a request header named that of
    the configuration value of `SECURITY_TOKEN_AUTHENTICATION_HEADER`
    """

    @wraps(fn)
    def decorated(*args, **kwargs):
        if not request.is_xhr:
            return _get_unauthorized_response()

        if current_user.is_authenticated():
            return fn(*args, **kwargs)

        return _get_unauthorized_response()

    return decorated


_not_found_text = """
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">
<title>404 Not Found</title>
<h1>Not Found</h1>
<p>The requested URL was not found on the server.  If you entered the URL manually please check your spelling and try again.</p>
"""

def admin_user_required(fn):
    """Decorator that protects endpoints using token authentication. The token
    should be added to the request by the client by using a query string
    variable with a name equal to the configuration value of
    `SECURITY_TOKEN_AUTHENTICATION_KEY` or in a request header named that of
    the configuration value of `SECURITY_TOKEN_AUTHENTICATION_HEADER`
    """

    @wraps(fn)
    def decorated(*args, **kwargs):
        if current_user.is_authenticated():
            if current_user.email in ['roshn.singh@gmail.com', 'manibhushan.cs@gmail.com']:
                return fn(*args, **kwargs)

        return abort(404)

    return decorated

def locate_user(fn):
    @wraps(fn)
    def decorated(*args, **kwargs):
        if not session.get('regionCode'):
            location = getIpToLocation(request.remote_addr)

            if location:
                session['regionCode'] = location['regionCode']
                session['region'] = location['region']
                session['city'] = location['city']
            else:
                session['regionCode'] = 'DL'
                session['region'] = 'delhi'
                session['city'] = 'delhi'

        return fn(*args, **kwargs)

    return decorated

