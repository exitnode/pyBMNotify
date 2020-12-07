from socketIO_client import SocketIO
import json
import datetime as dt

tg = 31650
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
    if call["DestinationID"] == tg and id != call["_id"]:
        time = dt.datetime.utcfromtimestamp(call["Start"]).strftime("%Y/%m/%d %H:%M")
        out += call["SourceCall"] + ' (' + call["SourceName"] + ') was active on ' + str(tg) + ' at ' + time
        print(out)
        #print(json.dumps(call,separators=(',',':'),sort_keys=True,indent=4))
        id = call["_id"]
            

socket = SocketIO('https://api.brandmeister.network/lh')
socket.on('connect', on_connect)
socket.on('disconnect', on_disconnect)
socket.on('reconnect', on_reconnect)
socket.on('mqtt', on_mqtt)
socket.wait()
