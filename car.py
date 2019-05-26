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
        self.inc_data = inc.Income_Data()
        #self.on_ramp = self.init_on_ramp()
        #self.off_ramp = self.init_off_ramp()
        #self.has_gtg = self.init_has_gtg()
        #self.pop = self.init_pop()
        #self.can_shift_left = self.shift_left()
        #self.can_move_forward = False
        #self.can_shift_right = self.shift_right()
        self.income = self.init_income()
        #self.length = 1
        #self.freq_commuter = self.init_frequent()
        #self.in_a_hurry = self.init_hurry()
        #self.crashed = False
        #self.horiz = 0
        #self.vertic = 0
        #self.speed = 0 # mph
        self.direction = direction
        
    def init_income(self):
        """ Initializes income of a car based on city-data.

            Assumes income of car is the driver's income.
        """ 
        income_class = self._class_breakdown() 
        city = self._city_data(income_class)
        
        if city == 'Everett':
            return self.inc_data.ev_inc(income_class)
        elif city == 'Lynnwood':
            return self.inc_data.lynn_inc(income_class) 
        elif city == 'Mountlake Terrace':
            return self.inc_data.mlt_inc(income_class)
        elif city == 'Bothell':
            return self.inc_data.bot_inc(income_class)
        elif city == 'Bellevue':
            return self.inc_data.bell_inc(income_class)
        elif city == 'Redmond':
            return self.inc_data.red_inc(income_class)
        elif city == 'Kirkland':
            return self.inc_data.kirk_inc(income_class)
      
    def _class_breakdown(self):
        low, mid_low, mid, mid_upper, upper = 0.0, 0.0, 0.0, 0.0, 0.0
        classes = ['low', 'mid low', 'mid', 'mid upper', 'upper']
        breakdown = [low, mid_low, mid, mid_upper, upper]
        for i in range(len(classes)):
            breakdown[i] = self.inc_data.income_breakdown[classes[i]] / 100.0
        l = breakdown[0]
        lm = l + breakdown[1]
        m = lm + breakdown[2]
        mu = m + breakdown[3]
        u = mu + breakdown[4] 
        
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

    def _city_data(self, inc_class):             
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



# random testing

#cars = np.empty(10, dtype=Car)

#for i in range(len(cars)):

#    cars[i] = Car()

#    print(cars[i].income)
