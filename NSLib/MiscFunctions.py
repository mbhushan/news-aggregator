'''
Created on Dec 14, 2014

@author: rsingh
'''

import uuid
from flask import current_app
import json
import requests

statesToCodeMapping = {"Haryana": "HR", "Punjab": "PB", "Goa": "GA", "Chhattisgarh": "CT", "Kerala": "KL", "Andaman and Nicobar": "AN", "Bihar": "BR", "Tamil Nadu": "TN", "Chandigarh": "CH", "Jammu and Kashmir": "JK", "Jharkhand": "JH", "Meghalaya": "ML", "Delhi": "DL", "Orissa": "OR", "Assam": "AS", "Madhya Pradesh": "MP", "Manipur": "MN", "Rajasthan": "RJ", "Sikkim": "SK", "West Bengal": "WB", "Andhra Pradesh": "AP", "Himachal Pradesh": "HP", "Nagaland": "NL", "Gujarat": "GJ", "Arunachal Pradesh": "AR", "Maharashtra": "MH", "Tripura": "TR", "Uttarakhand": "UT", "Puducherry": "PY", "Karnataka": "KA", "Mizoram": "MZ", "Uttar Pradesh": "UP"}
codeToStateMapping = {"DL": "Delhi", "WB": "West Bengal", "HR": "Haryana", "HP": "Himachal Pradesh", "UP": "Uttar Pradesh", "JH": "Jharkhand", "BR": "Bihar", "JK": "Jammu and Kashmir", "PB": "Punjab", "NL": "Nagaland", "PY": "Puducherry", "TR": "Tripura", "TN": "Tamil Nadu", "RJ": "Rajasthan", "CH": "Chandigarh", "AN": "Andaman and Nicobar", "AP": "Andhra Pradesh", "AS": "Assam", "AR": "Arunachal Pradesh", "GA": "Goa", "GJ": "Gujarat", "CT": "Chhattisgarh", "KA": "Karnataka", "UT": "Uttarakhand", "MN": "Manipur", "MH": "Maharashtra", "KL": "Kerala", "SK": "Sikkim", "MP": "Madhya Pradesh", "ML": "Meghalaya", "OR": "Orissa", "MZ": "Mizoram"}
statesCities = {"states":{"DL":["Delhi"],"CH":["Chandigarh"],"WB":["Kolkata"],"HR":["Chandigarh"],"HP":["Shimla"],"UP":["Lucknow"],"AN":["Port Blair"],"AP":["Vijayawada","Hyderabad"],"AS":["Dispur","Guwahati"],"AR":["Itanagar"],"JH":["Ranchi"],"BR":["Patna"],"JK":["Srinagar"],"GA":["Panaji"],"GJ":["Gandhinagar","Ahmedabad"],"CT":["Raipur"],"TN":["Chennai"],"KA":["Bengaluru"],"NL":["Kohima"],"ML":["Shillong"],"PY":["Pondicherry"],"TR":["Agartala"],"MH":["Mumbai","Pune","Nagpur"],"KL":["Thiruvananthapuram"],"PB":["Chandigarh"],"SK":["Gangtok"],"MP":["Bhopal"],"MN":["Imphal"],"UT":["Dehradun"],"OR":["Bhubaneswar"],"RJ":["Jaipur"],"MZ":["Aizawl"]},"cities":{"Delhi":{"coordinates":[28.64,77.09], "woeid":"2295019"}, "Pondicherry":{"coordinates":[11.93,79.78],"woeid":"20070459"},"Ranchi":{"coordinates":[23.35,85.33],"woeid":"2295383"},"Lucknow":{"coordinates":[26.84,80.94],"woeid":"2295377"},"Mumbai":{"coordinates":[18.97,72.82],"woeid":"2295411"},"Kohima":{"coordinates":[25.67,94.1],"woeid":"2289212"},"Pune":{"coordinates":[18.52,73.85],"woeid":"2295412"},"Agartala":{"coordinates":[23.83,91.26],"woeid":"2294951"},"Raipur":{"coordinates":[21.14,81.38],"woeid":"2294871"},"Shillong":{"coordinates":[25.56,91.88],"woeid":"2294854"},"Bhubaneswar":{"coordinates":[20.27,85.84],"woeid":"2294941"},"Bengaluru":{"coordinates":[12.96,77.56],"woeid":"2295420"},"Patna":{"coordinates":[25.61,85.14],"woeid":"2295381"},"Itanagar":{"coordinates":[27.1,93.62],"woeid":"2294848"},"Kolkata":{"coordinates":[22.56,88.36],"woeid":"2295386"},"Gandhinagar":{"coordinates":[23.22,72.68],"woeid":"2293567"},"Imphal":{"coordinates":[24.82,93.95],"woeid":"2294950"},"Bhopal":{"coordinates":[23.25,77.41],"woeid":"2295407"},"Nagpur":{"coordinates":[21.15,79.09],"woeid":"2282863"},"Chandigarh":{"coordinates":[30.75,76.78],"woeid":"2295391"},"Gangtok":{"coordinates":[27.33,88.62],"woeid":"2288890"},"Chennai":{"coordinates":[13.08,80.27],"woeid":"2295424"},"Port Blair":{"coordinates":[11.66,92.73],"woeid":"2295345"},"Shimla":{"coordinates":[31.1,77.17],"woeid":"2286457"},"Jaipur":{"coordinates":[26.92,75.82],"woeid":"2295401"},"Dehradun":{"coordinates":[30.31,78.02],"woeid":"2294972"},"Thiruvananthapuram":{"coordinates":[8.48,76.95],"woeid":"2295426"},"Hyderabad":{"coordinates":[17.36,78.47],"woeid":"2295414"},"Panaji":{"coordinates":[15.49,73.82],"woeid":"2295173"},"Guwahati":{"coordinates":[26.18,91.73],"woeid":"2277394"},"Vijayawada":{"coordinates":[16.5,80.64],"woeid":"2295237"},"Aizawl":{"coordinates":[23.72,92.71],"woeid":"2294952"},"Srinagar":{"coordinates":[34.09,74.79],"woeid":"2295387"},"Ahmedabad":{"coordinates":[23.03,72.58],"woeid":"2295402"},"Dispur":{"coordinates":[26.14,91.79],"woeid":"2289166"}}}


def get_unique_string():
    return str(uuid.uuid4()).replace('-', '')

def stringify(data):
    if isinstance(data, list):
        for item in data:

            if item.has_key('_id'):
                item['_id'] = str(item['_id'])

    elif isinstance(data, dict) and data.has_key('_id'):
        data['_id'] = str(data['_id'])

    return data

def jsonify(data):
    return current_app.response_class(json.dumps(data),
        mimetype='application/json')

def hypenify(text):
    return text.replace(' ', '-')

def getIpToLocation(ip):
    try:
        url = 'http://api.ipinfodb.com/v3/ip-city/?format=json&key=a95a716ace1676900dfc8084a8326b64085f058a56121b854a8a600b44710d97&ip=%s' % ip
        resp = requests.get(url)
        if resp.status_code == 200:

            data = json.loads(resp.text)
            #print data
            if data.get('statusCode') != 'OK':
                return None
            if not statesToCodeMapping.get(data['regionName']):
                return None

            return {'city': data['cityName'], 'region': data['regionName'], 'regionCode': statesToCodeMapping.get(data['regionName'])}
    except:
        pass

    return None

def renameLocation(loc):
    loc = loc.lower().strip()
    if loc == 'new delhi':
        loc = 'delhi'
    elif loc == 'bangalore':
        loc = 'bengaluru'

    return loc

def getLocationTopics(city, region, regionCode):
    city = renameLocation(city)
    region = renameLocation(region)

    topics = [region, city]
    topics.extend(statesCities['states'].get(regionCode))
    topics = [topic.lower() for topic in topics]
    return list(set(topics))


