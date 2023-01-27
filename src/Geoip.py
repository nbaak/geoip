
import pickle
import logging


class Geoip:

    def __init__(self, file='geoip.bin'):
        self.file = file
        self.load_data()

    def load_data(self) -> bool:
        try:
            with open(self.file, 'rb') as fp:
                self.data = pickle.load(fp)

            self.data.sort(key=lambda x: x['start'])

            return True
        except:
            self.data = None
            return False

    def check_data(self):
        value = -1
        for data in self.data:
            if value > data['start']:
                return False

            if data['stop'] < data['start']:
                return False

            value = data['start']

        return True

    def ip_int(self, ip:str) -> int:
        a3, a2, a1, a0 = ip.split('.')
        a3, a2, a1, a0 = int(a3), int(a2), int(a1), int(a0)
        return 256 ** 3 * a3 + 256 ** 2 * a2 + 256 * a1 + a0

    def search_slow(self, ip:str):
        int_ip = self.ip_int(ip)
        int_ip_min = self.ip_int('0.0.0.0')
        int_ip_max = self.ip_int('255.255.255.255')

        if int_ip > int_ip_max or int_ip < int_ip_min:
            exit()

        for data in self.data:
            if int_ip >= data['start'] and int_ip <= data['stop']:
                return {'code': data['code'], 'country': data['country'], 'region': data['region'], 'city': data['city'], 'ip': ip}

    def search(self, ip:str):
        int_ip = self.ip_int(ip)
        int_ip_min = self.ip_int('0.0.0.0')
        int_ip_max = self.ip_int('255.255.255.255')

        if int_ip > int_ip_max or int_ip < int_ip_min:
            exit()

        center_index = len(self.data) // 2
        lower_bounds = [0, center_index]
        upper_bounds = [center_index, len(self.data) - 1]

        trys = 0

        while True:
            data = self.data[center_index]

            if int_ip >= data['start'] and int_ip <= data['stop']:
                logging.info(f"finding {ip} took {trys} trys")
                return {'code': data['code'], 'country': data['country'], 'region': data['region'], 'city': data['city'], 'ip': ip}
            
            if int_ip >= self.data[lower_bounds[0]]['start'] and int_ip <= self.data[lower_bounds[1]]['stop']:
                # go left
                center_index = ((lower_bounds[0] + center_index) // 2)
                upper_bounds = [center_index, lower_bounds[1]]
                lower_bounds = [lower_bounds[0], center_index]

            elif int_ip >= self.data[upper_bounds[0]]['start'] and int_ip <= self.data[upper_bounds[1]]['stop']:
                # go right
                center_index = ((upper_bounds[1] + center_index) // 2) + 1
                lower_bounds = [upper_bounds[0], center_index]
                upper_bounds = [center_index, upper_bounds[1]]
            
            if trys > 150:
                logging.warning(f"fallback for {ip}")
                return self.search_slow(ip)

            trys += 1
        return None


if __name__ == '__main__':
    logging.basicConfig(format='%(message)s',
                        encoding='utf-8',
                        level=logging.INFO)
    # # test_all_ips it..
    geoip = Geoip()

