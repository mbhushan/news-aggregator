'''
Created on 07-May-2013

@author: rsingh
'''
from ConfigParser import ConfigParser
import os

class ErrorCodeManager(object):
    '''
    classdocs
    '''

    __ERROR_CODE_FILE = 'error_code.ini'

    def __init__(self):
        parser = ConfigParser()
        curPath = os.path.dirname(os.path.abspath(__file__)) + '/'
        errorCodeFile = curPath + self.__ERROR_CODE_FILE
        
        parser.read(errorCodeFile)
        
        self.__errorMessages = {}
        
        codes = parser.options('codes')
        for code in codes:
            self.__errorMessages[int(code)] = parser.get('codes', code)
        
    def getMessage(self, errorCode):
        '''
        Get message string for error code
        
        @param errorCode: integer error code
        @return: error message string
        @raise ValueError: whenever an unknown error code is encountered   
        '''
        if self.__errorMessages.has_key(errorCode):
            return self.__errorMessages[errorCode]
        else:
            raise ValueError("Invalid error code requested")
        
errorCodeManager = ErrorCodeManager()