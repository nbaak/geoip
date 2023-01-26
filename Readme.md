# Geo Ip
To analyze the ssh tarpit data, I needed a correlation between ip-addresses and countrys. One solution could be to query some ip lookip services on the internet. The problem with that solution is, we maybe have to query a lot of data and the service will just ignore our requests. To solve this problem I set up my own Geoip service.

The basedata for this service is provided by <a href="https://www.ip2location.com/developers/python">ip2locaion.com</a>.


## Create your own geoip.bin
You need to create an account at <a href="https://lite.ip2location.com/download-database">lite.ip2locaion.com</a>. There you will find your Download Token. The download token is needed for the application to download the latest version of the database file.
Copy the Token into the geoip.env file and replace the placeholder string. Now run `docker-compose up -d`.

If you don't replace the placeholder string, the container will use an outdated version of the geoip data.


## IP2LOCATION
This site or product includes IP2Location LITE data available from http://www.ip2location.com.