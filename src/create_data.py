
import pickle
import csv

geodata = []


with open("IP2LOCATION-LITE-DB1.CSV", 'r') as fp:
    reader = csv.reader(fp)
    
    for row in reader:
        start, stop, code, country = int(row[0]), int(row[1]), row[2], row[3]
        data = {'start': start, 'stop': stop, 'code': code, 'country': country}
        geodata.append(data)

with open("geoip.bin", "wb") as fp:
    pickle.dump(geodata, fp)

print(len(geodata)==215134)
print(geodata[0])
print(geodata[10])
print(geodata[1000])
print(geodata[10000])
