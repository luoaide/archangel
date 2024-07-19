#!/bin/bash

STREAM_ADDRESS=$(zerotier-cli get ${ZEROTIER_NETWORK} ip)
PUBLISHED_PATH=$1
RTSP_PORT=$2

curl -X POST "http://server.archangel/uas/announceStreamStart/${NODE_ADDRESS}/${PUBLISHED_PATH}" -H 'Content-Type: application/json' -d "{'source_ip': ${STREAM_ADDRESS}, 'rtsp_port': ${RTSP_PORT}}"
