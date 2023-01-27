

from Geoip import Geoip
import time


def ip_creator():
    for a in range(256):
        for b in range(256):
            for c in range(256):
                for d in range(256):
                    yield f"{d}.{c}.{b}.{a}"


def test():
    geoip = Geoip()
    
    start_main = time.time()
    for ip in ip_creator():
        data = geoip.search(ip)
        # print(data)
        # time.sleep(.25)
        
        
    stop_main = time.time()
    
    print(f"test took: {stop_main - start_main}s")

if __name__ == "__main__":
    test()
