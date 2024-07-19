#!/bin/bash

# confirm in ZeroTier Network
export NODE_ADDRESS=$(zerotier-cli -j info | python3 -c "import sys, json; print(json.load(sys.stdin)['address'])")
zerotier-cli join $ZEROTIER_NETWORK

# start DHCP server
systemctl restart dnsmasq

# start mediamtx
DATE=$(date +"%Y-%m-%d")
./home/archangel/mediamtx > "/home/archangel/missions/streamlog-${DATE}.txt"