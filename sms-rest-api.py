#!/usr/bin/env python

import sys
import time
import requests
import json
import random
from datetime import datetime

headers = {'Content-Type': 'application/json', 'Authorization': ''}
api_url = "https://www.e-osu.si/api"
nodes_url = "/nodes"
sensors_url = "/sensors"
measurements_url = "/measurements"
node_name = "test2"
sensor_type = "SHT21"
sensor_quantity = "humidity"
sensor_unit = "%"

# creates new node if not exists

r = requests.get(api_url+nodes_url+"?name="+node_name, headers=headers)
if "No nodes found" in r.text:
    json_str = '''{ "name": "''' + node_name + '''", "location": "", "loc_lat": null, "loc_lon": null, "cluster": "1", "cluster_title": "test", "status": "active", "setup": "", "scope": "", "project": "", "user_comment": "", "box_label": "", "serial_no": "", "mac": "", "network_addr": null, "network_addr2": null, "firmware": "", "bootloader": "", "role": "device", "sensors": [], "components": [] }''';
    r = requests.post(api_url+nodes_url, data=json_str, headers=headers)
    print r.text
    if "error" in r.text:
        print "Error: Node with the name " + node_name + " already exists"
        sys.exit()

# gets new node id

r = requests.get(api_url+nodes_url+"?name="+node_name, headers=headers)
new_node_id = [r.json()[0]['_id']]
r = requests.get(api_url+nodes_url+"/"+new_node_id[0], headers=headers)
new_node_id.append(str(r.json()[0]['id']))

# makes new sensor if not exists

sensor_id = new_node_id[1]+"-"+sensor_type+"-"+sensor_quantity
r = requests.get(api_url+sensors_url+"?id="+sensor_id, headers=headers)
if "No sensors found" in r.text:
    json_str = '''{ "id": "'''+sensor_id+'''", "type": "'''+sensor_type+'''", "quantity": "'''+sensor_quantity+'''", "unit": "'''+sensor_unit+'''", "node_id": "'''+new_node_id[0]+'''", "node": '''+new_node_id[1]+''' }'''
    r = requests.post(api_url+sensors_url, data=json_str, headers=headers)
    print r.text

# gets new sensor id

r = requests.get(api_url+sensors_url+"?id="+sensor_id, headers=headers)
new_sensor_id = r.json()[0]['_id']

# upload mesurements

measurement = '''{"sensor_id":"'''+new_sensor_id+'''","node_id": "'''+new_node_id[0]+'''","sensor": "'''+sensor_id+'''","node": '''+new_node_id[1]+''', "latitude": 46.041994 , "longitude": 14.487875 ,"ts": "2014-07-24T15:14:30.850Z","value": 25,"context":"test"}'''
measurements = []
for x in xrange(10):
    data = json.loads(measurement)
    data['ts'] = datetime.utcnow().isoformat()
    data['value'] = random.randint(1, 30)
    measurements.append(data)

r = requests.post(api_url+measurements_url, data=json.dumps(measurements), headers=headers)
print r.text
