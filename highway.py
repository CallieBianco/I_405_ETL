#=======================================================================
#                        General Documentation
#
    # Agent for I-405 Simulation
#
#-----------------------Additional Documentation------------------------

# Modification History:
# - 19 May 2019: Bus.py created by Adam Sirkis
# - 04 June 2019: Bus.py finalized by Adam Sirkis

# Notes:
# - Developed for Python 3.x

#=======================================================================

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
                 start_tolling=500, end_tolling=1900, etl_on=[]):
        """ Construct a Highway
        
        Method Arguments:
            - length: number to rpesent the length of the highway
            - num_norm_lns : number of GPL lanes
            - num_etl: number of ETL
            -peak_arr : array-like of the peak traffic times
            - shoulder_arr[] : array-like of time the shoulder is open
            - min_toll : number repesenting the minimum toll
            - max_toll : number representing the maximum toll
            - exit_loc_arr : array-like representing the locatiosn of exit
            - start_tolling : time to start tolling
            - end_tolling : time to end tolling
            - etl_on : array-like of locations that vehicles can enter the ETL
            
        Member Variables:
            - num_lns : total number of lanes
            - grid_per_mile : number of grid squares per mile
            - shoulder_open : bool representing if the shoulder is open
            - etl_speed : current speed fo the ETL
            - gpl_speed : current speed of the GPL
            - Grid: 3-D Numpy arraay defined by _generate_road
        
        """
        self.num_norm_lns = num_norm_lns
        self.num_etl_lns = num_etl
        self.num_lns = num_norm_lns + num_etl
        self.length = length
        self.is_peak = numpy.array(peak_arr)
        self.is_shoulder = numpy.array(shoulder_arr)
        self.min_toll = min_toll
        self.max_toll = max_toll
        self.grid_per_mile = 10
        self.exits_arr = []
        self.entrance_arr = []
        self.tolling_start = start_tolling
        self.tolling_end = end_tolling
        self.shoulder_open = False
        self.etl_price = 0
        self.grid = self._generate_road(exit_loc_arr)
        self.etl_entry_arr = etl_on
        self.etl_speed = 60
        self.gpl_speed = 60

        
    def _generate_road(self, exits):
        """
        First Axis represents the length of the roadway
        
        Second Axis represents Width fo the roadway, including buffer barriers
        
        Axis 3 Stores extra information
        
        The first index stores if there is a vehicle (0 = false, 1 = true)
        The second index stores the type of terrain (0 = GPL, 1 = ETL, 2 = barrier)
        Third Index stores if it is an On-ramp, Off-ramp, or neither (0 = neither, 1 = On-ramp, 2 = Off-ramp)
        Fourth Index stores current price (GPL = 0.00, ETL = max_toll where is_peak is true, ETL = min_toll where is_peak = false and is_toll = true, ETL = 0.00 where is_peak and is_toll are false)
        
        
        Method Arguments:
            - exits: aray of exit locations
            
        Returns:
            - grid representing the roadway
        """
        roadway = numpy.zeros((self.length*self.grid_per_mile, self.num_norm_lns + self.num_etl_lns + 2, 4), dtype='f')
        #Build Barriers on Either side
        for i in range(numpy.shape(roadway)[0]):            
            roadway[i, 0, 1] = 2
            roadway[i, -1, 1] = 2
            for j in range(self.num_etl_lns):
                roadway[i, j + 1, 1] = 1
        #Generate Exits and Entrances (Paired Sets)
        for i in exits:
            roadway[math.floor(i*self.grid_per_mile), 3, 3] = 2
            self.exits_arr.append(Exit(i,self.grid_per_mile, i*self.grid_per_mile))
            roadway[math.ceil(i*self.grid_per_mile), 3, 3] = 1
            self.entrance_arr.append(Enter(i,self.grid_per_mile, i*self.grid_per_mile))
        roadway[self.length - 1, 3, 3] = 2
        roadway[self.length - 1, 2, 3] = 2
        roadway[self.length - 1, 1, 3] = 2
        self.exits_arr.append(Exit(self.length,self.grid_per_mile, self.length * self.grid_per_mile))
        roadway[0, 3, 3] = 1
        roadway[0, 2, 3] = 1
        roadway[0, 1, 3] = 1
        self.exits_arr.append(Enter(0,self.grid_per_mile, 0))        
        return roadway
    
    def get_speed(self, grid_moved, time, lane):
        """
        Calculate the Average speed of a lane
        
        Method Arguments:
            -lane i: index of the lane (from left to right)
            -grid_moved : the aggregate number of squares moved
            -time : is the timestep used (fractions of an hour)
        
        vehiucles must report number of squares moved
        """
        num_vehicles = 0
        for i in range(self.length*self.grid_per_mile):
            if self.grid[i, 1 + lane, 0] == 1:
                num_vehicles += 1
        if num_vehicles == 0:
            num_vehicles += 1
        miles_moved = grid_moved / self.grid_per_mile
        miles_per_vehicle = miles_moved / num_vehicles
        
        miles_per_vehicle_per_hour = miles_per_vehicle * 1 / time
        return miles_per_vehicle_per_hour
    
    def set_toll(self, time_step):
        """
        Set the toll fo the ETL
        
        Methdo Arguments:
            - time_step : numebr representing the time step in the seuqence
        """
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
        """
        Open the HSoulder
        
        Method Arguments:
            - time_step : number representing the time step in the sequence
        """
        if time_step >= self.start_shoulder and \
        time_step < self.end_shoulder and \
        self.shoulder_open == False:
            self.shoulder_open = True
            self.num_norm_lns += 1
        elif time_step >= self.start_shoulder \
        and time_step < self.end_shoulder \
        and self.shoulder_open == True:
            pass
        else:
            self.shoulder_open = False
            self.num_norm_lns -= 1
            
