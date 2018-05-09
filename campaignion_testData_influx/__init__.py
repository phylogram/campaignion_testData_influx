# class?
import time
from influxdb import InfluxDBClient
from .write_data import influxdbTestData


def write_test_data(schema: dict, host=u'localhost', port=8086, username=u'admin',
                    password=u'admin', database_name=u'testData',
                    start_time=None, end_time=None, freq='H'):
    
    try:
        database = InfluxDBClient(host, port, username, password)
        if database_name not in [item['name'] for item in database.get_list_database()]:
            database.create_database(database_name)
        database.switch_database(database_name)
    except Exception as e:
        database = InfluxDBClient(host, port, username, password)
        database.create_database(database_name)
        database.switch_database(database_name)
    writer = influxdbTestData(schema, database, start_time, end_time, freq)
    datapoints = writer.timerange.shape[0]
    time_to_say_hello = datapoints//10
    count = 0
    printed = 0
    t = time.perf_counter()
    for write in writer:
        count += 1
        if count%time_to_say_hello is 0:
            passed_time = time.perf_counter() - t
            t = time.perf_counter()
            printed += 1
            yield "Row {count} ({percent:.2f}%)\t\tTime: {time:.1f} s".format(count=str(count), percent=count*100/datapoints, time=passed_time) + ' . ' * printed + '   ' * (10-printed) + '|'
    
    