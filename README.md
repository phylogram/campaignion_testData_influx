# campaignion_testData_influx
Holds a influx "schema" and writes "natural" random data to influx

## Requirements:
- python 3:
  - pandas
  - influxdb
- Influx (https://docs.influxdata.com/influxdb/v1.5/introduction/installation/)
## Steps to run:
### ./config.py !
- Influx-DB host, user, password, ...
- Test database name: Default testData, will be created if not exists. If allready exists, may lead to unexpected results.
- test time data: Currently -100 -> +30 days
### Run Script:
- python3 ./campaignion_testData_influx.script.py
### Grafana Dashboard:
- Set Influx & test database name as default data source!
- Copy or upload Dashboards from ./grafana_dashboards/ to grafana
## More
### Influx "Schema":
At ./test_data_schema.json

"random_arguments" are not part of the "schema". They are for the drunken walk random generator.



