'''
Created on Jan 26, 2015

@author: rsingh
'''

import requests, json, os
from NSLib.Config import config
from NSLib.Logger import Logger
from NSLib.db.News.Weather import Weather
import time

curPath = os.path.abspath(os.path.dirname(__file__))
cities = json.load(open(curPath + '/stateCities.json'))
log = Logger.getLogger(Logger.LOGGER_CONSOLE)

#     try:
#         baseurl = "https://query.yahooapis.com/v1/public/yql?"
#         yql_query = 'select item.condition from weather.forecast where woeid=%s AND u="c"' % details['woeid']
#         yql_url = baseurl + urllib.urlencode({'q':yql_query}) + "&format=json"
#         result = urllib2.urlopen(yql_url).read()
#         weatherData[city] = json.loads(result)['query']['results']['channel']['item']['condition']
#     except:
#         log.exception("some error happened while getting data for %s" % city)

weather = Weather(config)
for city, details in cities['cities'].iteritems():
    try:
        count = 0
        while count < 3:
            city = city.lower()
            url = 'http://api.openweathermap.org/data/2.5/forecast/daily?q=%s,in&units=metric&cnt=3' % city
            result = requests.get(url)

            if result.status_code == 200:
                weatherData = json.loads(result.text)
                if int(weatherData['cod']) == 200:
                    try:
                        #validate and save
                        weather._format({'details': weatherData}, city)
                        weather.save(city, weatherData)
                        log.info('got %s' % city)
                        break
                    except:
                        pass
                else:
                    log.info('Failed %s cod %s' % (city,weatherData['cod']))
            else:
                log.info('Failed %s %s' % (city, result.status_code))

            count += 1
            time.sleep(1)

    except:
        log.exception("failed to get city data")
