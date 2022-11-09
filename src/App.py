
from flask import Flask,jsonify
from Geoip import Geoip


geoip = Geoip()
app = Flask(__name__)



@app.route("/find/<string:ip>")
def find(ip):
    data = geoip.search(ip)
    return jsonify(data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

