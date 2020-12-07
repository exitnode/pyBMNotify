from socketIO_client import SocketIO
import json
import datetime as dt
import time

id = ""
last_activity = {}


# adapt the following variables to your needs
talkgroups = [91, 98002] # Talkgroups to monitor
#dmr_ids = [2637550]
callsigns = ["DL6MHC", "OE1MEW"]
min_duration = 2 # Min. duration of QSO to qualify for a push notification
min_silence = 300 # Min. time in seconds after the last QSO before a new push notification will be send.
 
def on_connect():
    print('connect')
 
def on_disconnect():
    print('disconnect')
 
def on_reconnect():
    print('reconnect')

def construct_message(c):
    tg = c["DestinationID"]
    out = ""
    duration = c["Stop"] - c["Start"]
    #print(c["DestinationName"])
    # convert unix time stamp to human readable format
    time = dt.datetime.utcfromtimestamp(c["Start"]).strftime("%Y/%m/%d %H:%M")
    # construct text message from various QSO properties
    out += c["SourceCall"] + ' (' + c["SourceName"] + ') was active on '
    out += str(tg) + ' (' + c["DestinationName"] + ') at '
    out += time + ' (' + str(duration) + ' seconds)'
    #print(json.dumps(call,separators=(',',':'),sort_keys=True,indent=4))
    # remember ID to prevent doublets
    #id = call["SessionID"]
    #last_activity[tg] = call["Start"]
    # finally print out the text message
    print(out)

def on_mqtt(*args):
    global id
    # get json data of QSO
    call = json.loads(args[0]['payload'])
    #print(json.dumps(call,separators=(',',':'),sort_keys=True,indent=4))
    # check if talkgroup is one of those to be monitored, if QSO has already been
    # ended and the same QSO has already been handled
    tg = call["DestinationID"]
    if call["SourceCall"] in callsigns:
        construct_message(call)
    elif tg in talkgroups and call["Stop"] > 0 and id != call["SessionID"] and (tg not in last_activity or (last_activity[tg] + min_silence) < call["Start"]):
        # calculate duration of QSO
        duration = call["Stop"] - call["Start"]
        # only proceed if QSO has the configured min. duration
        if duration >= min_duration:
            construct_message(call)
            id = call["SessionID"]
            last_activity[tg] = call["Start"]

socket = SocketIO('https://api.brandmeister.network/lh')
socket.on('connect', on_connect)
socket.on('disconnect', on_disconnect)
socket.on('reconnect', on_reconnect)
socket.on('mqtt', on_mqtt)
socket.wait()
