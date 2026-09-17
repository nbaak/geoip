import os
import secret_service
import pathlib


def read_token(tokenfile):
    if os.path.exists(tokenfile):
        with open(tokenfile, 'r') as f:
            return f.read().strip()
    else:
        return None

DEBUG = False

# Overall
THIS_PATH = pathlib.Path(__file__).parent.resolve()
GEODATA_DOWNLOAD = THIS_PATH / "geodata"
SECRET_FILE = os.path.join(THIS_PATH, 'geoip.secret')

secret = secret_service.get_secret(SECRET_FILE)

# Update Service
# TOKEN = os.getenv('IP2LOCATION_TOKEN')
TOKEN = read_token(os.path.join(THIS_PATH, 'auth.token'))
try_download = True

# better to set TOKEN in your geoip.env file
if not TOKEN:
    TOKEN = 'YOUR_SECRET_TOKEN_IF_YOU_WANT_TO_CONFIG_HERE'
    try_download = False

GEOIP_DATA_BASE_URL = "https://www.ip2location.com/download"
if DEBUG:
    # overwrite GEOIP_DATA_BASE_URL and TOKEN
    GEOIP_DATA_BASE_URL = "http://localhost:5001/download"
    TOKEN = "TEST1234"

database_codes = ["DB3LITECSV", "DB3LITECSVIPV6"]
download_urls = [f"{GEOIP_DATA_BASE_URL}/?token={TOKEN}&file={code}" for code in database_codes]

# Geoip Service
port = 22223
