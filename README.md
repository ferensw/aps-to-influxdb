# aps-to-influxdb
Docker file to put data from APSystems tot InfluxDB

Simple script and Docker file to pull data from APSystems API and put in an InfluxDB

It can be used to build dashboards in e.g. Grafana.

Change the environment variables in the `docker-compose.yaml` file and run:
```
docker-compose up -d
```
## Environment variables
```
- ECU_ID=<ID of the APSystem ECU>
- INFLUXDB_HOST=
- INFLUXDB_PORT=
- INFLUXDB_USERNAME=
- INFLUXDB_PASSWORD=
- INFLUXDB_DATABASE=
- SEND_DATA_INTERVAL=300 (default)
- TZ=<Timezone of the APSystems ECU>
```
