'''
Created on Apr 21, 2015

@author: rsingh
'''
from boto.s3.connection import S3Connection
from boto.s3.key import Key

class S3Uploader(object):

    def __init__(self, config):
        self.conn = S3Connection(config.awsConfig.ACCESS_KEY, config.awsConfig.ACCESS_SECRET)
        self.bucket = self.conn.get_bucket('nationstory')
        self.bucketPath = 'http://nationstory.s3-website-ap-southeast-1.amazonaws.com/'

    def uploadFromFileName(self, name, fileName):
        k = Key(self.bucket)
        k.key = name
        k.set_contents_from_filename(fileName, policy='public-read')
        return k.generate_url(0, query_auth=False)

    def uploadFromFile(self, name, fileOb):
        k = Key(self.bucket)
        k.key = name
        k.content_type = fileOb.mimetype
        k.set_contents_from_file(fileOb, policy='public-read')
        return k.generate_url(0, query_auth=False)

    def uploadFromString(self, name, val):
        k = Key(self.bucket)
        k.key = name
        k.set_contents_from_string(val, policy='public-read')
        return k.generate_url(0, query_auth=False)

