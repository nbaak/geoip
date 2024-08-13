#!/usr/bin/env python3
from flask import Flask, jsonify, request, redirect
from geoip import Geoip
import os
import settings
import secret_service
from datetime import datetime

geoip = Geoip(os.path.join(settings.THIS_PATH, 'geoip.bin'))
# if you want ti support ipv6
# geoip = Geoip(os.path.join(settings.THIS_PATH, 'geoip.bin'), os.path.join(settings.THIS_PATH, 'geoip_v6.bin'))
app = Flask(__name__)

# app:variables
app_variables = {
    "last_update": None,
    "ipv4": None,
    "ipv6": None
    }


@app.route("/version")
def version(): 
    return redirect("/info", 302)


@app.route("/info")
def info(): 
    return jsonify(app_variables)


@app.route('/update/<string:secret>')
def update(secret):
    global last_update
    if secret_service.verify(secret, settings.SECRET_FILE):
        ipv4, ipv6 = geoip.load_data()
        if ipv4 or ipv6:
            app_variables["last_update"] = datetime.now()
            app_variables["ipv4"] = ipv4
            app_variables["ipv6"] = ipv6
            
            return "Data loaded", 200

    return "ERROR", 404


@app.route("/", defaults={'ip': None})
@app.route("/<string:ip>")
def find(ip):
    if ip == None:
        if 'HTTP_X_FORWARDED_FOR' in request.environ:
            ip = request.environ['HTTP_X_FORWARDED_FOR']
        elif 'REMOTE_ADDR' in request.environ:
            ip = request.remote_addr

    data = geoip.search(ip)

    return jsonify(data)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=settings.port)

