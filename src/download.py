import settings
import requests
import logging
import time
from pathlib import Path
from zipfile import ZipFile
from urllib.parse import urlencode
from collections.abc import Iterator


def request_successful(response: requests.Response) -> bool:
    if response.status_code >= 400:
        return False

    return response.text != "NO PERMISSION"


def dict_to_query_string(data: dict[str, str]) -> str:
    return urlencode(data)


def download_file(url:str, parameters:dict, output_file_path:str | Path) -> Path | None:
    path = Path(output_file_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    para = dict_to_query_string(parameters)
    download_url = f"{url}?{para}"
    response = requests.get(download_url)

    if not request_successful(response):
        logging.info(f'could not download the geoip database from {download_url}')
        return None

    path.write_bytes(response.content)

    return path


def unzip_file(zip_path:str, output_directory:str) -> None:
    output_path = Path(output_directory)
    output_path.mkdir(parents=True, exist_ok=True)

    with ZipFile(zip_path, "r") as zip_file:
        zip_file.extractall(output_path)


def wait_for_file(path:Path, timeout:float=60.0, check_interval:float=0.5, stable_time:float=1.0) -> bool:
    start_time = time.monotonic()
    last_size = -1
    stable_since = None

    while time.monotonic() - start_time < timeout:
        if path.exists():
            current_size = path.stat().st_size

            if current_size == last_size and current_size > 0:
                if stable_since is None:
                    stable_since = time.monotonic()
                elif time.monotonic() - stable_since >= stable_time:
                    return True
            else:
                stable_since = None

            last_size = current_size

        time.sleep(check_interval)

    return False


def download_files(download_dir:Path):
    if not download_dir.exists():
        download_dir.mkdir(exist_ok=True)

    if not settings.try_download:
        logging.info("download databse is disabled")
        exit()

    for code in settings.database_codes:
        download_url = f"{settings.GEOIP_DATA_BASE_URL}"

        parameters = {
            "token": settings.TOKEN,
            "file": code
        }

        zip_file_path = download_file(download_url, parameters, download_dir / f"geodata-{code}.zip")


def find_zip_archives(folder: Path) -> Iterator[Path]:
    yield from (
        path
        for path in folder.iterdir()
        if path.is_file() and path.suffix.lower() == ".zip"
    )


def unpack_files(download_dir:Path):

    for archive in find_zip_archives(download_dir):
        print(archive)

        try:
            time.sleep(20)
            unzip_file(archive, download_dir)
            logging.info('downloaded and unpacked new csv files')

        except Exception as e:
            logging.error(f"Could not unpack the geoip database {archive}: {e}"
        )


def purge_files(folder:Path, files:list[str]) -> None:
    for file in files:
        file_path = folder / file

        if file_path.exists():
            file_path.unlink()
            logging.info(f"removed file: {file_path}")


def main():
    download_path = settings.GEODATA_DOWNLOAD
    
    download_files(download_path)
    unpack_files(download_path)

    purge_files(download_path, ['LICENSE_LITE.TXT', 'README_LITE.TXT'])


if __name__ == "__main__":
    main()
