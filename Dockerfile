FROM python:alpine3.8

WORKDIR /app
COPY requirements.txt /app
RUN pip3 install -r requirements.txt

ENV ECU_ID=
ENV INFLUXDB_HOST=
ENV INFLUXDB_PORT=
ENV INFLUXDB_USERNAME=
ENV INFLUXDB_PASSWORD=
ENV INFLUXDB_DATABASE=
ENV SEND_DATA_INTERVAL=300
ENV TZ=

COPY ./aps_to_influxdb.py /app

ENTRYPOINT [ "python", "./aps_to_influxdb.py"]
