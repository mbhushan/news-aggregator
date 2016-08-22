'''
Created on Dec 14, 2014

@author: rsingh
'''
from flask_login import UserMixin
from flask_mongoengine import MongoEngine
from flask_security.core import RoleMixin, Security
from flask_security.datastore import MongoEngineDatastore, UserDatastore


mdb = MongoEngine()

# Define models
class Role(mdb.Document, RoleMixin):
    name = mdb.StringField(required=True, unique=True, max_length=80)
    description = mdb.StringField(max_length=255)

class User(mdb.Document, UserMixin):
    id = mdb.SequenceField(required=True, primary_key=True)
    email = mdb.StringField(required=True, unique=True, max_length=255)
    password = mdb.StringField(required=True, max_length=255)
    name = mdb.StringField(max_length=255)
    username = mdb.StringField(max_length=255)
    last_login_at = mdb.DateTimeField()
    current_login_at = mdb.DateTimeField()
    last_login_ip = mdb.StringField(max_length=100)
    current_login_ip = mdb.StringField(max_length=100)
    login_count = mdb.IntField()
    registered_at = mdb.DateTimeField()
    active = mdb.BooleanField(default=True)
    confirmed_at = mdb.DateTimeField()
    roles = mdb.ListField(mdb.ReferenceField(Role), default=[])
    registration_token = mdb.StringField(max_length=200)
    approved = mdb.BooleanField(default=False)
    social_connections = mdb.ListField(mdb.DictField(), default=[{}])
    profile_pic = mdb.StringField(max_length=350)
    bio = mdb.StringField(max_length=500)
    website = mdb.StringField(max_length=100)
    facebook_profile = mdb.StringField(max_length=100)
    twitter_profile = mdb.StringField(max_length=100)

    def __str__(self):
        return "User id:%s, email:%s" % (self.id, self.email)

class MongoEngineUserDatastore(MongoEngineDatastore, UserDatastore):
    """A MongoEngine datastore implementation for Flask-Security that assumes
    the use of the Flask-MongoEngine extension.
    """
    def __init__(self, db, user_model, role_model):
        MongoEngineDatastore.__init__(self, db)
        UserDatastore.__init__(self, user_model, role_model)

    def find_user(self, **kwargs):
        if kwargs.get('id'):
            kwargs['id'] = int(kwargs['id'])

        return self.user_model.objects(**kwargs).first()

    def find_role(self, role):
        return self.role_model.objects(name=role).first()

    def get_user(self, email):
        return self.user_model.objects(**{'email': email}).first()

    def search_user(self, query):
        return self.user_model.objects(__raw__=query).first()

# Setup Flask-Security
user_datastore = MongoEngineUserDatastore(mdb, User, Role)
