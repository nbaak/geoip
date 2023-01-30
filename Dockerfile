FROM python:3.10.2

RUN apt-get update && apt-get install -y cron nano
 
RUN python -m pip install --upgrade pip
RUN python -m pip install flask requests

RUN mkdir /geoip && cd /geoip
COPY ./src /geoip

ADD ./crontab/crontab /geoip/crontab

RUN groupadd -r geoip -g 1000 && \
    useradd -u 1000 -r -g geoip -s /sbin/nologin -c "Docker image user" geoip && \
    chown -R 1000:1000 /geoip && \
    crontab -u geoip /geoip/crontab && \
    chmod u+s /usr/sbin/cron

USER geoip

EXPOSE 22223
ENTRYPOINT ["/geoip/start.sh"]