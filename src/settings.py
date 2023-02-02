import os
import secret_service
import pathlib


def read_token(tokenfile):
    with open(tokenfile, 'r') as f:
        return f.read()


# Overall
THIS_PATH = pathlib.Path(__file__).parent.resolve()
SECRET_FILE = os.path.join(THIS_PATH, 'geoip.secret')

secret = secret_service.get_secret(SECRET_FILE)

# Update Service
# token = os.getenv('IP2LOCATION_TOKEN')
token = read_token(os.path.join(THIS_PATH, 'auth.token'))
try_download = True

# better to set token in your geoip.env file
if not token:
    token = 'YOUR_SECRET_TOKEN_IF_YOU_WANT_TO_CONFIG_HERE'
    try_download = False

database_codes = ["DB3LITECSV", "DB3LITECSVIPV6"]
download_urls = [f"https://www.ip2location.com/download/?token={token}&file={code}" for code in database_codes]

# Geoip Service
port = 22223
