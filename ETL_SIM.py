#=======================================================================
#                        General Documentation
#
    # Simulation Driver for I-405 Simulation
#
#-----------------------Additional Documentation------------------------

# Modification History:
# - 19 May 2019: ETL_SIM.py created by Adam Sirkis
# - 04 June 2019: ETL_SIM.py finalized by Adam Sirkis

# Notes:
# - Developed for Python 3.x

#=======================================================================

from highway import Highway
from car import Car
from bus import Bus
import random
import file_saver
import numpy
#Price ranges + 1, default from 0
min_price = 11
max_price = 11

#number of vehilces in Washignton State divided by the number of buses. Update for year
vehicles_wa = 2925765
buses_wa = 23556
percent_bus = buses_wa / vehicles_wa 

#Number of simulations to run for each time price
sim_number = 1

#Minutes in a day
time_range = 24 * 60
time_step = 1

#Length in miles
length_highway = 11
#distance from the start of the highway
n_exit_loc_array = [5, 7, 8, 9, 10]
s_exit_loc_array = [1, 2, 3, 5, 6]

enter_loc_array = [5, 7, 8, 9, 10]

#Peak times in minutes
north_peak_start = 15*60
north_peak_end = 17*60
north_peak_arr = []
south_peak_start = 7*60
south_peak_end = 9*60
south_peak_arr = []
for i in range(24*60):
    if i < north_peak_start or i > north_peak_end:
        north_peak_arr.append(0)
    if i >= north_peak_start and i <= north_peak_end:
        north_peak_arr.append(1)
    if i < south_peak_start or i > south_peak_end:
        south_peak_arr.append(0)
    if i >= south_peak_start and i <= south_peak_end:
        south_peak_arr.append(1)

n_speed_g = []
n_speed_e = []
s_speed_g = []
s_speed_etl = []

time_vs_money = numpy.zeros(11)
for m in range(min_price):
    for n in range(m, max_price):
        for c in range(sim_number):
            north_highway = Highway(length_highway, min_toll=m, max_toll=n, exit_loc_arr=n_exit_loc_array, peak_arr=north_peak_arr)
            south_highway = Highway(length_highway, min_toll=m, max_toll=n, exit_loc_arr=s_exit_loc_array, peak_arr=south_peak_arr)
            n_vehicle_list = []
            print(n_vehicle_list)
            s_vehicle_list = []
            #North Highway
            for t in range(time_range):
                file_saver.graph_color_gradient(north_highway, t, m, n, 'north')
                #print(len(n_vehicle_list))
                n_total_moved_per_step = numpy.zeros((north_highway.num_lns))
                shift = 0
                n_vehicle_list.reverse()
                for i in range(len(n_vehicle_list)):
                    i -= shift
                    grids_squares_moved, north_highway, exited = n_vehicle_list[i].move(north_highway, t)
                    n_total_moved_per_step[n_vehicle_list[i].x-1] += grids_squares_moved
                    if exited == True or n_vehicle_list[i].y + north_highway.grid_per_mile >= north_highway.length * north_highway.grid_per_mile:
                        if(north_highway.exits_arr[north_highway.exits_arr.index(n_vehicle_list[i].exit)].count < north_highway.exits_arr[north_highway.exits_arr.index(n_vehicle_list[i].exit)].max):
                            north_highway.exits_arr[north_highway.exits_arr.index(n_vehicle_list[i].exit)].intake(n_vehicle_list[i])  
                            north_highway.grid[n_vehicle_list[i].y, n_vehicle_list[i].x, 0] = 0
                            north_highway.grid[n_vehicle_list[i].y-1, n_vehicle_list[i].x, 0] = 0
                            if n_vehicle_list[i].y < 109:
                                north_highway.grid[n_vehicle_list[i].y+1, n_vehicle_list[i].x, 0] = 0
                            if n_vehicle_list[i].y < 108:
                                north_highway.grid[n_vehicle_list[i].y-2, n_vehicle_list[i].x, 0] = 0
                            n_vehicle_list.remove(n_vehicle_list[i])

                            shift += 1
                n_vehicle_list.reverse()
                north_highway.gpl_speed = ((north_highway.get_speed(n_total_moved_per_step[1], (1/360.0), 1)) + (north_highway.get_speed(n_total_moved_per_step[2], (1/60.0), 2))) / 2.0
                north_highway.etl_speed = (north_highway.get_speed(n_total_moved_per_step[0], (1/360.0), 0))    
                north_highway.set_toll(t)
                time_vs_money[north_highway.etl_price] += len(n_vehicle_list)
                n_speed_g.append(north_highway.gpl_speed)
                n_speed_e.append(north_highway.etl_speed)
                if t % 5 == 0:
                    for i in range(len(north_highway.exits_arr)):
                        north_highway.exits_arr[i].deplete()
                #chaneg based on anticipated traffic numbers
                while bool(random.randint(0, 50) <= 30):
                    if random.randint(0, 1000000) / 1000000.0 <= percent_bus:
                        enter_number = random.randint(0, len(north_highway.entrance_arr))
                        n_vehicle_list.append(Bus(3, north_highway.entrance_arr[enter_number - 1].y, 10))
                    else:
                        n_vehicle_list.append(Car('North', north_highway.grid_per_mile / 2.0, north_highway.grid_per_mile / 2.0, north_highway, 10))
                north_highway.gpl_speed = ((north_highway.get_speed(n_total_moved_per_step[1], (1/60.0), 1)) + (north_highway.get_speed(n_total_moved_per_step[2], (1/60.0), 2))) / 2.0
                north_highway.etl_speed = (north_highway.get_speed(n_total_moved_per_step[0], (1/60.0), 0))    
                north_highway.set_toll(t)
                time_vs_money[north_highway.etl_price] += len(n_vehicle_list)
                n_speed_g.append(north_highway.gpl_speed)
                n_speed_e.append(north_highway.etl_speed)
                #South Highway
                """ for t in range(time_range):          
                    file_saver.graph_color_gradient(south_highway, t, m, n, 'south')
                    
                    s_total_moved_per_step = numpy.zeros((north_highway.width))
                    for i in reversed(list(s_vehicle_list)):
                        grids_squares_moved, south_highway, exited = i.move(south_highway, t)                   
                        s_total_moved_per_step[i.x-1] += grids_squares_moved
                        if exited == True:                        
                            if(south_highway.exits_arr[south_highway.exits_arr.index(i.exit)].count < south_highway.exits_arr[south_highway.exits_arr.index(i.exit)].max):
                                south_highway.exits_arr[south_highway.exits_arr.index(i.exit)].intake(i)  
                                n_vehicle_list.remove(i)
                    for i in range(len(south_highway.exits_arr)):
                        south_highway.exits_arr[i].deplete()    
                    while bool(random.randint(0, 50) <= 15):
                        if random.randint(0, 1000000) / 1000000.0 <= percent_bus:
                            enter_number = random.randint(0, len(south_highway.entrance_arr))
                            s_vehicle_list.append(Bus(3, north_highway.entrance_arr[enter_number].y, 1))
                        else:
                            s_vehicle_list.append(Car('South', south_highway.grid_per_mile / 2.0, south_highway.grid_per_mile / 2.0, south_highway, 1))
                    south_highway.gpl_speed = ((south_highway.get_speed(s_total_moved_per_step[1], (1/360.0), 1)) + (south_highway.get_speed(s_total_moved_per_step[2], (1/60.0), 2))) / 2.0
                    south_highway.etl_speed = (south_highway.get_speed(s_total_moved_per_step[0], (1/360.0), 0))     
                    time_vs_money[south_highway.etl_price] += len(s_vehicle_list)
                    s_speed_g.append(south_highway.gpl_speed)
                    s_speed_e.append(nsouth_highway.etl_speed)"""