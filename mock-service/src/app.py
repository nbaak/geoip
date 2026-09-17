#!/usr/bin/env python3

import settings
from flask import Flask, abort, request, send_from_directory
# http://localhost:5001/download?token=TEST1234&file=DB3LITECSV

app = Flask(__name__)


@app.route("/")
def main():
    return "~o~"


@app.route('/download')
def download():
    # read all GET parameters
    token = request.args.get("token")
    file_handle = request.args.get("file")

    if not file_handle in settings.DATABASES:
        print(f"file not found!")
        return "Nope.. nice try", 404
    
    if token == settings.TOKEN:
        file_name = settings.DATABASES.get(file_handle)
        print(f"sending data: {settings.DATA_PATH} / {file_name}")
        
        return send_from_directory(
            settings.DATA_PATH,
            f"{file_name}",
            as_attachment=True,
        )
    
    else:
        print(f"invalid download token: {token}")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=settings.PORT)
