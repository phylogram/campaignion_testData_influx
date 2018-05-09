# -*- coding: utf-8 -*-
# Put influxdb and grafana connection details here:

# database
host=u'localhost'
port=8086
username=u'admin'
password=u'admin'
database=u'testData'

# timerange
from datetime import timedelta,datetime
start_time = datetime.utcnow() - timedelta(days=100)  # utc due to influx
end_time = datetime.utcnow() + timedelta(days=30)   # utc due to influx
freq = 'H' # Availible frequeny strings: http://pandas.pydata.org/pandas-docs/stable/timeseries.html#offset-aliases
# schema path
schema_path = './test_data_schema.json'
