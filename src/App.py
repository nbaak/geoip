#!/usr/bin/env python3
from flask import Flask, jsonify, request
from Geoip import Geoip


geoip = Geoip()
app = Flask(__name__)



@app.route("/", defaults={'ip': None})
@app.route("/<string:ip>")
def find(ip):
    print("IP", type(ip), ip)
    if ip == None:
        ip = request.remote_addr
    
    data = geoip.search(ip)
        
    return jsonify(data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

