
import pickle
import logging
from binascii import hexlify
import socket
import time


class Geoip:

    def __init__(self, file='geoip.bin', file_v6=None):
        self.file = file
        self.file_v6 = file_v6

        self.load_data()

    def _load_data(self, file) -> bool:
        if not file:
            return None

        try:
            with open(file, 'rb') as fp:
                data = pickle.load(fp)

            data.sort(key=lambda x: x['start'])
            logging.info(f"loaded and sorted: {file}")
            return data

        except Exception as e:
            logging.error(f"{e}, {file}")
            return None

    def load_data(self) -> tuple:
        self.data_v4 = self._load_data(self.file)
        ipv4_loaded = True if self.data_v4 else False
        
        self.data_v6 = self._load_data(self.file_v6)
        ipv6_loaded = True if self.data_v6 else False
        
        return ipv4_loaded, ipv6_loaded

    def check_data(self):
        value = -1
        for data in self.data_v4:
            if value > data['start']:
                return False

            if data['stop'] < data['start']:
                return False

            value = data['start']

        return True

    def ip_to_int(self, ip:str) -> tuple:
        if '.' in ip:
            return self.ipv4_to_int(ip), 4

        elif ':' in ip:
            return self.ipv6_to_int(ip), 6

        else:
            return None, None

    def ipv4_to_int(self, ip:str) -> int:
        ip_parts = ip.split('.')
        if len(ip_parts) == 4:
            ip_parts = list(map(int, ip_parts))            
            a3, a2, a1, a0 = ip_parts
            return 256 ** 3 * a3 + 256 ** 2 * a2 + 256 * a1 + a0
        
        return None

    def ipv6_to_int(self, ip:str) -> int:
        try:
            return int(hexlify(socket.inet_pton(socket.AF_INET6, ip)), 16)
        except Exception as e:
            logging.error(f"{e}, ip:'{ip}'")
            return None

    def search_slow(self, ip:str):
        int_ip, version = self.ip_to_int(ip)
        int_ip_min = 0
        int_ip_max = 2 ** 32 - 1 if version == 4 else 2 ** 128 - 1

        if int_ip > int_ip_max or int_ip < int_ip_min:
            exit()

        data = self.data_v4 if version == 4 else self.data_v6

        for current_data in data:
            if int_ip >= current_data['start'] and int_ip <= current_data['stop']:
                return {'code': current_data['code'], 'country': current_data['country'], 'region': current_data['region'], 'city': current_data['city'], 'ip': ip}

    def search(self, ip:str):
        int_ip, version = self.ip_to_int(ip)   
        
        if int_ip == None: return None
        if version == None: return None     
        
        int_ip_min = 0
        int_ip_max = 2 ** 32 - 1 if version == 4 else 2 ** 128 - 1

        if int_ip > int_ip_max or int_ip < int_ip_min:
            exit()

        data = self.data_v4 if version == 4 else self.data_v6

        center_index = len(data) // 2
        lower_bounds = [0, center_index]
        upper_bounds = [center_index, len(data) - 1]

        trys = 0

        while True:
            current_data = data[center_index]

            if int_ip >= current_data['start'] and int_ip <= current_data['stop']:
                logging.info(f"finding {ip} took {trys} trys")
                return {'code': current_data['code'], 'country': current_data['country'], 'region': current_data['region'], 'city': current_data['city'], 'ip': ip}
            
            # print("IP", int_ip)
            # print("LB", data[lower_bounds[0]]['start'], data[lower_bounds[1]]['stop'])
            # print("UB", data[upper_bounds[0]]['start'], data[upper_bounds[1]]['stop'])
            
            if int_ip >= data[lower_bounds[0]]['start'] and int_ip <= data[lower_bounds[1]]['stop']:
                # go left
                center_index = ((lower_bounds[0] + center_index) // 2)
                upper_bounds = [center_index, lower_bounds[1]]
                lower_bounds = [lower_bounds[0], center_index]

            elif int_ip >= data[upper_bounds[0]]['start'] and int_ip <= data[upper_bounds[1]]['stop']:
                # go right
                center_index = ((upper_bounds[1] + center_index) // 2) + 1
                lower_bounds = [upper_bounds[0], center_index]
                upper_bounds = [center_index, upper_bounds[1]]

            trys += 1
        return None


if __name__ == '__main__':
    logging.basicConfig(format='%(message)s',
                        encoding='utf-8',
                        level=logging.INFO)
    b_g = time.time()
    geoip = Geoip('geoip.bin', 'geoip_v6.bin')
    
    # v4 quick test
    ips = ['77.64.121.231', '178.175.135.7', '185.220.100.255', '185.220.102.241']
    for ip in ips:
        print(geoip.search(ip))
    
    print()
    # v6 quick test
    ips = ['fe80::021b:77ff:fbd6:7860', '2001:4860:4860::8888', '2a02:8108:9c0:3788:754c:3142:cbdb:9ac', '2a02:2028:1038:1::34']
    for ip in ips:
        print(geoip.search(ip))

