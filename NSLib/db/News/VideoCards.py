'''
Created on Apr 7, 2015

@author: rsingh
'''
import time
import requests, json, feedparser

from NSLib.db.MongoInit import MongoInit
from NSLib.db.AutoIncStore import AutoIncStore
import urlparse
import arrow


class VideoCards(object):

    TYPE_YOUTUBE = 1

    def __init__(self, config):
        self.config = config
        self.mongo = MongoInit(config)

    def add(self, name, url, thumbnail, description, videoType=TYPE_YOUTUBE):
        ts = int(time.time())
        ais = AutoIncStore(self.config)
        _id = ais.getNext('video_cards')

        videoId = self.getVideoId(url)

        row = {'_id': _id, 'name': name, 'url': url, 'embed_url': 'https://www.youtube.com/embed/%s' % videoId, 'thumbnail':thumbnail,
               'description': description, 'added': ts, 'video_type': videoType}

        comments = self.getComments(videoId)
        details = self.getYTVideoDetails(videoId)

        row.update(details)
        row['comments'] = comments

        self.mongo.videoCardCollection.insert(row)
        return row

    def getAll(self, page, count=100):
        skip = (page-1) * count
        rows = list(self.mongo.videoCardCollection.find().skip(skip).limit(count))

        return rows

    def get(self, _id):
        return self.mongo.videoCardCollection.find_one({'_id': _id})

    def remove(self, _id):
        self.mongo.videoCardCollection.remove({'_id': _id})

    def edit(self, _id, name, url, thumbnail, description, videoType=TYPE_YOUTUBE):
        videoId = self.getVideoId(url)

        row = {'name': name, 'url': url, 'embed_url': 'https://www.youtube.com/embed/%s' % videoId, 'thumbnail': thumbnail,
               'description': description, 'video_type': videoType}

        comments = self.getComments(videoId)
        details = self.getYTVideoDetails(videoId)

        row.update(details)
        row['comments'] = comments

        self.mongo.videoCardCollection.update({'_id': _id}, {'$set': row})

    def getVideoId(self, yt_url):
        qs = urlparse.parse_qs(urlparse.urlparse(yt_url).query)
        return qs['v'][0]

    def getYTVideoDetails(self, videoId):
        url = 'https://www.googleapis.com/youtube/v3/videos?id=%s&key=AIzaSyAjmQGLBcXyWKspntCpK8zJvW7jnCJHKbE&part=snippet' % videoId

        resp = requests.get(url)
        if resp.status_code == 200:
            videoData = json.loads(resp.text)
            d = videoData['items'][0]
            return {'title': d['snippet']['title'], 'thumbnail': d['snippet']['thumbnails']['medium']['url']}

    def getComments(self, videoId):
        url = 'https://gdata.youtube.com/feeds/api/videos/%s/comments?max-results=20' % videoId
        d = feedparser.parse(url)

        comments = []
        for entry in d['entries']:
            try:
                comment = entry['content'][0]['value']
                if comment != '':
                    comments.append({'text': comment, 'name': entry['author'], 'published': time.mktime(entry.published_parsed),
                                     'profile_pic': self.getGooglePlusProfilePic(entry['yt_googleplususerid']), 'user_id': entry['yt_googleplususerid']})
            except:
                pass

        return comments

    def getGooglePlusProfilePic(self, googlePlusId):
        url = 'https://www.googleapis.com/plus/v1/people/%s?fields=image&key=AIzaSyAjmQGLBcXyWKspntCpK8zJvW7jnCJHKbE' % googlePlusId

        resp = requests.get(url)
        if resp.status_code == 200:
            data = json.loads(resp.text)
            return data['image']['url']

    def formatComment(self, comment):
        resp = {'text': comment['text'], 'published': arrow.get(comment['published']).humanize(),
                'user_id': comment['user_id'], 'name': comment['name'], 'profile_pic': comment['profile_pic']}

        return resp