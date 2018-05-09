# campaignion_testData_influx
Holds a influx "schema" and writes "natural" random data to influx

## Requirements:
- python:
  - pandas
  - influxdb
- Influx (https://docs.influxdata.com/influxdb/v1.5/introduction/installation/)
## ./config.py !
- Influx-DB host, user, password, ...
- test database name!
- test time data: Currently -100 -> +30 days
## Run:
- python ./campaignion_testData_influx.script.py
## Grafana Dashboard:
- Set Influx & test database name as default data source!
- Copy or upload Grafana_Main_Dashboard.json to Grafana
## Influx "Schema":
At ./test_data_schema.json
"random_arguments" are not part of the "schema". They are for the drunken walk random generator.



