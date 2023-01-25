# Geo Ip
To analyze the ssh tarpit data, I needed a correlation between ip-addresses and countrys. One solution could be to query some ip lookip services on the internet. The problem with that solution is, we maybe have to query a lot of data and the service will just ignore our requests. To solve this problem I set up my own Geoip service.

The basedata for this service is provided by <a href="https://www.ip2location.com/developers/python">ip2locaion.com</a>.

## Create your own geoip.bin
If you want to use the data from <a href="https://lite.ip2location.com/database/ip-country-region-city">lite.ip2locaion.com</a> you need to register your self and download the ip data (IP-COUNTRY-REGION-CITY). You can create your own geoip.bin file with the `create_data.py` script. 