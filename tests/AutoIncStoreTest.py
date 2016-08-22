'''
Created on Apr 7, 2015

@author: rsingh
'''
import unittest
from NSLib.db.AutoIncStore import AutoIncStore
from NSLib.Config import config

class Test(unittest.TestCase):


    def testAutoInc(self):
        autoIncStore = AutoIncStore(config)
        print autoIncStore.getNext('test_key')


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testAutoInc']
    unittest.main()