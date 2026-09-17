from pathlib import Path


# service port
PORT = 5001

# service root directory
ROOT_PATH = Path(__file__).parent.resolve()

DATA_PATH = ROOT_PATH / "data"

# token to download db
TOKEN = "TEST1234"

# dbs we serve
DATABASES = {
    "DB3LITECSV": "IPV4.CSV.zip",
    "DB3LITECSVIPV6": "IPV6.CSV.zip",
}
