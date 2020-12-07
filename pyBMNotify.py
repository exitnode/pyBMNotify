from socketIO_client import SocketIO
import json

tg = 98002
 
def on_connect():
    print('connect')
 
def on_disconnect():
    print('disconnect')
 
def on_reconnect():
    print('reconnect')

def on_mqtt(*args):
    found = False
    out = ""
    call = json.loads(args[0]['payload'])
    for key,value in call.items():
        if key == "DestinationID" and value == tg:
            found = True
        if found and key == "SourceCall":
            out += value
        if found and key == "SourceName":
            out += " - " + value
    if out:
        print(out)
            

socket = SocketIO('https://api.brandmeister.network/lh')
socket.on('connect', on_connect)
socket.on('disconnect', on_disconnect)
socket.on('reconnect', on_reconnect)
socket.on('mqtt', on_mqtt)
socket.wait()
