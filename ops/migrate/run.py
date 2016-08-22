'''
Created on Jun 27, 2013

@author: rsingh
'''

import os

import json
from NSLib.Config import config
from NSLib.db.MongoInit import MongoInit

mongo = MongoInit(config)

TEST_MODE = False

def readConfig():
    '''
    reads all the migrations available
    '''
    f = open('migrationinfo.json', 'r')
    lines = f.readlines()

    fileContent = []
    for line in lines:
        fileContent.append(line.strip())


    return json.loads("".join(fileContent))

def getLastMigrationId():
    '''
    fetches last applied migration
    '''
    row = mongo.configCollection.find_one({'_id':'migration'})

    lastMigration = 0
    if row is not None:
        lastMigration = row['value']

    return lastMigration

def setLastMigrationId(migationId):
    '''
    updates last applied migration
    '''
    if not TEST_MODE:
        mongo.configCollection.update({'_id':'migration'}, {'$set':{'value' : migationId}}, upsert = True)


if __name__ == '__main__':
    migrations = readConfig()

    pendingMigrations = {}
    lastMigrationId = getLastMigrationId()

    for migration in migrations:
        if migration['id'] > lastMigrationId:
            pendingMigrations[migration['id']] = migration

    if len(pendingMigrations) == 0:
        exit('*** No new migrations to run ***')

    pendingMigrationIds = sorted(pendingMigrations)

    lastSuccessfulMigration = None

    for i in pendingMigrationIds:
        cmd = 'python %s' % pendingMigrations[i]['filename']
        print "** running %s **" % cmd
        res = os.system(cmd)

        if res == 0:
            setLastMigrationId(i)
        else:
            print 'failed to run %s' % pendingMigrations[i]['filename']
            print 'aborting now!!'
            exit()

