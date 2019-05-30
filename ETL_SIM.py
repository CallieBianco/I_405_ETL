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

min_price = 1000
max_price = 1000
price_interval = 0.01

vehicles_wa = 2925765
buses_wa = 23556
percent_bus = buses_wa / vehicles_wa 


sim_number = 1000000

time_range = 24 * 60
time_step = 1

length_highway = 8
exit_loc_array = []
enter_loc_array = []
peak_arr = []

for m in range(min_price):
    m *= price_interval
    for n in range(max_price):
        n *= price_interval
        for c in range(sim_number):
            north_highway = Highway(length_highway)
            south_highway = Highway(length_highway, min_toll=m, max_toll=n)
            n_vehicle_list = []
            s_vehcile_list
            #North Highway
            for t in range(time_range):
                total_moved_per_step = numpy.zeros((north_highway.width))
                while bool(random.getrandbits(1)):
                    if random.randint(0, 1000000) / 1000000.0 <= percent_bus:
                        enter_number = random.randint(0, len(north_highway.entrance_arr))
                        n_vehicle_list.append(Bus(3, north_highway.entrance_arr[enter_number], north_highway.grids_per_mile))
                    else:
                        n_vehicle_list.append(Car())
                shift = 0
                for i in range(len(n_vehicle_list)):
                    i -= shift
                    grids_squares_moved, north_highway, exited = n_vehicle_list[i].move(north_highway)
                    total_moved_per_step[vehicle_list[i].x-1] += grids_squares_moved
                    if exited == True:
                        north_highway.exits[(n_vehicle_list[i].exit)].intake(n_vehicle_list[i])                       
                        n_vehicle_list.remove(i)
                        shift += 1
                for i in range(len(north_highway.exits_arr)):
                    north_highway.exits_arr.deplete()
                    
                    
            #South Highway
            for t in range(time_range):           
                while bool(random.getrandbits(1)):
                    if random.randint(0, 1000000) / 1000000.0 <= percent_bus:
                        enter_number = random.randint(0, len(south_highway.entrance_arr))
                        s_vehicle_list.append(Bus(3, north_highway.entrance_arr[enter_number], south_highway.grids_per_mile))
                    else:
                        s_vehicle_list.append(Car())
                shift = 0
                for i in range(len(vehicle_list)):
                    i -= shift
                    grids_squares_moved, south_highway, exited = s_vehicle_list[i].move(south_highway)
                    if exited == True:                        
                        south_highway.exits[(s_vehicle_list[i].exit)].intake(s_vehicle_list[i]) 
                        s_vehicle_list.remove(i)
                        shift += 1
                for i in range(len(north_highway.exits_arr)):
                    north_highway.exits_arr.deplete()        
    
