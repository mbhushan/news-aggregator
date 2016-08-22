'''
Created on Jun 27, 2013

@author: rsingh
'''

import os, sys

#path set up to fix import
path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../'))
sys.path.append(path + '/framework/')

def dummy():
    print 'executing dummy script'

if __name__ == '__main__':
    dummy()