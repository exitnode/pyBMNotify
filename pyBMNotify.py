#!/usr/bin/env python
from socketIO_client import SocketIO
import json
import datetime as dt
import time
import config as cfg
import http.client, urllib

# libraries only needed if Telegram is configured in config.py
if cfg.telegram:
    import telebot 
    from telethon.sync import TelegramClient 
    from telethon.tl.types import InputPeerUser, InputPeerChannel 
    from telethon import TelegramClient, sync, events 

# libraries only needed if dapnet is configured in config.py
if cfg.dapnet:
    import requests
    from requests.auth import HTTPBasicAuth

last_TG_activity = {}
last_OM_activity = {}

def on_connect():
    print('Connecting to the Brandmeister API')
 
def on_disconnect():
    print('Disconnected')
 
def on_reconnect():
    print('Reconnecting')

# Send push notification via Pushover. Disabled if not configured in config.py
def push_pushover(msg):
    conn = http.client.HTTPSConnection("api.pushover.net:443")
    conn.request("POST", "/1/messages.json",
        urllib.parse.urlencode({
        "token": cfg.pushover_token,
        "user": cfg.pushover_user,
        "message": msg,
        }), { "Content-type": "application/x-www-form-urlencoded" })
    conn.getresponse()

# Send push notification via Telegram. Disabled if not configured in config.py
def push_telegram(msg):
    client = TelegramClient('bm_bot', cfg.telegram_api_id, cfg.telegram_api_hash) 
    client.connect() 
    if not client.is_user_authorized(): 
        client.send_code_request(cfg.phone) 
        client.sign_in(cfg.phone, input('Please enter the code which has been sent to your phone: ')) 
    try: 
        receiver = InputPeerUser('user_id', 'user_hash') 
        client.send_message(cfg.telegram_username, msg) 
    except Exception as e: 
        print(e); 
    client.disconnect() 

# send pager notification via DAPNET. Disabled if not configured in config.py
def push_dapnet(msg):
    dapnet_json = json.dumps({"text": msg, "callSignNames": cfg.dapnet_callsigns, "transmitterGroupNames": [cfg.dapnet_txgroup], "emergency": True})
    response = requests.post(cfg.dapnet_url, data=dapnet_json, auth=HTTPBasicAuth(cfg.dapnet_user,cfg.dapnet_pass)) 

# assemble the text message
def construct_message(c):
    tg = c["DestinationID"]
    out = ""
    duration = c["Stop"] - c["Start"]
    # convert unix time stamp to human readable format
    time = dt.datetime.utcfromtimestamp(c["Start"]).strftime("%Y/%m/%d %H:%M")
    # construct text message from various transmission properties
    out += c["SourceCall"] + ' (' + c["SourceName"] + ') was active on '
    out += str(tg) + ' (' + c["DestinationName"] + ') at '
    out += time + ' (' + str(duration) + ' seconds)'
    # finally return the text message
    return out

# where the magic happens
def on_mqtt(*args):
    # get json data of transmission
    call = json.loads(args[0]['payload'])
    tg = call["DestinationID"]
    callsign = call["SourceCall"]
    start_time = call["Start"]
    stop_time = call["Stop"]
    notify = False
    now = int(time.time())
    # check if callsign is monitored, the transmission has already been finished
    # and the person was inactive for n seconds
    if callsign in cfg.callsigns:
        if callsign not in last_OM_activity:
            last_OM_activity[callsign] = 9999999
        inactivity = now - last_OM_activity[callsign]
        if callsign not in last_OM_activity or inactivity >= cfg.min_silence:
            # If the activity has happened in a monitored TG, remember the transmission start time stamp
            if tg in cfg.talkgroups and stop_time > 0:
                last_TG_activity[tg] = now
            # remember the transmission time stamp of this particular DMR user
            last_OM_activity[callsign] = now
            notify = True
    # Continue if the talkgroup is monitored, the transmission has been
    # finished and there was no activity during the last n seconds in this talkgroup
    elif tg in cfg.talkgroups and stop_time > 0:# and callsign not in cfg.noisy_calls:
        if tg not in last_TG_activity:
            last_TG_activity[tg] = 9999999
        inactivity = now - last_TG_activity[tg]
        # calculate duration of key down
        duration = stop_time - start_time
        # only proceed if the key down has been long enough
        if duration >= cfg.min_duration:
            if tg not in last_TG_activity or inactivity >= cfg.min_silence:
                notify = True
            elif cfg.verbose:
                print("ignored activity in TG " + str(tg) + " from " + callsign + ": last action " + str(inactivity) + " seconds ago.")
            last_TG_activity[tg] = now
    if cfg.verbose and callsign in cfg.noisy_calls:
        print("ignored noisy ham " + callsign)
    # finally write the message to the console and send a push notification
    if notify:
        msg = construct_message(call)
        print(msg)
        if cfg.pushover:
            push_pushover(msg)
        if cfg.telegram:
            push_telegram(msg)
        if cfg.dapnet:
            push_dapnet(msg)

socket = SocketIO('https://api.brandmeister.network/lh')
socket.on('connect', on_connect)
socket.on('disconnect', on_disconnect)
socket.on('reconnect', on_reconnect)
socket.on('mqtt', on_mqtt)
socket.wait()
