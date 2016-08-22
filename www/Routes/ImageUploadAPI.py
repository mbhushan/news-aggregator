'''
Created on Apr 21, 2015

@author: rsingh
'''
from flask import request, jsonify
from flask.views import MethodView

from NSLib.Config import config
from NSLib.AWS.S3Uploader import S3Uploader
from werkzeug import secure_filename
from www.decorator import authenticated_user_required
import time, uuid

class ImageUploadAPI(MethodView):

    decorator = [authenticated_user_required]

    def post(self):
#         print "here"
#         print request.files
        file1 = request.files['file']
        if file1 and self.allowed_file(file1):
            s3uploader = S3Uploader(config)
            filename = str(uuid.uuid4()) + secure_filename(file1.filename)
            link = s3uploader.uploadFromFile(filename, file1)
#             link = 'https://nationstory.s3.amazonaws.com/anonUser.jpg'
            return jsonify({'url': link})
        else:
            return jsonify({'status': 400, 'errorCode': 1001, 'message': 'Only jpg, png and jpeg are accepted.'})

    def allowed_file(self, file1):
        tokens = file1.filename.split('.')
        if tokens[-1] in ['png', 'jpg', 'jpeg']:
            return True
        else:
            return False