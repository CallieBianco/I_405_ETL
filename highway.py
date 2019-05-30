# -*- coding: utf-8 -*-
"""
Created on Wed May 22 10:08:24 2019

@author: awsir
"""
import numpy
import math

from enter import Enter
from exit import Exit
"""from gpl import GPL
from etl import ETL"""

class Highway:
    def __init__(self, length, num_norm_lns=2, num_etl=1, peak_arr=[],\
                 shoulder_arr=[], min_toll=0.75, \
                 max_toll=10.00, exit_loc_arr=[],\
                 start_shoulder=1500, end_shoulder=1700,
                 start_tolling=500, end_tolling=1900):
        self.num_norm_lns = num_norm_lns
        self.num_etl_lns = num_etl
        self.length = length
        self.width = num_norm_lns + num_etl
        self.is_peak = numpy.array(peak_arr)
        self.is_shoulder = numpy.array(shoulder_arr)
        self.min_toll = min_toll
        self.max_toll = max_toll
        self.grid_per_mile = 60
        self.exits_arr = []
        self.entrance_arr = []
        self.tolling_start = start_tolling
        self.tolling_end = end_tolling
        self.start_shoulder=start_shoulder
        self.end_shoulder = end_shoulder
        self.shoulder_open = False
        self.etl_price = 0
        self.grid = self._generate_road(exit_loc_arr)

        
    def _generate_road(self, exits):
        """
        First Axis represents the length of the roadway
        
        Second Axis represents Width fo the roadway, including buffer barriers
        
        Axis 3 Stores extra information
        
        The first index stores if there is a vehicle (0 = false, 1 = true)
        The second index stores the type of terrain (0 = GPL, 1 = ETL, 2 = barrier)
        Third Index stores if it is an On-ramp, Off-ramp, or neither (0 = neither, 1 = On-ramp, 2 = Off-ramp)
        Fourth Index stores current price (GPL = 0.00, ETL = max_toll where is_peak is true, ETL = min_toll where is_peak = false and is_toll = true, ETL = 0.00 where is_peak and is_toll are false)
        """
        roadway = numpy.zeros((self.length*self.grid_per_mile, self.num_norm_lns + self.num_etl_lns + 2, 4), dtype='f')
        #Build Barriers on Either side
        for i in range(numpy.shape(roadway)[0]):            
            roadway[i, 0, 1] = 2
            roadway[i, -1, 1] = 2
        #Generate Exits and Entrances (Paired Sets)
        for i in exits:
            roadway[math.floor(i*self.grid_per_mile - (0.1 * self.grid_per_mile)), 3, 3] = 2
            self.exits_arr.append(Exit(i/self.grid_per_mile))
            roadway[math.ceil(i*self.grid_per_mile + 0.1 * self.grid_per_mile), 3, 3] = 1
            self.entrance_arr.append(Enter(i/self.grid_per_mile))
        return roadway
    
    def get_speed(self, grid_moved, time, lane):
        """
        Calculate the Average speed of a lane
        
        lane is the index of the lane (from left to right) that the speed is being determined for
        grid_moved is the aggregate number of squares moved by vehicles in lane
        time is the timestep used in the driver program (fractions of an hour)
        
        vehiucles must report lane number and number of squares moved
        """
        num_vehicles = 0
        for i in range(self.length*self.grid_per_mile):
            if self.grid[i, 1 + lane, 0] == 1:
                num_vehicles += 1
        miles_moved = grid_moved / self.grid_per_mile
        miles_per_vehicle = miles_moved / num_vehicles
        
        miles_per_vehicle_per_hour = miles_per_vehicle * 1 / time
        return miles_per_vehicle_per_hour
    
    def set_toll(self, time_step):
        if time_step >= self.tolling_start and time_step < self.tolling_end:
            if self.is_peak[time_step]:
                self.etl_price = self.max_toll
                for i in range(numpy.shape(self.grid)[0]):
                    self.grid[i, 1, 3] = self.max_toll
            else:
                for i in range(numpy.shape(self.grid)[0]):
                    self.grid[i, 1, 3] = self.min_toll
                self.etl_price = self.min_toll
        else:
            for i in range(numpy.shape(self.grid)[0]):
                self.grid[i, 1, 3] = 0
            self.etl_price = 0

    def open_shoulder(self, time_step):
        if time_step >= self.start_shoulder and time_step < self.end_shoulder and self.shoulder_open == False:
            self.shoulder_open = True
            self.num_norm_lns += 1
            """temp = numpy.zeros(numpy.shape((self.length*self.grid_per_mile, self.num_norm_lns + self.num_etl_lns + 3, 4)), dtype='f')
            temp[:, 0:-2, :] = self.grid[:, 0:-1, :]
            temp[:, self.num_norm_lns + self.num_etl_lns + 2, :] = self.grid[:, -1, :]
            for i in range(numpy.shape(self.grid)[0]):
                temp[i, -2, 1] = 0"""
        elif time_step >= self.start_shoulder and time_step < self.end_shoulder and self.shoulder_open == True:
            pass
        else:
            self.shoulder_open = False
            self.num_norm_lns -= 1
            