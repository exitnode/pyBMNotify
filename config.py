#!/usr/bin/env python

# adapt the following variables to your needs
talkgroups = [91, 262] # Talkgroups to monitor
callsigns = ["N0CALL", "N0C4LL"] # Callsigns to monitor
noisy_calls = ["L1DHAM"] # Noisy calls signs that will be ignored
min_duration = 2 # Min. duration of a QSO to qualify for a push notification
min_silence = 300 # Min. time in seconds after the last QSO before a new push notification will be send
verbose = True # Enable extra messages (console only)
# Pushover configuration
pushover_token = "" # Your Pushover API token
pushover_user = "" # Your Pushover user key

