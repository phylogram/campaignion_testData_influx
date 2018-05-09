#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 24 20:27:07 2018

@author: Philip Röggla – phylogram

Run this scipt to write test data to influxdb and push dashboards to grafana
"""
from json import load
import config
from campaignion_testData_influx import write_test_data

def main():    
    with open(config.schema_path) as file:
        schema = load(file)
    writer = write_test_data(schema=schema, host=config.host, port=config.port,
                    username=config.username, password=config.password,
                    database_name=config.database, start_time=config.start_time,
                    end_time=config.end_time, freq=config.freq)
    for write in writer:
        if write:
            print(write)
    print('Done')
        
if __name__ == "__main__":
    main()
    
    