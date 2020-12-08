#!/usr/bin/env python
from socketIO_client import SocketIO
import json
import datetime as dt
import time
import config as cfg
import http.client, urllib

last_TG_activity = {}
last_OM_activity = {}

def on_connect():
    print('Connecting to the Brandmeister API')
 
def on_disconnect():
    print('Disconnected')
 
def on_reconnect():
    print('Reconnecting')

def push_message(msg):
    if cfg.pushover_token != "" and cfg.pushover_user != "":
        conn = http.client.HTTPSConnection("api.pushover.net:443")
        conn.request("POST", "/1/messages.json",
            urllib.parse.urlencode({
            "token": cfg.pushover_token,
            "user": cfg.pushover_user,
            "message": msg,
            }), { "Content-type": "application/x-www-form-urlencoded" })
        conn.getresponse()

def construct_message(c):
    tg = c["DestinationID"]
    out = ""
    duration = c["Stop"] - c["Start"]
    # convert unix time stamp to human readable format
    time = dt.datetime.utcfromtimestamp(c["Start"]).strftime("%Y/%m/%d %H:%M")
    # construct text message from various QSO properties
    out += c["SourceCall"] + ' (' + c["SourceName"] + ') was active on '
    out += str(tg) + ' (' + c["DestinationName"] + ') at '
    out += time + ' (' + str(duration) + ' seconds)'
    # finally return the text message
    return out

def on_mqtt(*args):
    # get json data of QSO
    call = json.loads(args[0]['payload'])
    tg = call["DestinationID"]
    callsign = call["SourceCall"]
    start_time = call["Start"]
    stop_time = call["Stop"]
    msg = ""
    # check if callsign is monitored, the over has already been finished
    # and the person was inactive for n seconds
    if callsign in cfg.callsigns:
        if callsign not in last_OM_activity or (last_OM_activity[callsign] + cfg.min_silence) < start_time:
            # If the activity has happened in a monitored TG, remember the QSO start time stamp
            if tg in cfg.talkgroups and stop_time > 0:
                last_TG_activity[tg] = start_time
            # remember the QSO's time stamp of this particular DMR user
            last_OM_activity[callsign] = start_time
            msg = construct_message(call)
    # Continue if the talkgroup is monitored, the over has been finished and there was no activity
    # during the last n seconds in this talkgroup
    elif tg in cfg.talkgroups and stop_time > 0:
        if tg not in last_TG_activity or (last_TG_activity[tg] + cfg.min_silence) < start_time:
            # calculate duration of key down
            duration = stop_time - start_time
            # only proceed if the key down has been long enough
            if duration >= cfg.min_duration:
                last_TG_activity[tg] = start_time
                msg = construct_message(call)
    # finally write the message to the console and send a push notification
    if msg != "":
        print(construct_message(call))
        push_message(construct_message(call))

socket = SocketIO('https://api.brandmeister.network/lh')
socket.on('connect', on_connect)
socket.on('disconnect', on_disconnect)
socket.on('reconnect', on_reconnect)
socket.on('mqtt', on_mqtt)
socket.wait()
