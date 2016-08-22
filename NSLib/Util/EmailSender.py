'''
Created on Oct 23, 2014

@author: rsingh
'''

import smtplib
from email.mime.text import MIMEText
from email.Header import Header

class EmailSender(object):
    '''
    Utility class to send emails
    '''

    SENDGRID_HOST = 'smtp.mandrillapp.com'
    SENDGRID_PORT = 587
    SENDGRID_USERNAME = 'singh.roshan08@gmail.com'
    SENDGRID_PASSWORD = 't9wKf2NE1GbpOGw4ImF7cg'

    def __init__(self):
        self.smtp = smtplib.SMTP(self.SENDGRID_HOST, self.SENDGRID_PORT)
        #self.smtp.set_debuglevel(1)
        self.smtp.starttls()
        self.smtp.login(self.SENDGRID_USERNAME, self.SENDGRID_PASSWORD)

    def __del__(self):
        try:
            self.smtp.close()
        except:
            pass

    def sendEmail(self, sender, to, subject, body, cc = None, bcc = None, setReplyToAsTo = False, replyTo = None, mimeType="html"):
        '''to, cc, bcc should be lists of email addresses'''

        if not isinstance(to, list):
            raise ValueError('to should be list')

        if cc is not None and not isinstance(cc, list):
            raise ValueError('cc should be list')

        if bcc is not None and not isinstance(bcc, list):
            raise ValueError('bcc should be list')

        message = MIMEText(body.encode('UTF-8'), mimeType, 'UTF-8')
        message['Subject'] = Header(subject, 'UTF-8')
        message['From']    = sender
        message['To']      = ','.join(to)
        #this is specific to mandrill, and should be commented out when using any other mailer.
        #message.add_header('X-MC-Track', 'opens')

        if setReplyToAsTo:
            message['Reply-to'] = ','.join(to)

        if replyTo:
            message['Reply-to'] = replyTo

        recipients = []
        recipients.extend(to)

        if cc is not None:
            message['CC'] = ','.join(cc)
            recipients.extend(cc)

        if bcc is not None:
            message['BCC'] = ','.join(bcc)
            recipients.extend(bcc)

        #retry logic
        retryCount = 1
        while True:
            try:
                self.smtp.sendmail(sender, recipients, message.as_string())
                return
            except smtplib.SMTPException, e:
                if retryCount is 4 :
                    raise e
                else:
                    print "retrying..."
                    self.__init__()
                    retryCount = retryCount + 1






