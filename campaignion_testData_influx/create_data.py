#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 24 20:27:07 2018

@author: Philip Röggla – phylogram

Creates Random Data
"""
from itertools import count
from random import random, uniform

class randomWalk(object):
    """Provides drunken walk generators: x[n] = x[n-1] + rand"""
    
    """ Factor of default limits"""
    limitFactor = 10
    
    def __init__(self, initial_value= None, max_span=None,
                 upper_limit=False, lower_limit=0,
                 turning_point=None, length=2400):
        """ Provides drunken walk generators: x[n] = x[n-1] + rand
            Args:
                initial_value (int): Initial Value of the drunken walk. Defaults to 1000.
                max_span (float): The maximum percantage of step width (step[n] < step[n-1] * 1 + maxSpan) and (step[n] > step[n-1] * 1 - maxSpan). Defaults to 0.1
                bias (float): Biases the drunken walk to simulate a trend. Defaults to 0.3
                upper_limit (float, int): Will not exceed this absolute limit. If set to True, x[0]*10 and x[0]//10
                lower_limit (float, int): Will not exceed this absolute limit
                use_anti_bias (bool): When True will turn bias *= -1
                anti_bias_iterations (int, None): If set, will return to normal bias after * iterations
                stop (bool, int): If and when to stop iterations

        """
        self.turningPoint = turning_point if turning_point else uniform(0, 1)
        if not upper_limit:
            self.initialValue = initial_value if initial_value else 50/self.turningPoint
        else:
            # Scale
            self.initialValue = (1 - self.turningPoint) * (upper_limit - lower_limit) + lower_limit
        self._current_ = self.initialValue
        self.maxSpan = max_span if max_span else 3/(self.turningPoint * length)
        self._skew_ = self.maxSpan
        self._currentBias_ = True
        self._direction_ = 1
        if upper_limit is True:
            upper_limit = self.initialValue * self.limitFactor
        self.upperLimit = upper_limit
        if lower_limit is True:
            lower_limit = self.initialValue / self.limitFactor
        self.lowerLimit = lower_limit
        self.length = length
        turningPoint = self.turningPoint
        self.bias = (
                        (self.length**-1*x 
                             if x < turningPoint*self.length
                         else 
                             (self.length**-1*x*-3)+2*turningPoint) + turningPoint
                         for x in count()
                        )
                        
                        
    def __iter__(self):
        return self
    
    def __next__(self):
        return self.next()
    
    def next(self):
        bias = next(self.bias)
        self._thisBias_ = bias
        self._directionRandom_ = uniform(-1, 1)
        self._direction_ = +1 if self._directionRandom_ <= bias else -1
        self._skew_ = random() * self.maxSpan * self._direction_
        self._current_ *= 1+self._skew_
        if self.lowerLimit is not False or self.upperLimit is not False:
            self._limit_()
        # Python influxdb changes 2.0 to 2, and if this is the first value in a
        # Tag, this will determine the field type and lead to type errors, if
        # float follow. So make sure, that never ever leaves a f.0 this module!
        if self._current_ % 1 is 0:
            self._current_ += 0.000000001
        return self._current_
                
    def _limit_(self):
        """If current is out of bonds, cut"""
        if self.lowerLimit is not False and self._current_ < self.lowerLimit:
            self._current_ = self.lowerLimit
        if self.upperLimit is not False and self._current_ > self.upperLimit:
            self._current_ = self.upperLimit
        
                
class randomIntWalk(randomWalk):
    """Provides drunken walk generators for int: x[n] = x[n-1] + rand"""

    def next(self):
        super().next()
        self._current_ = int(self._current_ + 1) if self._direction_ is 1 else int(self._current_)
        if self.lowerLimit:
            self.lowerLimit = int(round(self.lowerLimit))
        if self.upperLimit:
            self.upperLimit = int(round(self.upperLimit))
        return self._current_

