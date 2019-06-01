# -*- coding: utf-8 -*-
"""
Created on Wed May 22 10:09:02 2019

@author: awsir
"""

class Enter:
    def __init__(self, number, grids_per_mile, max_capacity=25,):   
        self.max = max_capacity
        self.count = 0
        self.number_dispensed = 0
        self.dispense_num = 5
        self.id = number
        
        self.y = number * grids_per_mile + (0.5*grids_per_mile)
        
    def intake(self, veh):
        self.count += 1
    
    def deplete(self):
        if self.count >= self.dispense_num:
            self.count -= self.dispense_num
            self.number_dispensed += self.dispense_num
        else:
            self.number_dispensed += self.count
            self.count = 0
