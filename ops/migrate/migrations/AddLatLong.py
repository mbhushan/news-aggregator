'''
Created on Mar 10, 2015

@author: rsingh
'''

from NSLib.Config import config
from NSLib.db.MongoInit import MongoInit
from NSLib.Logger import Logger
import requests, json, time


mongo = MongoInit(config)
rows = list(mongo.indianCitiesTagsCollection.find({'location': {'$exists': False}}))
log = Logger.getLogger(Logger.LOGGER_CONSOLE)


url = 'https://maps.googleapis.com/maps/api/geocode/json?address=%s+,%s+,india'

for row in rows:
    res = requests.get(url % (row['_id'], row['state']))
    if res.status_code == 200:
        data = json.loads(res.text)
        if data.get('status') == 'OK':
            loc = (data['results'][0]['geometry']['location']['lat'], data['results'][0]['geometry']['location']['lng'])
            log.info("%s %s %s " % (row['_id'], loc[0], loc[1]))
            mongo.indianCitiesTagsCollection.update({'_id': row['_id']}, {'$set': {'location': loc}})
        else:
            log.error('**** Failed %s' % row['_id'])
    else:
        log.error('**** Failed %s' % row['_id'])

    time.sleep(4)


