
import pickle
import logging
from binascii import hexlify
import socket
import time


class Geoip:

    def __init__(self, file='geoip.bin'):
        self.file = file
        self.load_data()
        
    def _load_data(self, file) -> bool:
        try:
            with open(file, 'rb') as fp:
                data = pickle.load(fp)

            data.sort(key=lambda x: x['start'])

            return data
        except:
            return None

    def load_data(self) -> bool:
        self.data_v4 = self._load_data(self.file)
        # self.data_v6 = self._load_data(self.file_v6)

    def check_data(self):
        value = -1
        for data in self.data_v4:
            if value > data['start']:
                return False

            if data['stop'] < data['start']:
                return False

            value = data['start']

        return True

    def ip_to_int(self, ip:str) -> int:
        return self.ipv4_to_int(ip) if '.' in ip else self.ipv6_to_int(ip)
    
    def ipv4_to_int(self, ip:str) -> int:
        a3, a2, a1, a0 = ip.split('.')
        a3, a2, a1, a0 = int(a3), int(a2), int(a1), int(a0)
        return 256 ** 3 * a3 + 256 ** 2 * a2 + 256 * a1 + a0
    
    def ipv6_to_int(self, ip:str) -> int:
        return int(hexlify(socket.inet_pton(socket.AF_INET6, ip)), 16)

    def search_slow(self, ip:str):
        int_ip = self.ip_to_int(ip)
        int_ip_min = self.ip_to_int('0.0.0.0')
        int_ip_max = self.ip_to_int('255.255.255.255')

        if int_ip > int_ip_max or int_ip < int_ip_min:
            exit()

        for data in self.data_v4:
            if int_ip >= data['start'] and int_ip <= data['stop']:
                return {'code': data['code'], 'country': data['country'], 'region': data['region'], 'city': data['city'], 'ip': ip}

    def search(self, ip:str):
        int_ip = self.ip_to_int(ip)
        int_ip_min = self.ip_to_int('0.0.0.0')
        int_ip_max = self.ip_to_int('255.255.255.255')

        if int_ip > int_ip_max or int_ip < int_ip_min:
            exit()
                   
        data = self.data_v4

        center_index = len(data) // 2
        lower_bounds = [0, center_index]
        upper_bounds = [center_index, len(data) - 1]

        trys = 0

        while True:
            current_data = data[center_index]

            if int_ip >= current_data['start'] and int_ip <= current_data['stop']:
                logging.info(f"finding {ip} took {trys} trys")
                return {'code': current_data['code'], 'country': current_data['country'], 'region': current_data['region'], 'city': current_data['city'], 'ip': ip}
            
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
    geoip = Geoip()
    e_g = time.time()
    
    ip = 'fe80::021b:77ff:fbd6:7860'
    b_i = time.time()
    print(geoip.ip_to_int(ip))
    e_i = time.time()
    
    print(f"load geoip: {e_g - b_g}")
    print(f"load ipv6: {e_i - b_i}")

