# -*- coding: utf-8 -*-
"""
Created on Wed May 22 10:09:02 2019

@author: awsir
"""

class Enter:
    def __init__(self, number, max_capacity=25, on_ramp_name):   
        self.on_ramp_name = on_ramp_name
        self.max = max_capacity
        self.count = 0
        self.number_dispensed = 0
        self.dispense_num = 5
        self.id = number
        
    def intake(self, veh):
        self.count += 1
    
    def deplete(self):
        if self.count >= self.dispense_num:
            self.count -= self.dispense_num
            self.number_dispensed += self.dispense_num
        else:
            self.number_dispensed += self.count
            self.count = 0
