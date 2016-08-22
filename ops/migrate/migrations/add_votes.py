'''
Created on Dec 27, 2014

@author: rsingh
'''

from NSLib.db.MongoInit import MongoInit
from NSLib.Config import config

if __name__ == '__main__':
    #exit()
    mongo = MongoInit(config)
    print mongo.newsArticlesCollection.update({}, {'$set': {'votes': 0, 'up_votes': [], 'down_votes': []}}, multi=True)

