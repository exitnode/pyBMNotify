# pyBMNotify

Monitors a defined set of Brandmeister talkgroups and callsigns for activity and sends push notifications via Pushover.

## Credits

Inspired by [https://github.com/klinquist/bmPushNotification]

## Requirements

* Python 3
* socketIO-client (install with _sudo pip3 install socketIO-client_)

## Configuration

Configure _config.py_ to your needs. If you don't want push notifications, leave the corresponding variables empty.

## Execution

_# python3 pyBMNotify.py_
