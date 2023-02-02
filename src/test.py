#!/usr/bin/env python3

from Geoip import Geoip
import time
import logging
import sys
from tqdm import tqdm


def ip_generator():
    for a in range(256):
        for b in range(256):
            for c in range(256):
                for d in range(256):
                    yield f"{d}.{c}.{b}.{a}"


def test_geoip_basic(geoip:Geoip):
    print("Basic test - integrity")
    if geoip.data_v4:
        if geoip.check_data():
            print('data_v4 is consecutive')

    else:
        print('no data_v4 found..')


def test_some_ips(geoip:Geoip):
    print(len(geoip.data_v4))
    print(geoip.data_v4[0])
    print(geoip.data_v4[1000])
    print(geoip.data_v4[10000])
    print(geoip.data_v4[3109495])
    print(geoip.data_v4[3109496])

    print(geoip.data_v4[len(geoip.data_v4) - 1])
    print()

    print('test some ips:')
    start = time.time()
    print(geoip.search('0.0.0.0'))
    print(geoip.search('77.64.141.242'))
    print(geoip.search('14.49.113.37'))
    print(geoip.search('61.177.173.13'))
    print(geoip.search('61.177.172.91'))
    print(geoip.search('146.0.75.2'))
    print(geoip.search('193.3.19.178'))
    print(geoip.search('118.37.244.77'))
    print(geoip.search('61.177.173.39'))
    print(geoip.search('255.255.255.255'))

    print(geoip.search('224.0.0.0'))

    t1 = time.time() - start
    print(f"searching took {t1}s")
    print()


def test_all_ips(geoip:Geoip):
    print("testing ALL ip v4 addresses")
    start_main = time.time()

    for ip in tqdm(ip_generator(), total=255**4):
        geoip.search(ip)

    stop_main = time.time()

    print(f"test_all_ips took: {stop_main - start_main}s")


if __name__ == "__main__":
    logging.basicConfig(format='%(message)s',
                        encoding='utf-8',
                        level=logging.WARN)

    geoip = Geoip()

    test_geoip_basic(geoip)

    test_some_ips(geoip)

    if len(sys.argv) > 1:
        test_all_ips(geoip)

