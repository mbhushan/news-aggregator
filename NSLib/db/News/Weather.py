'''
Created on Jan 26, 2015

@author: rsingh
'''
from NSLib.db.MongoInit import MongoInit
from datetime import datetime

class Weather(object):

    def __init__(self, config):
        self.config = config
        self.mongo = MongoInit(config)

    def save(self, city, weatherData):
        self.mongo.weatherCollection.update({'_id': city}, {'$set': {'details': weatherData}}, upsert=True)

    def get(self, city):
        row = self.mongo.weatherCollection.find_one({'_id': city})
        if row:
            return self._format(row, city)

        return None

    def _format(self, row, city):
        if row['details'].has_key('list'):
            details = row['details']['list'][0]

            forecast = []
            for index, f in enumerate(row['details']['list'][:3]):
                if index==0:
                    temp = {'ts': f['dt'], 'date': 'Today'}
                else:
                    temp = {'ts': f['dt'], 'date': datetime.fromtimestamp(f['dt']).strftime('%a')}

                temp.update(f['temp'])
                temp.update(f['weather'][0])
                forecast.append(temp)

            icon = 'http://openweathermap.org/img/w/%s.png' % details['weather'][0]['icon']
            return {'temperature': details['temp']['day'], 'icon': icon,
                    'description': details['weather'][0]['description'].title(), 'name': city.title(),
                    'forecast': forecast}
        return None

    def getAll(self):
        rows = list(self.mongo.weatherCollection.find())

        resp = []
        for row in rows:
            resp.append(self._format(row, row['_id']))

        return resp
