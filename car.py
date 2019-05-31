# -*- coding: utf-8 -*-

"""

Created on Wed May 22 10:08:13 2019

@author: CallieBianco

"""

# to be combined with Abdullahi's code for Car.py
import numpy as np
import Income_Data as inc

class Car(object):
    """ Defines a car object.
    
        Data fields:
            on_ramp:          On-ramp name from which car enters I-405, 
                              associated with a city
            off_ramp:         Exit number that which car leaves I-405.
            has_gtg:          Whether or not a car has a Good-to-Go! Account
            pop:              Number of passengers in car, including driver 
            can_shift_left:   Boolean if car can shift left
            can_move_forward: Boolean if car can move forward
            can_shift_right:  Boolean if car can shift right
            income:           How much money car makes
            length:           How many grid lengths a car is
            freq_commuter:    Boolean if they are a frequent commuter or not
            in_a_hurry:       Boolean if in a hurry
            crashed:          Boolean for if car has crashed
            horiz:            Car's position on the x-axis
            vertic:           Car's position on the y-axis
            speed:            How fast a car is moving
            
        Constraints:
            * on_ramp and off_ramp will fall between Everett and Bellevue
            * 1 <= pop <= 8 (we are not considering vans)
            * in_a_hurry will be decided on a random basis 
            * For this model, a Good-to-Go! pass will act as a Flex Pass
              for carpooling (pop >= 3) cars. (free access to ETL)
    """
    
    def __init__(self, direction, near_etl_length, near_exit_length, highway, \
                 max_forward_moves):
        self.direction = direction
        self.inc_data = inc.Income_Data()
        self.on_ramp = self.init_on_ramp()
        self.off_ramp = self.init_off_ramp()
        self.income_class = self._class_breakdown() 
        self.city = self._city_data()
        self.income = self.init_income()
        self.has_gtg = self.init_has_gtg()
        self.pop = self.init_pop()
        self.freq_commuter = self.init_freq_commuter()
        self.in_a_hurry = self.init_hurry()
        self.going_to_etl = False
        self.on_etl = False
        self.etl_entry_coord = [0,0] # (vertic, horiz)
        self.horiz = 3
        self.vertic = 1
        self.near_etl_length = near_etl_length
        self.highway = highway
        self.max_forward_moves = max_forward_moves
    
    def init_on_ramp(self):
        # Hard to find data for
        # Educated guess of percentages based on populations
        # Found population of each city associated with an on-ramp
        # Divided each by the total (that percentage is the chance that
        # a car entered from that on-ramp)
        south_pops = [110079, 38273, 21337, 45533, 45533]
        total_s = np.sum(south_pops)
        chances_s = np.zeros(len(south_pops))
        for i in range(len(chances_s)):
            chances_s[i] = south_pops[i] / total_s
            
        north_pops = [144444, 64291, 88630, 45533]
        total_n = np.sum(north_pops)
        chances_n = np.zeros(len(north_pops))
        for i in range(len(chances_n)):
            chances_n[i] = north_pops[i] / total_n
            
        on_ramps_south = ['I5 North', 'I5 South1','I5 South2', 'Canyon Park', \
                          'WA_522']                  
        on_ramps_north = ['Bellevue 4th St', 'Redmond Way', 'Central Way', \
                          'WA 527']
        
        chance = np.random.uniform()
        if self.direction == 'South':
            if chance < chances_s[0]:
                return on_ramps_south[0]
            elif chance > chances_s[0] and chance < np.sum(chances_s[0:2]):
                return on_ramps_south[1]
            elif chance > chances_s[1] and chance < np.sum(chances_s[0:3]):
                return on_ramps_south[2]
            elif chance > chances_s[2] and chance < np.sum(chances_s[0:4]):
                return on_ramps_south[3]
            elif chance > chances_s[3] and chance < np.sum(chances_s[0:5]):
                return on_ramps_south[4]
                
        elif self.direction == 'North':
            if chance < chances_n[0]:
                return on_ramps_north[0]
            elif chance > chances_n[0] and chance < np.sum(chances_n[0:2]):
                return on_ramps_north[1]
            elif chance > chances_n[1] and chance < np.sum(chances_n[0:3]):
                return on_ramps_north[2]
            elif chance > chances_n[2] and chance < np.sum(chances_n[0:4]):
                return on_ramps_north[3]
        
    def init_off_ramp(self):
        # randomly assigned off_ramps
        # Constraint: All exits are between Lynnwood and Bothell
        # Southbound: includes a "past Bothell" exit
        # Northbound: includes a "before Bothell" exit
        south_exits = ['SR 527', 'NE 195th', 'SR 522', 'NE 160th', 'NE 124th', \
                       'Past Bothell']
        north_exits = ['Before Bothell', 'SR 527', 'I5 North', 'I5 South', \
                       'SR 525']
        # Assume at least half of cars are going to go past Bothell
        if self.direction == 'South':
            if self.on_ramp == 'Bothell':
                return south_exits[-1]
            else:
                rand = np.random.uniform()
                if rand <= .5:
                    return south_exits[-1]
                else:
                    rint = np.random.randint(0,5)
                    return south_exits[rint]
        # Assume at least half of cars will exit before Bothell
        else:
            if self.on_ramp != 'Bothell':
                rand = np.random.uniform()
                if rand <= .5:
                    return north_exits[0]
                else:
                    rint = np.random.randint(1,5)
                    return north_exits[rint]
            else:
                rint = np.random.randint(1,5)
                return north_exits[rint]
        
    def init_income(self):
        """ Initializes income of a car based on city-data.
            
            Assumes income of car is the driver's income.
        """       
        if self.city == 'Everett':
            return self.inc_data.ev_inc(self.income_class)
        elif self.city == 'Lynnwood':
            return self.inc_data.lynn_inc(self.income_class) 
        elif self.city == 'Mountlake Terrace':
            return self.inc_data.mlt_inc(self.income_class)
        elif self.city == 'Bothell':
            return self.inc_data.bot_inc(self.income_class)
        elif self.city == 'Bellevue':
            return self.inc_data.bell_inc(self.income_class)
        elif self.city == 'Redmond':
            return self.inc_data.red_inc(self.income_class)
        elif self.city == 'Kirkland':
            return self.inc_data.kirk_inc(self.income_class)
    
    def _class_breakdown(self):
        low, mid_low, mid, mid_upper, upper = 0.0, 0.0, 0.0, 0.0, 0.0
        classes = ['low', 'low mid', 'mid', 'upper mid', 'upper']
        breakdown = [low, mid_low, mid, mid_upper, upper]
        for i in range(len(classes)):
            breakdown[i] = self.inc_data.income_breakdown[classes[i]] / 100.0
        l = breakdown[0]
        lm = l + breakdown[1]
        m = lm + breakdown[2]
        mu = m + breakdown[3]
        
        assign = np.random.uniform()
        if assign < l:
            income_class = 'low'
        elif assign > l and assign < lm:
            income_class = 'low mid'
        elif assign > lm and assign < m:
            income_class = 'mid'
        elif assign > m and assign < mu:
            income_class = 'upper mid'
        else:
            income_class = 'upper'
            
        return income_class
        
    def _city_data(self):             
        if self.direction == 'South':
            entered = self.inc_data.on_ramps_south[self.on_ramp]
        else:
            entered = self.inc_data.on_ramps_north[self.on_ramp] 
            
        return entered       

    
    def init_has_gtg(self):
        GTG_PASS_PROB = 0.5
        if np.random.uniform(0, 1) < GTG_PASS_PROB:
            return True
        else:
            return False  
            
    def init_pop(self):
        POP_PROBS = np.array([[1,2,3,4,5], [0.764, 0.884, 0.944, 0.974, 1]])
        rand = np.random.uniform(0, 1)
        pop = None
        idx = 0
        while pop is None:
            if rand < POP_PROBS[1, idx]:
                pop = POP_PROBS[0, idx]
            else:
                idx += 1
        return pop
        
    def init_freq_commuter(self):
        FREQ_COMM_PROB = 0.8
        if np.random.uniform(0, 1) < FREQ_COMM_PROB:
            return True
        else:
            return False
              
    def init_hurry(self):
        """ Determines chance of driver being in a hurry
        
            Percentage calculated based on data from: https://aaafoundation.org/
            wp-content/uploads/2018/03/TSCI-2017-Report.pdf
            Data used (percentages based on a 30-day basis):
                * hurry is defined by driving 15mph over speed limit on freeway
                * 49.6% of drivers are never in a hurry 
                * 51.4% may be in a hurry
                * 18.8% are regularly/semi-regularly in a hurry
                * 31.6% are rarely or just once in a hurry
        """
        chances = np.random.uniform(size=2)
        # rule out drivers who wouldn't drive 15mph over speed limit
        if chances[0] < .514:
            may_speed = True
        else:
            may_speed = False
        
        # ignore habitual speeders
        if may_speed == True:
            if chances[1] < .316:
                return True
            else:
                return False
        else:
            return False
            
    def want_to_move_to_ETL(self, curr_toll, time, etl_speed, gpl_speed, \
                            score_weights=[8, 2, 3, 3, 6, 8]):
        """ Uses factors that influence a car's decision to use toll lanes and
            determines if they want to move to the ETL

            Parameters:
                curr_toll: current toll price of ETL
                time: what time it is
                etl_speed: how fast ETL are moving
                gpl_speed: how fast GPL are moving
                score_weights: how the scores are weighted. Default weight
                               determined from find_best_weights() in
                               Price_Elasticity_Model.py
        """
        # data used to determine influential factors and weights:
        # 1. https://www.wsdot.wa.gov/sites/default/files/2009/12/29/ 
        #    App5bTolling_Online_Survey_030510.pdf
        # 2. https://www.wsdot.wa.gov/Tolling/EastsideCorridor/
        #    EastsideCorridorTollingFAQ.htm#6
        # 3. https://www.wsdot.wa.gov/sites/default/files/2009/12/29/
        #    App5dFocusGroup_Tolling_Report.pdf
        #Algorithm Data:
        want_to_move = False
        #Income4
        inc_props = [.03, .02, .01, .008, .007, .006, .005]
        inc_move = [0.0, 0.15, 0.3, 0.45, 0.6, .75, .9, 1.0]
        inc = curr_toll / self.income * 100
        if inc > inc_props[0]:
            inc_score = inc_move[0]
        elif inc_props[0] > inc > inc_props[1]:
            inc_score = inc_move[1]
        elif inc_props[1] > inc > inc_props[2]:
            inc_score = inc_move[2]
        elif inc_props[2] > inc > inc_props[3]:
            inc_score = inc_move[3]
        elif inc_props[3] > inc > inc_props[4]:
            inc_score = inc_move[4]
        elif inc_props[4] > inc > inc_props[5]:
            inc_score = inc_move[5]
        elif inc_props[5] > inc > inc_props[6]:
            inc_score = inc_move[6]
        else:
            inc_score = inc_move[7]
        
        #Time of day
        # peak hours have greatest influence (5am-9am SB 3pm-7pm NB)
        if self.direction == 'South' and time > 5 and time < 9:
            time_score = 1.0
        elif self.direction == 'North' and time > 15 and time < 19:
            time_score = 1.0
        # lunch rush hours have second influence
        elif time > 11 and time < 1:
            time_score = 0.5
        else:
            time_score = 0.0
        #Frequent commuter
        # frequent commuters during peak have greatest chance
        if self.direction == 'South' and time > 5 and time < 9 and \
        self.freq_commuter == True:
            commuter_score = 1.0
        elif self.direction == 'North' and time > 15 and time < 19 and \
        self.freq_commuter == True:
            commuter_score = 1.0
        # frequent commuters in general have a slightly higher chance
        elif self.freq_commuter == True:
            commuter_score = .5
        # if not a commuter, random effect from 0.0-0.5
        else:
            rand = np.random.uniform(0.0, 0.5)
            commuter_score = rand
        #How many people they are travelling with
        # If they have #+ and a Good-To-Good pass, 100% chance to move to ETL
        if self.pop >= 3 and self.has_gtg == True:
            pop_score = 1.0
        else:
            pop_score = 0.0
        #If they have a good-to-go pass
        # Some percent more likely to merge depending on price because of the
        # $2 increase in toll without GTG pass
        if self.has_gtg == True:
            rand = np.random.uniform(0.5, 1.0)
            gtg_score = rand
        else:
            gtg_score = 0.0
        #Urgency 
        if self.in_a_hurry == True:
            rand = np.random.uniform(0.7, 1.0)
            hurry_score = rand
        else:
            hurry_score = 0.0
        # How much faster are ETL's than GPL's
        compare_speeds = [0, .15, .3, .45, .6, .75, .9, 1.0]
        speed_inc = (etl_speed / gpl_speed) - 1.0
        if speed_inc <= compare_speeds[0]:
            speed_score = compare_speeds[0]
        elif compare_speeds[0] < speed_inc <= compare_speeds[1]:
            speed_score = compare_speeds[1]
        elif compare_speeds[1] < speed_inc <= compare_speeds[2]:
            speed_score = compare_speeds[2]
        elif compare_speeds[2] < speed_inc <= compare_speeds[3]:
            speed_score = compare_speeds[3]
        elif compare_speeds[3] < speed_inc <= compare_speeds[4]:
            speed_score = compare_speeds[4]
        elif compare_speeds[4] < speed_inc <= compare_speeds[5]:
            speed_score = compare_speeds[5]
        elif compare_speeds[5] < speed_inc <= compare_speeds[6]:
            speed_score = compare_speeds[6]
        elif compare_speeds[6] < speed_inc <= compare_speeds[7]:
            speed_score = compare_speeds[7]
        else:
            speed_score = 1.0
        scores = np.array([inc_score, time_score, commuter_score, gtg_score, \
                  hurry_score, speed_score])
        # weights from 1-10
        score = np.sum(scores*score_weights)
        threshold = np.sum(score_weights)
        # if the score is at least 50% of the total score, car moves
        if score > (threshold / 2):
            want_to_move = True
        else:
            want_to_move = False
        return want_to_move
        
     def remove_old_loc(self, veh_locs_grid, ver, hor):
        veh_locs_grid[ver, hor] = 0
        veh_locs_grid[ver - 1, hor] = 0

    def add_new_loc(self, veh_locs_grid, ver, hor):
        veh_locs_grid[ver, hor] = 1
        veh_locs_grid[ver - 1, hor] = 1
    
    def can_shift_left(self, veh_locs_grid, lane_type_grid):
        # Check if general purpose lane to left
        if lane_type_grid[self.vertic, self.horiz - 1] != 0:
            return False
        if veh_locs_grid[self.vertic, self.horiz - 1] == 0 and \
                veh_locs_grid[self.vertic - 1, self.horiz - 1] == 0:
            return True
        else:
            return False
    
    def can_shift_right(self, veh_locs_grid, lane_type_grid):
        # Check if general purpose lane to right
        if lane_type_grid[self.vertic, self.horiz + 1] != 0:
            return False
        if veh_locs_grid[self.vertic, self.horiz + 1] == 0 and \
                veh_locs_grid[self.vertic - 1, self.horiz + 1] == 0:
            return True
        else:
            return False
    
    # Note: Do all cars take an exit located on the grid?
    def get_max_left(self, veh_locs_grid, grid_length):
        max_moves = 0
        idx = self.vertic + 1
        while idx < grid_length and veh_locs_grid[idx, self.horiz - 1] == 0:
            max_moves += 1
            idx += 1
        return max_moves
    
    def get_max_right(self, veh_locs_grid, grid_length):
        max_moves = 0
        idx = self.vertic + 1
        while idx < grid_length and veh_locs_grid[idx, self.horiz + 1] == 0:
            max_moves += 1
            idx += 1
        return max_moves
    
    def get_max_forward(self, veh_locs_grid, grid_length):
        max_moves = 0
        idx = self.vertic + 1
        while idx < grid_length and veh_locs_grid[idx, self.horiz] == 0:
            max_moves += 1
            idx += 1
        return max_moves
    
    def shift_left(self, veh_locs_grid):
        self.remove_old_loc(veh_locs_grid, self.vertic, self.horiz)
        self.horiz -= 1
        self.add_new_loc(veh_locs_grid, self.vertic, self.horiz)
        
    
    def shift_right(self, veh_locs_grid):
        self.remove_old_loc(veh_locs_grid, self.vertic, self.horiz)
        self.horiz += 1
        self.add_new_loc(veh_locs_grid, self.vertic, self.horiz)
    
    def move_forward(self, space_avail, veh_locs_grid):
        moves = space_avail if space_avail < self.max_forward_moves else \
                self.max_forward_moves
        temp_vertic = self.vertic
        self.vertic += moves
        self.remove_old_loc(veh_locs_grid, temp_vertic, self.horiz)
        self.add_new_loc(veh_locs_grid, self.vertic, self.horiz)
        
    def move_on_gpl(self, veh_locs_grid, lane_type_grid):
        max_left = 0
        max_right = 0
        max_forward = 0
        grid_length = N.size(veh_locs_grid[:, 0])
        if self.can_shift_left(veh_locs_grid, lane_type_grid):
            max_left = self.get_max_left(veh_locs_grid, grid_length)
        if self.can_shift_right(veh_locs_grid, lane_type_grid):
            max_right = self.get_max_right(veh_locs_grid, grid_length)
        max_forward = self.get_max_forward(veh_locs_grid, grid_length)
        if max_forward >= max_right and max_forward >= max_left:
            self.move_forward(max_forward, veh_locs_grid)
        elif max_right >= max_left:
            self.shift_right(veh_locs_grid)
            self.move_forward(max_right, veh_locs_grid)
        else:
            self.shift_left(veh_locs_grid)
            self.move_forward(max_left, veh_locs_grid)
    
    def move_on_etl(self, veh_locs_grid):
        grid_length = N.size(veh_locs_grid[:, 0])
        max_forward = self.get_max_forward(veh_locs_grid, grid_length)
        self.move_forward(max_forward, veh_locs_grid)
    
    def remove_car(self):
        print("Car removed")
        #exit_dict = self.highway.string_to_int
        #exit_idx = exit_dict[self.off_ramp]
        #exit_ramp = self.highway.exits_arr[exit_idx]
        #exit_ramp.intake(self)
    
    def go_to_exit(self, veh_locs_grid, lane_type_grid):
        while self.can_shift_right(veh_locs_grid, lane_type_grid):
            self.shift_right(veh_locs_grid)
        space_until_exit = self.exit_coord[0] - self.vertic
        grid_length = N.size(veh_locs_grid[:, 0])
        max_forward = self.get_max_forward(veh_locs_grid, grid_length)
        min_move = space_until_exit if space_until_exit < max_forward else \
                max_forward
                
    self.move_forward(min_move, veh_locs_grid)
        if self.vertic == self.exit_coord[0] and \
                self.horiz == self.exit_coord[1]:
            self.remove_car()
    
    def move_to_etl(self, veh_locs_grid, lane_type_grid):
        while self.can_shift_left(veh_locs_grid, lane_type_grid):
            self.shift_left(veh_locs_grid)
        space_until_entrance = self.etl_entry_coord[0] - self.vertic
        grid_length = N.size(veh_locs_grid[:, 0])
        max_forward = self.get_max_forward(veh_locs_grid, grid_length)
        min_move = space_until_entrance if space_until_entrance < max_forward \
                else max_forward
        self.move_forward(min_move, veh_locs_grid)
        if self.vertic == self.etl_entry_coord[0]:
            self.shift_left(veh_locs_grid)
            self.on_etl = True
            self.going_to_etl = False
        
    def is_near_exit(self):
        if self.exit_coord[0] - self.vertic <= self.near_exit_length:
            return True
        return False
    
    def update_nearest_etl(self):
        entry_arr = self.highway.etl_entry_arr
        for i in range(len(entry_arr)):
            if self.vertic <= entry_arr[i][0]:
                self.etl_entry_coord[0] = entry_arr[i][0]
                self.etl_entry_coord[1] = entry_arr[i][1]
    
    def is_near_etl(self):
        self.update_nearest_etl()
        if self.etl_entry_coord[0] - self.vertic <= self.near_etl_length:
            return True
        return False
    
    def move(self, highway_grid):
        veh_locs_grid = highway_grid[:,:,0]
        lane_type_grid = highway_grid[:,:,1]
        if self.is_near_etl() and self.want_to_move_to_ETL():
            self.move_to_etl(veh_locs_grid, lane_type_grid)
        else:
            if self.is_near_exit():
                self.go_to_exit(veh_locs_grid, lane_type_grid)
            else:
                if self.on_etl:
                    self.move_on_etl(veh_locs_grid)
                else:
                    self.move_on_gpl(veh_locs_grid, lane_type_grid)
            
            
            
        #if self.going_to_etl:
         #   if self.is_near_etl():
          #      self.move_to_etl(veh_locs_grid, lane_type_grid)
           # else:
            #    self.move_on_gpl(veh_locs_grid, lane_type_grid)     
        #else:
         #   if self.is_near_exit():
          #      self.go_to_exit(veh_locs_grid, lane_type_grid)
           # else:
            #    if self.on_etl:
             #       self.move_on_etl(veh_locs_grid)
              #  else:
               #     self.move_on_gpl(veh_locs_grid, lane_type_grid)

    
