# Geoip Data Host Mock
To test the Geoip service we want to use a mock because the original service allows us just 5 downloads per 24hr.

## How to use
Download the databases you need for your service and put them in the ./data directory.

Add the files to the DATABASES dictionary in settings.

Start the serive and install requirements.

Download database from `http://localhost:5001/download?token=TEST1234&file=DB3LITECSV`