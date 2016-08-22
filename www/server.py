'''
Created on 29-Jan-2013

@author: roshan
'''

from flask import Flask
from flask.ext.assets import Environment


import www.settings
from flask.ext.sqlalchemy import SQLAlchemy
from NSLib.Config import config

from flask import render_template
from flask.ext.mongoengine import MongoEngine
from flask.ext.security import Security

from flask.ext.login import current_user
from flask_mail import Mail
from www.login.models import mdb, user_datastore
from datetime import timedelta
import json, time

#views
from www.Routes.IndexAPI import IndexAPI
from www.Routes.StoriesAPI import StoriesAPI
from www.Routes.TagStoriesAPI import TagStoriesAPI
from www.Routes.SocialConnectAPI import SocialConnectAPI
from www.Routes.ProfileAPI import ProfileAPI
from www.Routes.VoteAPI import VoteAPI
from www.Routes.DiscoverAPI import DiscoverAPI
from www.Routes.PinnedTopicAPI import PinnedTopicAPI, PinnedTopicPublicAPI
from www.Routes.TagSearchAPI import TagSearchAPI
from www.Routes.HeadlinesAPI import HeadlinesAPI
from www.Routes.FeedbackAPI import FeedbackAPI
from www.Routes.TrendingAPI import TrendingAPI
from www.Routes.SourceStoriesAPI import SourceStoriesAPI
from www.Routes.ContestsAPI import ContestsAPI
from www.Routes.CommentsAPI import CommentsAPI
from www.Routes.UserStoriesAPI import UserStoriesAPI
from www.Routes.OpinionsAPI import OpinionsAPI, OpinionItemAPI
from www.Routes.ImageUploadAPI import ImageUploadAPI

#admin views
from www.Routes.Admin.AdminMainAPI import AdminMainAPI
from www.Routes.Admin.NewsSourcesAPI import NewsSourcesAPI
from www.Routes.Admin.TagsAPI import TagsAPI
from www.Routes.Admin.XMLUploadAPI import XMLUploadAPI
from www.Routes.Admin.VideoCardsAPI import VideoCardsAPI
from www.Routes.Admin.AdminUserStoriesAPI import AdminUserStoriesAPI

app = Flask(__name__, static_folder='static', template_folder='templates')

app.config['PROPAGATE_EXCEPTIONS'] = True #propagates errors to log, now all logs should appear in apache error log
assets = Environment(app)
app.config.from_object('www.settings')
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False
app.config['INIT_TIME'] = int(time.time())

app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024

security = Security(app, datastore = user_datastore)
mail = Mail(app)
mdb.init_app(app)

def get_app_settings():
    appSettings = {'facebook': config.facebookConfig.CONSUMER_KEY,
                    'google': config.googleConfig.CONSUMER_KEY,
                    'app_url': config.serverConfig.APP_URL}
    return appSettings

app.jinja_env.globals.update(get_app_settings=get_app_settings)

indexApi = IndexAPI.as_view('index_view')
app.add_url_rule('/', view_func=indexApi, methods=['GET'])
app.add_url_rule('/all', view_func=indexApi, methods=['GET'])
app.add_url_rule('/profile', view_func=indexApi, methods=['GET'])
app.add_url_rule('/tag/<tag>', view_func=indexApi, methods=['GET'])
app.add_url_rule('/story/<storyId>', view_func=indexApi, methods=['GET'])
app.add_url_rule('/<path>', view_func=indexApi, methods=['GET'])
app.add_url_rule('/user/<username>', view_func=indexApi, methods=['GET'])
app.add_url_rule('/write/<username>', view_func=indexApi, methods=['GET'])
app.add_url_rule('/opinion/<username>', view_func=indexApi, methods=['GET'])

storiesApi = StoriesAPI.as_view('stories_view')
app.add_url_rule('/api/stories', defaults={'storyId': None}, view_func=storiesApi, methods=['GET'])
app.add_url_rule('/api/stories/<storyId>', view_func=storiesApi, methods=['GET'])

app.add_url_rule('/api/tag/<tagId>', view_func=TagStoriesAPI.as_view('tag_stories_view'), methods=['GET'])

app.add_url_rule('/register/<sn>', view_func=SocialConnectAPI.as_view('social_connect_view'), methods=['GET', 'POST', 'OPTIONS'])

profileApi = ProfileAPI.as_view('profile_view')
app.add_url_rule('/api/profile', view_func=profileApi, methods=['POST', 'OPTIONS'])
app.add_url_rule('/api/profile/<username>', view_func=profileApi, methods=['GET', 'OPTIONS'])

app.add_url_rule('/api/vote/<storyId>/<voteType>', view_func=VoteAPI.as_view('vote_view'), methods=['POST', 'OPTIONS'])

discoverApi = DiscoverAPI.as_view('discover_view')
app.add_url_rule('/discover', view_func=discoverApi, methods=['GET', 'OPTIONS'])
app.add_url_rule('/discover/<regionCode>', view_func=discoverApi, methods=['GET', 'OPTIONS'])

app.add_url_rule('/api/pintopic', view_func=PinnedTopicAPI.as_view('pinnedtopic_view'), methods=['POST', 'OPTIONS'])
app.add_url_rule('/api/pinnedtopics', view_func=PinnedTopicPublicAPI.as_view('pinnedtopic_pub_view'), methods=['GET', 'OPTIONS'])

app.add_url_rule('/api/tag_search', view_func=TagSearchAPI.as_view('tag_search_view'), methods=['GET', 'OPTIONS'])

app.add_url_rule('/api/headlines', view_func=HeadlinesAPI.as_view('headlines_view'), methods=['GET', 'OPTIONS'])

app.add_url_rule('/api/feedback', view_func=FeedbackAPI.as_view('feedback_view'), methods=['POST', 'OPTIONS'])

app.add_url_rule('/api/trendingtopics', view_func=TrendingAPI.as_view('trending_view'), methods=['GET', 'OPTIONS'])

app.add_url_rule('/api/source/<source>', view_func=SourceStoriesAPI.as_view('source_view'), methods=['GET', 'OPTIONS'])

app.add_url_rule('/contest', view_func=ContestsAPI.as_view('contest_view'), methods=['GET', 'OPTIONS'])

app.add_url_rule('/api/comments', view_func=CommentsAPI.as_view('comments_view'), methods=['GET', 'POST', 'OPTIONS'])

userStories = UserStoriesAPI.as_view('user_stories_api')
app.add_url_rule('/api/userstories', view_func=userStories, methods=['POST', 'OPTIONS'])
app.add_url_rule('/api/userstories/<storyId>', view_func=userStories, methods=['GET', 'DELETE', 'OPTIONS'])

opinionsApi = OpinionsAPI.as_view('opinions_api')
app.add_url_rule('/api/opinions/<username>', view_func=opinionsApi, methods=['GET', 'OPTIONS'])
app.add_url_rule('/api/opinions', view_func=opinionsApi, methods=['GET', 'OPTIONS'])
app.add_url_rule('/api/opinion/<storyId>', view_func=OpinionItemAPI.as_view('opinions_item_api'), methods=['GET', 'POST', 'OPTIONS'])

app.add_url_rule('/api/photoupload', view_func=ImageUploadAPI.as_view('photo_upload'), methods=['POST', 'OPTIONS'])



#admin
adminMainApi = AdminMainAPI.as_view('admin_main_view')
app.add_url_rule('/nsadmin', view_func=adminMainApi, methods=['GET'])
app.add_url_rule('/nsadmin/<path>', view_func=adminMainApi, methods=['GET'])

app.add_url_rule('/api/admin/news_sources', view_func=NewsSourcesAPI.as_view('news_sources_view'), methods=['GET', 'POST', 'PUT', 'DELETE'])

app.add_url_rule('/api/admin/tags', view_func=TagsAPI.as_view('news_tags_view'), methods=['GET', 'POST', 'PUT', 'DELETE'])

app.add_url_rule('/api/admin/xmlupload', view_func=XMLUploadAPI.as_view('xmlupload_view'), methods=['POST', 'OPTIONS'])

app.add_url_rule('/api/admin/video_cards', view_func=VideoCardsAPI.as_view('video_cards_view'), methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'])

app.add_url_rule('/api/admin/userstories', view_func=AdminUserStoriesAPI.as_view('admin_user_stories'), methods=['GET', 'POST', 'OPTIONS'])

@app.route('/d3')
def d3():
    return render_template('index.html')

if __name__ == '__main__':
    app.debug = True
    app.config['ASSETS_DEBUG'] = True
    app.run(host='0.0.0.0', port=3000)
