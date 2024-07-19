from flask import Flask
from flask import render_template
from flask import request
from flask import jsonify
from flask import g

from markupsafe import escape

import sqlite3
import json
from scripts.zt import getAllDevices, updateMember, deleteMember, updateNetwork
#from scripts.db import getCursor

app = Flask(__name__)

NW_ID = "81df17ee36bf1ee1"
DATABASE = './database.db'

#########################
###### MAIN ROUTES ######
#########################
@app.route("/network")
def network():
    devices = getAllDevices(NW_ID)
    print(devices)
    return render_template("network.html", data={"nw_id": NW_ID, "devices": devices})

@app.route("/live")
def live():
    return render_template("live.html", data={})

@app.route("/newStreamFrame")
def newStreamFrame():
    feeds = queryOpenStreamsServer()
    #### TO DO
    #### THIS IS WHERE WE JOIN THE MULTICAST GROUP AND USE MEDIAMTX CLI access to
    #### Add a path and then send teh webserver the right information taht it needs... depends on the local address
    #### of the c2 node.
    return render_template("newStreamFrame.html", data={"feeds": feeds})

@app.route("/airspace")
def airspace():
    return render_template("airspace.html")

#######################################
###### APIs for Feed Maintenence ######
#######################################
# Source of Truth for which UAS state lives on the Archangel Webserver (archangel.webserver)
# Feeds are pulled by C2 Nodes on the client-side... only the URLs of and state for UAS live on the server
@app.route("/uas/announceStreamStart/<nodeID>/<pathName>", methods=["POST"])
def announceStreamStart(nodeID, pathName):
    print(json.dumps(request.json))
    zt_nodeID = escape(nodeID)
    streamIP = escape(request.json["source_ip"])
    streamPort = escape(request.json["rtsp_port"])
    streamPath = escape(pathName)
    command = "INSERT INTO live_feeds (is_active, zt_node_id, ip, port, stream_path) VALUES (TRUE, '{}', '{}', '{}', '{}');".format(zt_nodeID, streamIP, streamPort, streamPath)
    commit_db(command)
    return jsonify(success=True)

@app.route("/uas/announceStreamEnd/<nodeID>/<pathName>", methods=["GET"])
def announceStreamEnd(nodeID, pathName):
    zt_nodeID = escape(nodeID)
    streamPath = escape(pathName)
    command = "UPDATE live_feeds SET is_active = FALSE WHERE zt_node_id =  '{}' AND stream_path = '{}';".format(zt_nodeID, streamPath)
    commit_db(command)
    return jsonify(success=True)

@app.route("/uas/queryOpenStreams", methods=["GET"])
def queryOpenStreams():
    command = "SELECT * FROM live_feeds WHERE is_active = TRUE;"
    feeds = query_db(command)
    return jsonify(success=True, feeds=feeds)

######################################
###### SERVER FUNCTIONS (Feeds) ######
######################################
def queryOpenStreamsServer():
    # I don't think I need the app context because I always call this from a view function...
    with app.app_context():
        command = "SELECT * FROM live_feeds WHERE is_active = TRUE;"
        return query_db(command)
        

############################################
###### APIs for ZTO Network Controller #####
############################################
@app.route("/zt/controller/network/archangel/member/<nodeID>", methods=["POST"])
def apiRelayMemberUpdate(nodeID):
    data = request.json
    newAuth = data.get("authorized")
    newIP = data.get("ipAssignment")
    newName = data.get("name")
    controllerResponse = updateMember(NW_ID, nodeID, authorized=newAuth, ipAssignment=newIP, name=newName)
    if controllerResponse.status_code == 200:
        return jsonify(success=True)
    elif controllerResponse.status_code == 404:
        return jsonify(success=False, message="The device was not found.")
    else:
        return jsonify(success=False, message="Unknown Error with the ZeroTier One Controller")
    
@app.route("/zt/controller/network/archangel/member/<nodeID>", methods=["DELETE"])
def apiRelayDeleteMember(nodeID):
    if deleteMember(NW_ID, nodeID) == 200:
        return jsonify(success=True)
    else:
        return jsonify(success=False)

@app.route("/zt/controller/network/archangel", methods=["POST"])
def apiRelayNetworkUpdate():
    controllerResponse = updateNetwork(NW_ID)
    print(controllerResponse.json())
    if controllerResponse.status_code == 200:
        return jsonify(success=True)
    elif controllerResponse.status_code == 404:
        return jsonify(success=False, message="The network was not found.")
    else:
        return jsonify(success=False, message="Unknown Error with the ZeroTier One Controller")

################################
###### DATABASE MANAGEMENT #####
################################
def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('./static/schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        
    def make_dicts(cursor, row):
        return dict((cursor.description[idx][0], value) for idx, value in enumerate(row))
    db.row_factory = make_dicts
    return db

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

def commit_db(query, args=()):
    db = get_db()
    db.execute(query, args)
    db.commit()

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()