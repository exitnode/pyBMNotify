# pyBMNotify

Monitors a defined set of Brandmeister talkgroups and callsigns for activity. It then sends push notifications via the following services for any transmission in / of the monitored talk groups / call signs:

* Pushover (https://pushover.net)
* Telegram (https://telegram.org)
* DAPNET (https://hampager.de)

In order to prevent message flooding, the script only notifes you again after 300 (configurable) seconds of silence in a TG or from a monitored call sign.

## Credits

Inspired by https://github.com/klinquist/bmPushNotification

## Requirements

* Python 3
* socketIO-client (install with _sudo pip3 install socketIO-client_)

If you want to be notified via Telegram, the following libraries need to be installed:

* telebot (install with _sudo pip3 install telebot_)
* telethon (install with _sudo pip3 install telethon_)

## Configuration

Configure _config.py_ to your needs. If you don't want push notifications, set the corresponding variables to False.

## Execution

```
# python3 pyBMNotify.py
```
