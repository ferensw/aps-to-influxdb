#!/usr/bin/env python3

import datetime
import os
import time
import requests
import json
import pytz
from influxdb import InfluxDBClient

APSYSTEMS_URL = 'http://api.apsystemsema.com:8073/apsema/v1/ecu/getPowerInfo'

print("ECU ID: " + os.environ['ECU_ID'], flush=True)
print("Writing to influx database \"" + os.environ['INFLUXDB_DATABASE'] + "\" at " + os.environ['INFLUXDB_HOST'] + ":" + os.environ['INFLUXDB_PORT'], flush=True)

influx_client = InfluxDBClient(host=os.environ['INFLUXDB_HOST'], port=os.environ['INFLUXDB_PORT'], database=os.environ['INFLUXDB_DATABASE'])
influx_client.create_database(os.environ['INFLUXDB_DATABASE'])

timezone = pytz.timezone(os.environ['TZ'])

def influx(timestamp, fields):
    json_body = [
        {
            "measurement": "aps",
            "time": datetime.datetime.strptime(getDateStringOfToday()+ ' ' +timestamp, "%Y%m%d %H:%M:%S").astimezone(timezone).isoformat(),
            "fields": fields,
        }
    ]
    try:
        influx_client.write_points(json_body)
    except Exception as e:
        log('Failed to write to influxdb: ', e)

def getDateStringOfToday():
    return datetime.date.today().strftime("%Y%m%d");

def getDataFromAPS():
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }

    data = {
      'ecuId': os.environ['ECU_ID'],
      'filter': 'power',
      'date': getDateStringOfToday()
    }

    response = requests.post(APSYSTEMS_URL, headers=headers, data=data)
    return response.json();

def log(message, exception):
    if exception is None:
        print("[" + str(datetime.datetime.utcnow())+ "] " + message, flush=True)
    else:
        print("[" + str(datetime.datetime.utcnow())+ "] " + message, exception, flush=True)


while True:
    aps_data = getDataFromAPS()
    if aps_data is None:
        log("APS status data is None", None)
        time.sleep(60)
        continue
    timesstring = aps_data.get("data").get("time")
    powersstring = aps_data.get("data").get("power")
    timelist = json.loads(timesstring)
    powerlist = json.loads(powersstring)
    for i in range(len(timelist)):
        timestamp = timelist[i]
        measurement = {"power":powerlist[i]}
        influx(timestamp, measurement)
    log("Sent data to influxdb", None)
    time.sleep(int(os.environ['SEND_DATA_INTERVAL']))
