# -*- coding: utf-8 -*-
"""
Created on Sat May 25 13:50:41 2019

@author: awsir
"""

from car import Car
from highway import Highway
import numpy as N
import math as M



EXPECTED_FREQ_COMM_AVG = 0.5

EXPECTED_POP_AVG = 1.5

EXPECTED_HAS_GTG_AVG = 0.5

MAX_AVG_ERR = 0.1



def car_setters_test():

    auto_veh = Car()

    freq_comm_avg = 0

    pop_avg = 0

    has_gtg_avg = 0

    for i in range(5000):

        freq_comm_avg += auto_veh.set_freq_commuter()

        pop_avg += auto_veh.set_pop()

        has_gtg_avg += auto_veh.set_has_gtg()

    freq_comm_avg /= 5000

    pop_avg /= 5000

    has_gtg_avg /= 5000

    if N.absolute(EXPECTED_FREQ_COMM_AVG - freq_comm_avg) <= 0.1:

        print("set_freq_commuter() passed")

    else:

        print("set_freq_commuter() may have some issues")

    if N.absolute(EXPECTED_POP_AVG - pop_avg) <= 0.1:

        print("set_pop() passed")

    else:

        print("set_pop() may have some issues")

    if N.absolute(EXPECTED_HAS_GTG_AVG - has_gtg_avg) <= 0.1:

        print("set_has_gtg() passed")

    else:

        print("set_has_gtg() may have some issues")

        
def highway_setters_test():
    
    length_in_miles = 10
    
    min_price = 0
    
    max_price = 1
    
    start_tolling = 5
    
    end_tolling = 19
    
    shoulder_start = 15
    
    shoulder_end = 17
    
    GPL = 2
    
    ETL = 1
    
    exits = [3, 4, 6]
    
    peak_arr = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    
    test_road = Highway(length_in_miles, num_norm_lns=GPL, \
                        num_etl=ETL, exit_loc_arr = exits, \
                        min_toll=min_price, max_toll=max_price, \
                        start_tolling=start_tolling, end_tolling=end_tolling, \
                        start_shoulder=shoulder_start, end_shoulder=shoulder_end, peak_arr=peak_arr)
    
    if N.shape(test_road.grid)[0] != test_road.grid_per_mile * length_in_miles:
        print("Possible problem in scaling road")
    else:
        print("Road Length Scaled")
    if N.shape(test_road.grid)[1] != 5:
        print("Possible problem in _generate_road construction")
    else:
        print("Road Width maintained")
    for i in exits:
        if test_road.grid[M.floor(i*test_road.grid_per_mile - 0.5 * test_road.grid_per_mile), 3, 3] != 2:
            print("Exit \t\t", i, " Not Generated Properly" )
        else:
            print("Exit \t\t", i, " Generated Properly")
        if test_road.grid[M.ceil(i*test_road.grid_per_mile + 0.5 * test_road.grid_per_mile), 3, 3] != 1:
            print("Entrance \t", i, " Not Generated Properly" )
        else:
            print("Entrance \t", i, " Generated Properly")
    
    for i in range(24):
        test_road.set_toll(i)
        if i >= start_tolling and i < end_tolling:
            if test_road.etl_price != min_price and test_road.etl_price != max_price:
                print("ETL Price Inaacurate: Problems in set_toll")
            else:
                print("ETL Price Accurate: set_toll has no known problems")
        else:
            if test_road.etl_price != 0:
                print("ETL Price Inaacurate: Problems in set_toll")                
            else:                
                print("ETL Price Accurate: set_toll has no known problems")
    
    for i in range(24):
        test_road.open_shoulder(i)
        """Known problems in openeing shoulder"""
        if i >= shoulder_start and i < shoulder_end:
            if test_road.shoulder_open == False:
                print("Error opening shoulder")
            else:
                print("Shoudler opened successfully")
        else:
            if test_road.shoulder_open == True:
                print("Error closing shoulder")
            else:
                print("Shoudler closed successfully")
        
            
    



def car_test():

    car_setters_test()

def highway_test():
    
    highway_setters_test()
    
    
if __name__ == "__main__":

    #car_test()
    
    highway_test()
