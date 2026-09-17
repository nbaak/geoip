#!/usr/bin/env python3

import create_data
import download
import pathlib
import os
import settings
import requests
import logging
import time


def send_to_service():
    r = requests.get(f'http://127.0.0.1:{settings.port}/update/{settings.secret}')

    if r.status_code == 200:
        logging.info("successful loaded new data.")
        return True

    logging.info("failed to load new data.")
    return False


def create_database():
    this_path = pathlib.Path(__file__).parent.resolve()
    download_path = this_path / "geodata"
    print("download data")
    download.download_files(download_path)
    
    time.sleep(10)
    print("unpack data")
    download.unpack_files(download_path)
    
    time.sleep(10)
    print("compile data")
    if os.path.exists(os.path.join(download_path, 'IP2LOCATION-LITE-DB3.CSV')):
        geoip_db = os.path.join(download_path, 'IP2LOCATION-LITE-DB3.CSV')
        create_data.create(geoip_db, 'geoip.bin')

    if os.path.exists(os.path.join(download_path, 'IP2LOCATION-LITE-DB3.IPV6.CSV')):
        geoip_db = os.path.join(download_path, 'IP2LOCATION-LITE-DB3.IPV6.CSV')
        create_data.create(geoip_db, 'geoip_v6.bin')


def cleanup():
    files = [
        "geodata-DB3LITECSV.zip",
        "geodata-DB3LITECSVIPV6.zip",
        "IP2LOCATION-LITE-DB3.CSV",
        "IP2LOCATION-LITE-DB3.IPV6.CSV",
        "LICENSE_LITE.TXT",
        "README_LITE.TXT"
    ]

    download.purge_files(settings.GEODATA_DOWNLOAD, files)


if __name__ == '__main__':
    create_database()
    send_to_service()
    cleanup()
