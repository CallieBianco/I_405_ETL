# -*- coding: utf-8 -*-
"""
Created on Wed May 29 11:33:29 2019

@author: awsir
"""


from highway import Highway
from car import Car
from bus import Bus
import random
import file_saver
import numpy

min_price = 10
max_price = 10

vehicles_wa = 2925765
buses_wa = 23556
percent_bus = buses_wa / vehicles_wa 


sim_number = 1

time_range = 24 * 60 * 60
time_step = 1

length_highway = 11
n_exit_loc_array = [5, 7, 8, 9, 10]
s_exit_loc_array = [1, 2, 3, 5, 6]

enter_loc_array = [5, 7, 8, 9, 10]

north_peak_start = 15*60
north_peak_end = 17*60
peak_arr = []

for m in range(min_price):
    for n in range(m, max_price):
        for c in range(sim_number):
            north_highway = Highway(length_highway, min_toll=m, max_toll=n, exit_loc_arr=n_exit_loc_array)
            south_highway = Highway(length_highway, min_toll=m, max_toll=n, exit_loc_arr=s_exit_loc_array)
            n_vehicle_list = []
            print(n_vehicle_list)
            s_vehicle_list = []
            #North Highway
            for t in range(time_range):
                file_saver.graph_color_gradient(north_highway, t, m, n, 'north')
                #print(len(n_vehicle_list))
                n_total_moved_per_step = numpy.zeros((north_highway.width))
                while bool(random.randint(0, 5) <= 3):
                    if random.randint(0, 1000000) / 1000000.0 <= percent_bus:
                        enter_number = random.randint(0, len(north_highway.entrance_arr))
                        n_vehicle_list.append(Bus(3, north_highway.entrance_arr[enter_number - 1].y, north_highway.grid_per_mile))
                    else:
                        n_vehicle_list.append(Car('North', north_highway.grid_per_mile / 2.0, north_highway.grid_per_mile / 2.0, north_highway, north_highway.grid_per_mile))
                for i in reversed(list(n_vehicle_list)):
                    grids_squares_moved, north_highway, exited = i.move(north_highway, t)
                    n_total_moved_per_step[i.x-1] += grids_squares_moved
                    if exited == True:
                        if(north_highway.exits_arr[north_highway.exits_arr.index(i.exit)].count < north_highway.exits_arr[north_highway.exits_arr.index(i.exit)].max):
                            north_highway.exits_arr[north_highway.exits_arr.index(i.exit)].intake(i)  
                            n_vehicle_list.remove(i)
                for i in range(len(north_highway.exits_arr)):
                    north_highway.exits_arr[i].deplete()
                north_highway.gpl_speed = ((north_highway.get_speed(n_total_moved_per_step[1], (1/360.0), 1)) + (north_highway.get_speed(n_total_moved_per_step[2], (1/60.0), 2))) / 2.0
                north_highway.etl_speed = (north_highway.get_speed(n_total_moved_per_step[0], (1/360.0), 0))    
                    
            #South Highway
            for t in range(time_range):          
                file_saver.graph_color_gradient(south_highway, t, m, n, 'south')
                
                s_total_moved_per_step = numpy.zeros((north_highway.width))
                while bool(random.randint(0, 5) <= 3):
                    if random.randint(0, 1000000) / 1000000.0 <= percent_bus:
                        enter_number = random.randint(0, len(south_highway.entrance_arr))
                        s_vehicle_list.append(Bus(3, north_highway.entrance_arr[enter_number].y, south_highway.grid_per_mile))
                    else:
                        s_vehicle_list.append(Car('South', south_highway.grid_per_mile / 2.0, south_highway.grid_per_mile / 2.0, south_highway, south_highway.grid_per_mile))
                for i in reversed(list(s_vehicle_list)):
                    grids_squares_moved, south_highway, exited = i.move(south_highway, t)                   
                    s_total_moved_per_step[i.x-1] += grids_squares_moved
                    if exited == True:                        
                        if(south_highway.exits_arr[south_highway.exits_arr.index(i.exit)].count < south_highway.exits_arr[south_highway.exits_arr.index(i.exit)].max):
                            south_highway.exits_arr[south_highway.exits_arr.index(i.exit)].intake(i)  
                            n_vehicle_list.remove(i)
                for i in range(len(south_highway.exits_arr)):
                    south_highway.exits_arr[i].deplete()        
                south_highway.gpl_speed = ((south_highway.get_speed(s_total_moved_per_step[1], (1/360.0), 1)) + (south_highway.get_speed(s_total_moved_per_step[2], (1/60.0), 2))) / 2.0
                south_highway.etl_speed = (south_highway.get_speed(s_total_moved_per_step[0], (1/360.0), 0))     
