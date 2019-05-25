# -*- coding: utf-8 -*-
"""
Created on Wed May 22 10:08:24 2019

@author: awsir
"""
import numpy

from enter import Enter
from exit import Exit
"""from gpl import GPL
from etl import ETL"""

class Highway:
    def __init__(self, length, num_norm_lns=2, num_etl=1, peak_arr=[], \
                 toll_arr=[], shoulder_arr=[], min_toll=0.75, \
                 max_toll=10.00, exit_loc_arr=[], enter_loc_arr=[]):
        self.num_norm_lns = num_norm_lns
        self.num_etl_lns = num_etl
        self.length = length
        self.is_peak = numpy.array(peak_arr)
        self.is_toll = numpy.array(toll_arr)
        self.is_shoulder = numpy.array(shoulder_arr)
        self.min_toll = min_toll
        self.max_toll = max_toll
        self.grid_per_mile = 6
        self.exits_arr = []
        self.entrance_arr = []
        self.grid = self._generate_road(exit_loc_arr, enter_loc_arr)

        
    def _generate_road(self, exits, enters):
        """
        First Axis represents the length of the roadway
        
        Second Axis represents Width fo the roadway, including buffer barriers
        
        Axis 3 Stores extra information
        
        The first index stores if there is a vehicle (0 = false, 1 = true)
        The second index stores the type of terrain (0 = GPL, 1 = ETL, 2 = barrier)
        Third Index stores if it is an On-ramp, Off-ramp, or neither (0 = neither, 1 = On-ramp, 2 = Off-ramp)
        Fourth Index stores current price (GPL = 0.00, ETL = max_toll where is_peak is true, ETL = min_toll where is_peak = false and is_toll = true, ETL = 0.00 where is_peak and is_toll are false)
        """
        roadway = numpy.zeros((self.length*self.grid_per_mile, self.num_norm_lns + self.num_etl_lns + 2, 4), dtype='i')
        #Build Barriers on Either side
        for i in range(numpy.shape(roadway)[0]):            
            roadway[i, 0, 1] = 2
            roadway[i, -1, 1] = 2
        #Generate Exits
        for i in exits:
            roadway[i*self.grid_per_mile, 1, 3] = 2
            self.exits_arr.append(Exit(i/self.grid_per_mile))
        #Generate Entrances
        for i in enters:
            roadway[i*self.grid_per_mile, 1, 3] = 1
            self.entrance_arr.append(Enter(i/self.grid_per_mile))
        return roadway
    
    def get_speed(self, grid_moved, time, lane):
        """
        Calculate the Average speed of a lane
        
        lane is the index of the lane (from left to right) that the speed is being determined for
        grid_moved is the aggregate number of squares moved by vehicles in lane
        time is the timestep used in the driver program (fractions of an hour)
        """
        num_vehicles = 0
        for i in range(self.length*self.grid_per_mile):
            if self.grid[i, 1 + lane, 0] == 1:
                num_vehicles += 1
        miles_moved = grid_moved / self.grid_per_mile
        miles_per_vehicle = miles_moved / num_vehicles
        
        miles_per_vehicle_per_hour = miles_per_vehicle * 1 / time
        return miles_per_vehicle_per_hour