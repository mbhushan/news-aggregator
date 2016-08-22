'''
Created on Jun 27, 2013

@author: rsingh
'''

from NSLib.ErrorCodes.ErrorCodeManager import errorCodeManager

class ApiException(Exception):
    '''
    custom class for raising exceptions
    '''

    def __init__(self, errorCode, message = None):
        self.errorCode = errorCode
        if message is None:
            message = errorCodeManager.getMessage(errorCode)

        self.message = message

    def __str__(self):
        return "ApiException code : %s, message: %s" %(self.errorCode, self.message)
