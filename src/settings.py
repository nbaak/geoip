import os

token = os.getenv('IP2LOCATION_TOKEN')
try_download = True

# better to set token in your geoip.env file
if not token:
    token = "YOUR_SECRET_TOKEN_IF_YOU_WANT_TO_CONFIG_HERE"
    try_download = False

database_code = "DB3LITECSV"
downlaod_url = f"https://www.ip2location.com/download/?token={token}&file={database_code}"