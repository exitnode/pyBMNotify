from socketIO_client import SocketIO
import json
import datetime as dt

tg = [91, 98002]
min_duration = 2
id = ""
 
def on_connect():
    print('connect')
 
def on_disconnect():
    print('disconnect')
 
def on_reconnect():
    print('reconnect')

def on_mqtt(*args):
    out = ""
    global id
    call = json.loads(args[0]['payload'])
    #print(json.dumps(call,separators=(',',':'),sort_keys=True,indent=4))
    #if call["DestinationID"] in tg and id != call["SessionID"]:
    if call["DestinationID"] in tg and call["Stop"] > 0 and id != call["SessionID"]:
        duration = call["Stop"] - call["Start"]
        if duration > min_duration:
            time = dt.datetime.utcfromtimestamp(call["Start"]).strftime("%Y/%m/%d %H:%M")
            out += call["SourceCall"] + ' (' + call["SourceName"] + ') was active on '
            out += str(call["DestinationID"]) + ' (' + call["DestinationName"] + ') at '
            out += time + ' (' + str(duration) + ' seconds)'
            #print(json.dumps(call,separators=(',',':'),sort_keys=True,indent=4))
            id = call["SessionID"]
            print(out)

socket = SocketIO('https://api.brandmeister.network/lh')
socket.on('connect', on_connect)
socket.on('disconnect', on_disconnect)
socket.on('reconnect', on_reconnect)
socket.on('mqtt', on_mqtt)
socket.wait()
