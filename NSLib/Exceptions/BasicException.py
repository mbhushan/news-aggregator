'''
Created on May 13, 2013

@author: roshan
'''

class BasicException(Exception):
    '''
    custom class for raising exceptions
    '''


    def __init__(self, errorCode, message = None):
        self.errorCode = errorCode
        self.message = message
        
    def __str__(self):
        return "BasicException code : %s, message" %(self.errorCode, self.message)