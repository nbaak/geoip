import settings
import requests, zipfile, io
import pathlib
import os
import logging


def download_and_unpack(download_dir:str):
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)
    
    if not settings.try_download:
        logging.info("download databse is disabled")
        exit()
    
    for download_url in settings.download_urls:
        r = requests.get(download_url)
        try:
            z = zipfile.ZipFile(io.BytesIO(r.content))
            z.extractall(download_dir)
            logging.info('downloaded and unpacked new csv files')
        except:
            logging.info(f'could not download the geoip database from {download_url}')


def purge_files(folder:str, files:list):
    for file in files:
        if os.path.exists(os.path.join(folder, file)):
            os.remove(os.path.join(folder, file))
            logging.info(f'removed file: {folder}/{file}')


def main():
    this_path = pathlib.Path(__file__).parent.resolve()
    download_path = os.path.join(this_path, './geodata')

    download_and_unpack(download_path)
    
    purge_files(download_path, ['LICENSE_LITE.TXT', 'README_LITE.TXT'])


if __name__ == "__main__":
    main()
