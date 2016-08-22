'''
Created on Apr 6, 2015

@author: rsingh
'''
from flask.views import MethodView
from flask import request
from werkzeug import secure_filename

import uuid
import os

from NSLib.Config import config
from NSLib.db.News.XMLSource import XMLSource
from www.decorator import admin_user_required

class XMLUploadAPI(MethodView):

    decorators = [admin_user_required]

    def post(self):

        file1 = request.files['file']
        fileName = str(uuid.uuid4()) + '-' + secure_filename(file1.filename)
        filePath = os.path.join(config.serverConfig.LOCAL_STORAGE, fileName)
        file1.save(filePath)

        name = request.form.get('name')

        xmlSource = XMLSource(config)
        xmlSource.add(name, filePath)

        return ""

