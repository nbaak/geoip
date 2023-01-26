#!/usr/bin/env python3

import create_data
import download
import pathlib
import os


def main():
    this_path = pathlib.Path(__file__).parent.resolve()
    download_path = os.path.join(this_path, './geodata')
    download.download_and_unpack(download_path)

    if os.path.exists(os.path.join(download_path, 'IP2LOCATION-LITE-DB3.CSV')):
        geoip_db = os.path.join(download_path, 'IP2LOCATION-LITE-DB3.CSV')
        create_data.create(geoip_db)


if __name__ == '__main__':
    main()
