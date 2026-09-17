#!/usr/bin/env python3

import create_data
import download
import os
import settings
import requests
import logging
import time

from pathlib import Path
import argparse


def send_to_service():
    r = requests.get(f'http://127.0.0.1:{settings.port}/update/{settings.secret}')

    if r.status_code == 200:
        logging.info("successful loaded new data.")
        return True

    logging.info("failed to load new data.")
    return False


def download_data(download_path:Path) -> None:
    print("download data")
    download.download_files(download_path)


def unpack_data(download_path:Path, only:bool=False) -> None:
    if not only: time.sleep(10)
    print("unpack data")
    download.unpack_files(download_path)


def compile_data(download_path, only:bool=False) -> None:
    if not only: time.sleep(10)
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
    
    
def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Update GeoIP databases."
    )

    group = parser.add_mutually_exclusive_group()

    group.add_argument(
        "-d",
        "--download-only",
        action="store_true",
        help="Download databases only.",
    )

    group.add_argument(
        "-u",
        "--unpack-only",
        action="store_true",
        help="Unpack databases only.",
    )

    group.add_argument(
        "-c",
        "--compile-only",
        action="store_true",
        help="Compile databases only.",
    )

    return parser.parse_args()


def main():
    args = parse_arguments()
    
    download_path = settings.GEODATA_DOWNLOAD
    
    if args.download_only:
        download_data(download_path)
        return

    if args.unpack_only:
        unpack_data(download_path, only=True)
        return

    if args.compile_only:
        compile_data(download_path, only=True)
        return
    
    download_data(download_path)
    unpack_data(download_path)
    compile_data(download_path)
    
    send_to_service()
    cleanup()


if __name__ == '__main__':
    main()
