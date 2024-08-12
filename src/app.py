#!/usr/bin/env python3
from flask import Flask, jsonify, request
from geoip import Geoip
import os
import settings
import secret_service
from datetime import datetime

geoip = Geoip(os.path.join(settings.THIS_PATH, 'geoip.bin'))
app = Flask(__name__)


# app:variables
last_update = None


@app.route("/version")
def version():
    app_data = {
        "last_update": last_update,        
        }
    
    return jsonify(app_data)


@app.route('/update/<string:secret>')
def update(secret):
    global last_update
    if secret_service.verify(secret, settings.SECRET_FILE):
        if geoip.load_data():
            last_update = datetime.now()
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

