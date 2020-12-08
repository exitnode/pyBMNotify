#!/usr/bin/env python

# adapt the following variables to your needs
talkgroups = [91, 262] # Talkgroups to monitor
callsigns = ["N0CALL", "N0C4LL"] # Callsigns to monitor
noisy_calls = ["L1DHAM"] # Noisy calls signs that will be ignored
min_duration = 2 # Min. duration of a QSO to qualify for a push notification
min_silence = 300 # Min. time in seconds after the last QSO before a new push notification will be send
verbose = True # Enable extra messages (console only)

# Pushover configuration
pushover = False # Enable or disable notifications via Pushover
pushover_token = "1234567890" # Your Pushover API token
pushover_user = "abcdefghijklm" # Your Pushover user key

# Telegram configuration
telegram = False # Enable or disable notifications via Telegram
telegram_api_id = "1234567"
telegram_api_hash = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
telegram_username = "foo_bot"
phone = "+491234567890"

# DAPNet configuration
dapnet = False # Enable or disable notifications via dapnet
dapnet_user = "mycall"
dapnet_pass = "xxxxxxxxxxxxxxxxxxxx"
dapnet_url = 'http://www.hampager.de:8080/calls'
dapnet_callsigns = ["MYCALL"]
dapnet_txgroup = "dl-all"
