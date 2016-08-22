'''
Created on Dec 13, 2014

@author: rsingh
'''
from pymongo.read_preferences import ReadPreference
from NSLib.Config import config

SECRET_KEY = '32rd3da3aoi8327adhj'

MONGODB_SETTINGS = {
    'db': 'nation_story',
    'host': 'mongodb://%s' % config.mongoConfig.HOST,
    'port': config.mongoConfig.PORT,
    'read_preference': ReadPreference.PRIMARY
}

SECURITY_REGISTERABLE = True
SECURITY_CONFIRMABLE = True
SECURITY_RECOVERABLE = True
SECURITY_TRACKABLE = True
DEFAULT_MAIL_SENDER = 'noreply@nationstory.com'
SECURITY_EMAIL_SENDER = 'noreply@nationstory.com'
SECURITY_PASSWORD_HASH = 'bcrypt'
SECURITY_PASSWORD_SALT = 'asjd21wde1ebae2kb3'
SECURITY_CONFIRM_EMAIL_WITHIN = '2 days'
#SECURITY_MSG_CONFIRM_REGISTRATION = 'Thank you. We are right now in a closed beta. We will get in touch soon.', ''
SECURITY_POST_REGISTER_VIEW = '/register'
SECURITY_POST_LOGIN_VIEW = '/'
SECURITY_POST_LOGOUT_VIEW = '/'

SECURITY_POST_LOGIN_VIEW = '/'
SQLALCHEMY_DATABASE_URI = 'mongodb://localhost:27017/nation_story'

SOCIAL_CONNECT_ALLOW_VIEW = '/profile'

MAIL_SERVER = 'smtp.mandrillapp.com'
MAIL_PORT = 2525
MAIL_USE_TLS = True
MAIL_USE_SSL = False
MAIL_USERNAME = 'singh.roshan08@gmail.com'
MAIL_PASSWORD = 't9wKf2NE1GbpOGw4ImF7cg'
