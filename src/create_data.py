
import pickle
import csv
import os
import pathlib


def create(geoip_db) -> list:
    geodata = []

    with open(geoip_db, 'r') as fp:
        for start, stop, code, country, region, city in csv.reader(fp):
            data = {'start': int(start), 'stop': int(stop), 'code': code, 'country': country, 'region': region, 'city': city}
            geodata.append(data)

    with open(os.path.join(pathlib.Path(geoip_db).parent.parent, 'geoip.bin'), 'wb') as fp:
        pickle.dump(geodata, fp)

    return geodata


def test(geodata:list):
    print('testing...')
    print(len(geodata))
    print(geodata[0])
    print(geodata[10])
    print(geodata[1000])
    print(geodata[10000])


def main():
    this_dir = pathlib.Path(__file__).parent.resolve()
    geoip_db = os.path.join(this_dir, 'geodata/IP2LOCATION-LITE-DB3.CSV')
    geodata = create(geoip_db)
    test(geodata)


if __name__ == '__main__':
    main()
