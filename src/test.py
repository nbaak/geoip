#!/usr/bin/env python3

from geoip import Geoip
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


def test_ip_v4_search(geoip:Geoip):
    print('test ip v5 addresses')
    print(len(geoip.data_v4))
    print(geoip.data_v4[0])
    print(geoip.data_v4[1000])
    print(geoip.data_v4[10000])
    print(geoip.data_v4[-1])

    print(geoip.data_v4[len(geoip.data_v4) - 1])
    print()
    
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
    
    
def test_ip_v6_search(geoip:Geoip):
    print("test ip v6 addresses")
    
    ips = ['fe80::021b:77ff:fbd6:7860', '2001:4860:4860::8888', '2a02:8108:9c0:3788:754c:3142:cbdb:9ac', '2a02:2028:1038:1::34']
    start = time.time()
    for ip in ips:
        print(geoip.search(ip))
    stop = time.time()
    print(f"searching took {stop-start}s")
    print()
     

def test_all_ip_v4(geoip:Geoip):
    print("testing ALL ip v4 addresses")
    start_main = time.time()

    for ip in tqdm(ip_generator(), total=255**4):
        geoip.search(ip)

    stop_main = time.time()

    print(f"test_all_ip_v4 took: {stop_main - start_main}s")


if __name__ == "__main__":
    logging.basicConfig(format='%(message)s',
                        encoding='utf-8',
                        level=logging.WARN)

    geoip = Geoip('geoip.bin', 'geoip_v6.bin')

    test_geoip_basic(geoip)

    test_ip_v4_search(geoip)
    
    test_ip_v6_search(geoip)

    if len(sys.argv) > 1:
        test_all_ip_v4(geoip)

