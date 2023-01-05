
import pickle

class Geoip:
    
    def __init__(self, file="geoip.bin"):
        try:
            with open(file, 'rb') as fp:
                self.data = pickle.load(fp)
        except:
            self.data = None
            
    def test(self):
        print()
        print("test..")
        if self.data:
            print(len(self.data))
            print(self.data[0])
            print(self.data[1000])
            print(self.data[10000])
            print()
        else:
            print("no data found..")
    
    def ip_int(self, ip:str) -> int:
        a3,a2,a1,a0 = ip.split('.')
        a3,a2,a1,a0 = int(a3),int(a2),int(a1),int(a0)
        return 256**3*a3 + 256**2*a2 + 256*a1 + a0
            
    def search(self, ip:str):
        int_ip = self.ip_int(ip)
        
        for data in self.data:
            if int_ip >= data['start'] and int_ip <= data['stop']:
                return {"code": data['code'], "country": data['country'], "ip": ip}
            
        return None
    
    
if __name__ == "__main__":
    ## test it..
    geoip = Geoip()
    geoip.test()
    print(geoip.search("61.177.173.39"))
    
    
    