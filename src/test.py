#!/usr/bin/env python3

from Geoip import Geoip
import time
import logging
import sys


def progressBar(iterable, total:int=None, prefix='', suffix='', decimals=1, length=100, fill='█', printEnd="\r"):
    """
    Call in a loop to create terminal progress bar
    https://stackoverflow.com/questions/3173320/text-progress-bar-in-terminal-with-block-characters
    @params:
        iterable    - Required  : iterable object (Iterable)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    total = len(iterable) if total == None else total

    # Progress Bar Printing Function
    def printProgressBar (iteration):
        percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
        filledLength = int(length * iteration // total)
        bar = fill * filledLength + '-' * (length - filledLength)
        print(f'\r{prefix} |{bar}| {percent}% {suffix}', end=printEnd)

    # Initial Call
    printProgressBar(0)
    # Update Progress Bar
    for i, item in enumerate(iterable):
        yield item
        printProgressBar(i + 1)
    # Print New Line on Complete
    print()


def ip_generator():
    for a in range(256):
        for b in range(256):
            for c in range(256):
                for d in range(256):
                    yield f"{d}.{c}.{b}.{a}"


def test_geoip_basic(geoip:Geoip):
    print("Basic test - integrity")
    if geoip.data:
        if geoip.check_data():
            print('data is consecutive')

    else:
        print('no data found..')


def test_some_ips(geoip:Geoip):
    print(len(geoip.data))
    print(geoip.data[0])
    print(geoip.data[1000])
    print(geoip.data[10000])
    print(geoip.data[3109495])
    print(geoip.data[3109496])

    print(geoip.data[len(geoip.data) - 1])
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
    counter = 0
    start_main = time.time()

    # logging.info("testing: ", ip, counter)
    for ip in progressBar(ip_generator(), 255**4):
        geoip.search(ip)
        counter += 1

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

