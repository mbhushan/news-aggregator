'''
Created on 29-Jan-2013

@author: roshan
'''
from flask.views import MethodView
from flask import render_template, request

from NSLib.Config import config
from flask.globals import session
from flask_login import current_user
from NSLib.db.News.Weather import Weather
from NSLib.MiscFunctions import getIpToLocation
from flask.json import jsonify
from NSLib.Util.EmailSender import EmailSender


class FeedbackAPI(MethodView):

    def post(self):
        feedback = request.json.get('feedback')
        email = request.json.get('email')

        if not feedback or feedback.strip() == '':
            return jsonify({'status': 400, 'errorCode': 1001, 'message': 'Feedback can not be empty'}), 400

        if not current_user.is_authenticated() and (email is None or email.strip() == ''):
            return jsonify({'status': 400, 'errorCode': 1001, 'message': 'Email can not be empty'}), 400

        if current_user.is_authenticated():
            email = current_user.email

        emailSender = EmailSender()
        body = '<b>Sender<b>: %s <br/><br/><b>Body:</b><br/>%s' % (email, feedback)
        emailSender.sendEmail('noreply@nationstory.com', ['rsingh@nationstory.com', 'mani@nationstory.com'], 'Feedback received', body)

        return jsonify({'status': 200})
