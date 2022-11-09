# Geo Ip
To analyze the ssh tarpit data, I needed a correlation between ip-addresses and countrys. One solution could be to query some ip lookip services on the internet. The problem with that solution is, we maybe have to query a lot of data and the service will just ignore our requests. To solve this problem I set up my own Geoip service.

The basedata for this service is provided by <a href="https://www.ip2location.com/developers/python">ip2locaion.com</a>.

## IP2LOCATION
If you want to use the data from <a href="https://www.ip2location.com/developers/python">ip2locaion.com</a> you need to register your self and download the ip data. You can create your own geoip.bin file with the `create_data.py` script. This might be a good idea because I don't know when my added `geoip.bin` file is outdated.