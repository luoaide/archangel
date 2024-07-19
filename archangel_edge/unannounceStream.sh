#!/bin/bash

PUBLISHED_PATH=$1
curl -X GET "http://server.archangel/uas/announceStreamEnd/${NODE_ADDRESS}/${PUBLISHED_PATH}"
