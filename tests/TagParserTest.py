'''
Created on Feb 1, 2015

@author: rsingh
'''
import unittest
from NSLib.Parser.TagParser import TagParser


class Test(unittest.TestCase):

    def testName(self):
        refdata = TagParser("hyderabad bangalore mysore elections: BJP plans aggressive campaign; counter AAP", True)
        print refdata.getTags()


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()