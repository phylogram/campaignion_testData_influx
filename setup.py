# -*- coding: utf-8 -*-
from setuptools import setup

setup(name='campaignion_testData_influx',
      version='0.1',
      description='''
      Holds a influx "schema" and writes "natural" random data to influx
      ''',
      url='http://github.com/phylogram/campaignion_testData_influx',
      author='Philip Röggla',
      author_email='philip.roeggla@phylogram.eu',
      license='MIT',
      packages=['set_up_grafana_and_influxdb'],
      install_requires=['pandas', 'influxdb'],
      python_requires='>=3',
      zip_safe=False)
