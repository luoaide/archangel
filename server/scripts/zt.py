# Strictly Server Side

import requests 
import json

ZT_AUTH_TOKEN = "l0lwe4yv9r2tlvr1lswzxza2"

###### APIs for ZTO Network Controller
def getAllDevices(networkID):
    ZT_url = "http://localhost:9993/controller/network/" + networkID + "/member"
    try:
        ZT_response = requests.get(
            ZT_url,
            headers={
                "Content-type": "application/json; charset=UTF-8",
                "X-ZT1-AUTH": ZT_AUTH_TOKEN
            }
        )
        ZT_response.raise_for_status()
    except requests.exceptions.HTTPError as errh:
        print("Http Error:",errh)
    except requests.exceptions.ConnectionError as errc:
        print("Error Connecting:",errc)
    except requests.exceptions.Timeout as errt:
        print("Timeout Error:",errt)
    except requests.exceptions.RequestException as err:
        print("OOps: Something Else",err)
    except:
        print("OK")

    nodeIDs = list(ZT_response.json().keys())
    nodeList = []
    for nodeID in nodeIDs:
        ZT_url = "http://localhost:9993/controller/network/" + networkID + "/member/" + nodeID
        try:
            ZT_response = requests.get(
                ZT_url,
                headers={
                    "Content-type": "application/json; charset=UTF-8",
                    "X-ZT1-AUTH": ZT_AUTH_TOKEN
                }
            )
            ZT_response.raise_for_status()
        except requests.exceptions.HTTPError as errh:
            print("Http Error:",errh)
        except requests.exceptions.ConnectionError as errc:
            print("Error Connecting:",errc)
        except requests.exceptions.Timeout as errt:
            print("Timeout Error:",errt)
        except requests.exceptions.RequestException as err:
            print("OOps: Something Else",err)
        nodeList.append(ZT_response.json())
    return nodeList

def updateMember(networkID, nodeID, authorized=None, ipAssignment=None, name=None):
    ZT_url = "http://localhost:9993/controller/network/" + networkID + "/member/" + nodeID
    ZT_payload = {
        "authorized": authorized,
        "ipAssignments": [
            ipAssignment
        ],
        "name": name,
        "noAutoAssignIps": True,
        "activeBridge": True,
    }
    try:
        ZT_response = requests.post(
            ZT_url,
            headers={
                "Content-type": "application/json; charset=UTF-8",
                "X-ZT1-AUTH": ZT_AUTH_TOKEN
            },
            data=json.dumps(ZT_payload)
        )
        ZT_response.raise_for_status()
    except requests.exceptions.HTTPError as errh:
        print("Http Error:",errh)
    except requests.exceptions.ConnectionError as errc:
        print("Error Connecting:",errc)
    except requests.exceptions.Timeout as errt:
        print("Timeout Error:",errt)
    except requests.exceptions.RequestException as err:
        print("OOps: Something Else",err)
    return ZT_response

def deleteMember(networkID, nodeID):
    ZT_url = "http://localhost:9993/controller/network/" + networkID + "/member/" + nodeID
    try:
        ZT_response = requests.delete(
            ZT_url,
            headers={
                "Content-type": "application/json; charset=UTF-8",
                "X-ZT1-AUTH": ZT_AUTH_TOKEN
            }
        )
        ZT_response.raise_for_status()
    except requests.exceptions.HTTPError as errh:
        print("Http Error:",errh)
    except requests.exceptions.ConnectionError as errc:
        print("Error Connecting:",errc)
    except requests.exceptions.Timeout as errt:
        print("Timeout Error:",errt)
    except requests.exceptions.RequestException as err:
        print("OOps: Something Else",err)

    return ZT_response.status_code

def updateNetwork(networkID):
    ZT_url = "http://localhost:9993/controller/network/" + networkID
    ZT_payload = {
        "allowDNS": True,
        "ipAssignmentPools": [{
            "ipRangeStart": "10.173.0.0",
            "ipRangeEnd": "10.173.255.255"
        }],
        "routes": [{
            "target": "10.173.0.0/16", 
            "via": "10.173.0.1"
        }],
        "v4AssignMode": {
            "zt": True
        },
        "v6AssignMode": {
            "6plane": False,
            "rfc4193": False,
            "zt": False
        },
        "dns": {
            "domain": "archangel",
            "servers": ["10.173.0.1"]
        }
    }
    try:
        ZT_response = requests.post(
            ZT_url,
            headers={
                "Content-type": "application/json; charset=UTF-8",
                "X-ZT1-AUTH": ZT_AUTH_TOKEN
            },
            data=json.dumps(ZT_payload)
        )
        ZT_response.raise_for_status()
    except requests.exceptions.HTTPError as errh:
        print("Http Error:",errh)
    except requests.exceptions.ConnectionError as errc:
        print("Error Connecting:",errc)
    except requests.exceptions.Timeout as errt:
        print("Timeout Error:",errt)
    except requests.exceptions.RequestException as err:
        print("OOps: Something Else",err)
    return ZT_response