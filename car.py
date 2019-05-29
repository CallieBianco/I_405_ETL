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
            on_ramp:          Mile marker from which car enters I-405, 
                              associated with a city
            off_ramp:         Exit number that which car leaves I-405.
            has_gtg:          Whether or not a car has a Good-to-Go! account
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
    def __init__(self, direction):
        self.direction = direction
        self.inc_data = inc.Income_Data()
        self.on_ramp = self.init_on_ramp()
        self.off_ramp = self.init_off_ramp()
        self.income_class = self._class_breakdown() 
        self.city = self._city_data()
        #self.has_gtg = self.init_has_gtg()
        #self.pop = self.init_pop()
        #self.can_shift_left = self.shift_left()
        #self.can_move_forward = False
        #self.can_shift_right = self.shift_right()
        self.income = self.init_income()
        #self.length = 1
        #self.freq_commuter = self.init_frequent()
        self.in_a_hurry = self.init_hurry()
        #self.crashed = False
        #self.horiz = 0
        #self.vertic = 0
        #self.speed = 0 # mph
    
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
      
    def init_frequent(self):
        """ Initializes whether or not a car is a frequent commuter based on
            commuter data.
        """
        # function plan:
        # determine the percentage of frequent commuters on I-405
        # generate a random number
        # if random number < percentage of freq commuters: False
        # else: True
        # temporary return: True
        return True
      
    def shift_left(self, location):
        """ Checks spot horizontally left of car's current location
        
            If spot is open (True), self.can_shift_left = True

        """
        if self.horiz - 1 == True:
            return True
        else:
            return False
          
    def shift_right(self, location):
        """ Checks spot horizontally right of car's current location
        
            If spot is open (True), self.can_shift_right= True
        """
        if self.horiz + 1 == True:
            return True
        else:
            return False
          
    def enter(self):
        # assuming that entry point is at (0,0)
        self.speed = 60
        self.horiz = 0
        self.vertic = 0
        
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
