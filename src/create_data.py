
import pickle
import csv


def create() -> list:
    geodata = []

    with open("geodata/IP2LOCATION-LITE-DB3.CSV", 'r') as fp:
        for start, stop, code, country, region, city in csv.reader(fp):
            data = {'start': int(start), 'stop': int(stop), 'code': code, 'country': country, 'region': region, 'city': city}
            geodata.append(data)

    with open("geoip.bin", "wb") as fp:
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
    geodata = create()
    test(geodata)


if __name__ == "__main__":
    main()
