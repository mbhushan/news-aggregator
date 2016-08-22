import json
import os, re
from NSLib.db.MongoInit import MongoInit
from NSLib.Config import config
from NSLib.MiscFunctions import hypenify

class RefData:

    def __init__(self):
        self.mongo = MongoInit(config)
        self.generalTags = list(self.mongo.tagsCollection.find())
        self.indianCities = list(self.mongo.indianCitiesTagsCollection.find())
        self.indianStates = list(self.mongo.indianStatesTagsCollection.find())

    def _searchForTags(self, text):
        tags = []
        textLower = text.lower()

        possibleTags = {}
        for tagVal in self.generalTags:
            if tagVal.get('case_sensitive'):
                match = re.search(r'\b%s\b' % tagVal['_id'], text)

            else:
                match = re.search(r'\b%s([:-]|\'s)?\b' % tagVal['_id'], textLower, re.IGNORECASE)

            if match:
                possibleTags[tagVal['_id']] = tagVal

        #possible set is a list of rows
        #now iterate and look for longest key params
        keys = possibleTags.keys()
        keys.sort(key = len, reverse=True)

        filteredTags = self._getFilteredTags(keys)
        for ft in filteredTags:
            tagVal = possibleTags[ft]

            if isinstance(tagVal['tags'], list):
                tags.extend(tagVal['tags'])
            else:
                tags.append(tagVal['tags'])

        return list(set(tags))

    def _getFilteredTags(self, tags):
        pTags = []

        for t in tags:
            found = False
            t = t.replace('-', ' ')
            for pt in pTags:
                pt = pt.replace('-', ' ')

                if pt == t:
                    found = True

                elif re.search(r'\b%s\b' % t, pt):
                    found = True

            if not found:
                pTags.append(t)

        return list(set(pTags))


    def getRefTags(self, text):
        if not text:
            return []

        text = text.strip()
        tags = self._searchForTags(text)

        return tags

#     def _removeSmallerTag(self, tags):
#         '''
#         if a tag has meenaxi and meenaxi lekhi, then meenaxi will be removed
#         '''
#         tags.sort(key = lambda s: len(s), reverse=True)
#         finalTags = []
#
#         for tag in tags:
#             found = False
#             for ft in finalTags:
#                 tokens = ft.split('-')
#                 for t in tokens:
#                     if tag == t:
#                         found = True
#                         break
#             if not found:
#                 finalTags.append(tag)
#
#         return finalTags

    def getLocationTags(self, text):
        text = text.strip().lower()
        cityTags = set([])
        stateTags = set([])

        for tagVal in self.indianStates:
            if re.search(r'\b%s\b' % tagVal['_id'], text):
                stateTags.update(tagVal['tags'])

        for tagVal in self.indianCities:
            if re.search(r'\b%s\b' % tagVal['_id'], text):
                stateTags.add(hypenify(tagVal['state']))
                cityTags.add(hypenify(tagVal['city']))

        return list(cityTags), list(stateTags)


