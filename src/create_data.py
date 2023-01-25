
import pickle
import csv


def create() -> list:
    geodata = []

    with open("IP2LOCATION-LITE-DB1.CSV", 'r') as fp:
        for start, stop, code, country in csv.reader(fp):
            data = {'start': int(start), 'stop': int(stop), 'code': code, 'country': country}
            geodata.append(data)

    with open("geoip.bin", "wb") as fp:
        pickle.dump(geodata, fp)

    return geodata


def test(geodata:list):
    print('testing...')
    print(len(geodata) == 215134)
    print(geodata[0]['stop'] == 16777215 and geodata[0]['code'] == '-', geodata[0])
    print(geodata[10]['stop'] == 16843263 and geodata[10]['code'] == 'US', geodata[10])
    print(geodata[1000]['stop'] == 37394431 and geodata[1000]['code'] == 'NL', geodata[1000])
    print(geodata[10000]['stop'] == 390643711 and geodata[10000]['code'] == 'AU', geodata[10000])


def main():
    geodata = create()
    test(geodata)


if __name__ == "__main__":
    main()
