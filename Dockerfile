FROM python:3.10.2

RUN python -m pip install --upgrade pip
RUN python -m pip install flask

RUN mkdir /geoip && cd /geoip
COPY ./src /geoip

EXPOSE 22223
ENTRYPOINT ["/geoip/App.py"]