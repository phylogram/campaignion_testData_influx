#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 24 20:27:07 2018

@author: Philip Röggla – phylogram

Writes data to influxdb
"""
from datetime import timedelta,datetime
from itertools import product, zip_longest
import importlib
import influxdb
from pandas import date_range
create_data = importlib.import_module('campaignion_testData_influx.create_data')


class influxdbTestData(object):
    
    rows_in_a_push = 100
    time_zone = 'UTC'  # Influx default timezone!
    
    def __init__(self, schema: dict, database: influxdb.DataFrameClient, start=None, end=None, freq='H'):
        """ Generates dicts with the right random generators 
        Args:
            scheme: a dict json like ...
            start: A time string, default 100 days ago
            stop: A time string default now
        """
        self.database = database
        self._addTimeRange(start, end, freq)
        self.schema = schema
        self._createIteratorDicts()
        self._row = 0
        
    def __iter__(self):
        return self
    
    def _addTimeRange(self, start, end, freq):
        self.start = start if start else datetime.now() - timedelta(days=100)
        self.end = end if end else datetime.utcnow()
        self.timerange = date_range(self.start, self.end, freq=freq, tz=self.time_zone)
        self.timerange_iterator = iter(self.timerange)
        self.length = self.timerange.shape[0]
        
    def _createIteratorDicts(self):
        self.IteratorDicts = list()
        for measurement_schema in self.schema['measurements']:
            iterator_dict = dict()
            iterator_dict['measurement'] = measurement_schema['measurement']
            
            # Create Tags
            iterator_dict['tags'] = dict()
            tags = list()
            index = 0
            iterator_dict['tags'] = dict()
            iterator_dict['tags']['indexes'] = dict()
            pass_items = []
            for tag, specification in measurement_schema['tags'].items():
                if tag in pass_items:
                    continue
                if 'grouped' in specification:
                    grouped_tag = specification['grouped']
                    grouped_values = measurement_schema['tags'][grouped_tag]['values']
                    values = zip_longest(specification['values'], grouped_values)
                    pass_items.append(grouped_tag)
                    iterator_dict['tags']['indexes'][(tag, grouped_tag)] = index
                else:
                    values = specification['values']
                    iterator_dict['tags']['indexes'][tag] = index
                tags.append(tuple(values))
                
                index += 1
            tags = tuple(tags)
            iterator_dict['tags']['tuple'] = tags
                            
                
            # Create fields
            iterator_dict['fields'] = dict()
            for field, specification in measurement_schema['fields'].items():
                data_type = specification['type']
                arguments = specification['random_arguments'] if 'random_arguments' in specification else dict()
                if data_type == "int":
                    randomClass = getattr(create_data, 'randomIntWalk')
                elif data_type == "float":
                    randomClass = getattr(create_data, 'randomWalk')
                else:
                    continue
                iterator_dict['fields'][field] = dict()
                for permutation in product(*tags):
                    iterator_dict['fields'][field][permutation] = randomClass(**arguments, length=self.timerange.shape[0])
            self.IteratorDicts.append(iterator_dict)
                
    
    def __next__(self):
        return self.next()
        
    def next(self):
        testData = self._createNextData()
        return self.database.write_points(testData)
        
    def _createNextData(self):
        
        testData = list()
        self._row += 1
        while (self._row % self.rows_in_a_push is not 0):            
            time = next(self.timerange_iterator)
            time = str(time.asm8)
            for iterator_dict in self.IteratorDicts:
                for permutation in product(*iterator_dict['tags']['tuple'] ):
                    testData_n = dict()
                    testData_n['measurement'] = iterator_dict['measurement']
                    
                    testData_n['tags'] = dict()
                    # Write tags
                    for tag, index in iterator_dict['tags']['indexes'].items():
                        if type(tag) is str:
                            testData_n['tags'][tag] = permutation[index]
                        elif type(tag) is tuple:
                            values = permutation[index]
                            for grouped_index, grouped_tag in enumerate(tag):
                                testData_n['tags'][grouped_tag] = values[grouped_index]
                    testData_n['fields'] = dict()
                    for field, generators in iterator_dict['fields'].items():
                        generator = generators[permutation]
                        testData_n['fields'][field] = next(generator)
                        
                    testData_n['time'] = time
                    testData.append(testData_n)
            self._row += 1
            
        return testData
        