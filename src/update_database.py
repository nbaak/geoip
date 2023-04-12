#!/usr/bin/env python3

import create_data
import download
import pathlib
import os
import settings
import requests
import logging


def send_to_service():
    r = requests.get(f'http://127.0.0.1:{settings.port}/update/{settings.secret}')
    if r.status_code == 200:
        logging.info("successful loaded new data.")
        return True
    
    logging.info("failed to load new data.")
    return False


def create_database():
    this_path = pathlib.Path(__file__).parent.resolve()
    download_path = os.path.join(this_path, './geodata')
    download.download_and_unpack(download_path)

    if os.path.exists(os.path.join(download_path, 'IP2LOCATION-LITE-DB3.CSV')):
        geoip_db = os.path.join(download_path, 'IP2LOCATION-LITE-DB3.CSV')
        create_data.create(geoip_db, 'geoip.bin')
        
    if os.path.exists(os.path.join(download_path, 'IP2LOCATION-LITE-DB3.IPV6.CSV')):
        geoip_db = os.path.join(download_path, 'IP2LOCATION-LITE-DB3.IPV6.CSV')
        create_data.create(geoip_db, 'geoip_v6.bin')


if __name__ == '__main__':
    create_database()
    send_to_service()
