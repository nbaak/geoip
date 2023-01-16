#!/usr/bin/env python3
from flask import Flask, jsonify, request
from Geoip import Geoip
import pathlib
import os

THIS_PATH = pathlib.Path(__file__).parent.resolve()

geoip = Geoip(os.path.join(THIS_PATH, 'geoip.bin'))
app = Flask(__name__)


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
    app.run(host="0.0.0.0", port=22223)

