'''
Created on Feb 28, 2015

@author: rsingh
'''
from NSLib.db.MongoInit import MongoInit
from NSLib.Config import config
import json
from NSLib.MiscFunctions import hypenify

locationTagsFiles = ['india_city_state.txt']
statesTagsFile = "india_states.txt"
generalTagsFiles = ["india_actors.txt", "india_actress.txt", "india_test_cricketers.txt", "india_odi_cricketers.txt",
                     "india_politicians.txt", "brands.txt"]


mongo = MongoInit(config)

def getExtraTags(fname):
    if fname in ['india_actors.txt', 'india_actress.txt']:
        return ['movies']

    elif fname in ['india_test_cricketers.txt', 'india_odi_cricketers.txt']:
        return ["cricket"]

    elif fname in ['india_politicians.txt']:
        return ['politics']

    return []

for fname in generalTagsFiles:
    with open(fname, "r") as f:
        for line in f:
            if line:
                row = {}
                line = json.loads(line.strip())
                row['_id'] = line['name']
                row['tags'] = [hypenify(line['tag'])]

                meta = getExtraTags(fname)
                row['tags'].extend(meta)
                row['meta'] = meta

                mongo.tagsCollection.insert(row)


for fname in locationTagsFiles:
    with open(fname, "r") as f:
        for line in f:
            if line:
                line = json.loads(line.strip())
                line['_id'] = line['name']
                del line['name']

                finalTags = []
                for tag in line['tag']:
                    finalTags.append(hypenify(tag))

                line['tags'] = finalTags
                del line['tag']

                mongo.indianCitiesTagsCollection.insert(line)

with open(statesTagsFile, "r") as f:
    for line in f:
        if line:
            row = {}
            line = json.loads(line.strip())
            row['_id'] = line['name']
            row['tags'] = [hypenify(line['tag'])]

            meta = getExtraTags(fname)
            row['tags'].extend(meta)
            row['meta'] = meta

            mongo.indianStatesTagsCollection.insert(row)
