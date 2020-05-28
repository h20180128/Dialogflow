# -*- coding:utf8 -*-
# !/usr/bin/env python
# Copyright 2017 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import print_function
#from future.standard_library import install_aliases
#install_aliases()

import time, uuid, urllib, urllib2
import hmac, hashlib
from base64 import b64encode


#from urllib.parse import urlparse, urlencode
#from urllib.request import urlopen, Request
#from urllib.error import HTTPError

import json
import os

from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    #print("Request: Here it comes.............")
    #print(req.json() )
    x=json.dumps(req, indent=4)
    #print(type(x))
    x=json.loads(x)
    x=x["queryResult"]["parameters"]["geo-city"]
    #print(x)

    if req.get("result").get("action") != "yahooWeatherForecast":
        return {}
    url='https://weather-ydn-yql.media.yahoo.com/forecastrss'
    method = 'GET'
    app_id = 'MAECMG48'
    consumer_key = 'dj0yJmk9NjlManhWM0FwcGFBJmQ9WVdrOVRVRkZRMDFITkRnbWNHbzlNQS0tJnM9Y29uc3VtZXJzZWNyZXQmc3Y9MCZ4PWQ3'
    consumer_secret = '956184cfb63ede4c76c7afb6bf12477d3b8d292b'
    concat = '&'
    query = {'location': x, 'format': 'json'}
    oauth = {
        'oauth_consumer_key': consumer_key,
        'oauth_nonce': uuid.uuid4().hex,
        'oauth_signature_method': 'HMAC-SHA1',
        'oauth_timestamp': str(int(time.time())),
        'oauth_version': '1.0'
    }

    """
    Prepare signature string (merge all params and SORT them)
    """
    merged_params = query.copy()
    merged_params.update(oauth)
    sorted_params = [k + '=' + urllib.quote(merged_params[k], safe='') for k in sorted(merged_params.keys())]
    signature_base_str =  method + concat + urllib.quote(url, safe='') + concat + urllib.quote(concat.join(sorted_params), safe='')

    """
    Generate signature
    """
    composite_key = urllib.quote(consumer_secret, safe='') + concat
    oauth_signature = b64encode(hmac.new(composite_key, signature_base_str, hashlib.sha1).digest())

    """
    Prepare Authorization header
    """
    oauth['oauth_signature'] = oauth_signature
    auth_header = 'OAuth ' + ', '.join(['{}="{}"'.format(k,v) for k,v in oauth.iteritems()])

    """
    Send request
    """
    url = url + '?' + urllib.urlencode(query)
    request1 = urllib2.Request(url)
    request1.add_header('Authorization', auth_header)
    request1.add_header('X-Yahoo-App-Id', app_id)
    response = urllib2.urlopen(request1).read()
    #print(response)
    response=json.loads(response)
    url2 = "https://api.airvisual.com/v2/city?city={}&state=California&country=USA&key=28ed033f-4236-4a07-a8f8-83e5f30a19b8".format(x)

    payload = {}
    headers= {}

    response2 = requests.request("GET", url2, headers=headers, data = payload)

    t=(response2.text.encode('utf8'))

    d=json.loads(t)

    #print(d)
    #print(pass)
    s=d['data']['current']['pollution']['aqius']
    #print(s)
    if 0<=s<=50 :
      return {
      "fulfillmentMessages": 



              "Today in " + x +" : " + response["current_observation"]["condition"]["text"] + " with a temperature of " + str(response["current_observation"]["condition"]["temperature"]) + " degrees fahrenheit and a good A.Q.I of " + str(s)
      }
    elif 51<=s<=100 :
      return {
      "fulfillmentMessages": 



              "Today in " + x +" : " + response["current_observation"]["condition"]["text"] + " with a temperature of " + str(response["current_observation"]["condition"]["temperature"]) + " degrees fahrenheit and a moderate A.Q.I of " + str(s)


    }

    elif 101<=s<=150:
      return {
      "fulfillmentMessages": 



              "Today in " + x +" : " + response["current_observation"]["condition"]["text"] + " with a temperature of " + str(response["current_observation"]["condition"]["temperature"]) + " degrees fahrenheit and an A.Q.I of " + str(s) + "which is unhealthy for sensitive groups"


    }

    elif 151<=s<=200:
      return {
      "fulfillmentMessages": 



              "Today in " + x +" : " + response["current_observation"]["condition"]["text"] + " with a temperature of " + str(response["current_observation"]["condition"]["temperature"]) + " degrees fahrenheit and an unhealthy A.Q.I of " + str(s)


    }

    elif 201<=s<=300:
      return {
      "fulfillmentMessages": 



              "Today in " + x +" : " + response["current_observation"]["condition"]["text"] + " with a temperature of " + str(response["current_observation"]["condition"]["temperature"]) + " degrees fahrenheit and a very unhealthy A.Q.I of " + str(s)


    }

    elif 301<=s<=500:
      return {
      "fulfillmentMessages": 



              "Today in " + x +" : " + response["current_observation"]["condition"]["text"] + " with a temperature of " + str(response["current_observation"]["condition"]["temperature"]) + " degrees fahrenheit and a moderate A.Q.I of " + str(s)


    }
    
    '''
    return {"fulfillmentMessages": [
      {
        "text": {
          "text": [
            "Today in "+ x +" : " + response["current_observation"]["condition"]["text"] + " with a temperature of " + str(response["current_observation"]["condition"]["temperature"])
          ]
        }
      }
    ]}
    '''

@app.route('/test', methods=['GET'])
def test():
    return  "Hello there"


@app.route('/static_reply', methods=['POST'])
def static_reply():
    speech = "Hello there, this is static reply from the webhook."
    string = "Guten tag"
    Message ="message string"

    my_result =  {

    "fulfillmentText": string,
     "source": string
    }

    res = json.dumps(my_result, indent=4)

    r = make_response(res)

    r.headers['Content-Type'] = 'application/json'
    return r



'''
    res = processRequest(req)

    res = json.dumps(res, indent=4)
    # print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


def processRequest(req):
    if req.get("result").get("action") != "yahooWeatherForecast":
        return {}
    baseurl = "https://weather-ydn-yql.media.yahoo.com/forecastrss"
    yql_query = makeYqlQuery(req)
    if yql_query is None:
        return {}
    yql_url = baseurl + urlencode({'q': yql_query}) + "&format=json"
    result = urlopen(yql_url).read()
    data = json.loads(result)
    res = makeWebhookResult(data)
    return res


def makeYqlQuery(req):
    result = req.get("result")
    parameters = result.get("parameters")
    city = parameters.get("geo-city")
    if city is None:
        return None

    return "select * from weather.forecast where woeid in (select woeid from geo.places(1) where text='" + city + "')"


def makeWebhookResult(data):
    query = data.get('query')
    if query is None:
        return {}

    result = query.get('results')
    if result is None:
        return {}

    channel = result.get('channel')
    if channel is None:
        return {}

    item = channel.get('item')
    location = channel.get('location')
    units = channel.get('units')
    if (location is None) or (item is None) or (units is None):
        return {}

    condition = item.get('condition')
    if condition is None:
        return {}

    # print(json.dumps(item, indent=4))

    speech = "Today in " + location.get('city') + ": " + condition.get('text') + \
             ", the temperature is " + condition.get('temp') + " " + units.get('temperature')

    print("Response:")
    print(speech)

    return {
        "speech": speech,
        "displayText": speech,
        # "data": data,
        # "contextOut": [],
        "source": "apiai-weather-webhook-sample"
    }
'''

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run(debug=False, port=port, host='0.0.0.0')
