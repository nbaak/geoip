FROM python:3.10.2

RUN apt-get update && apt-get install -y cron nano
 
RUN python -m pip install --upgrade pip
RUN python -m pip install flask requests

RUN mkdir /geoip && cd /geoip
COPY ./src /geoip

ADD ./crontab/crontab /
RUN crontab /crontab

EXPOSE 22223
ENTRYPOINT ["/geoip/App.py"]