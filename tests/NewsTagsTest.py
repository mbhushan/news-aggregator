'''
Created on Feb 28, 2015

@author: rsingh
'''
import unittest
from NSLib.db.News.NewsTags import NewsTags
from NSLib.Config import config

class NewsTagsTest(unittest.TestCase):


    def testSearch(self):
        nt = NewsTags(config)
        print nt.search('SAC')

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()