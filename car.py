# -*- coding: utf-8 -*-
"""
Created on Wed May 22 10:08:13 2019

@author: awsir
@author: CallieBianco
"""
class Car(object):
    """ Defines a car object.
    
        Data fields:
            on_ramp:          Mile marker from which car enters I-405, 
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
    
    def __init__(self, on_ramp, off_ramp, has_gtg, pop, horiz, vertic):
        self.on_ramp = on_ramp
        self.off_ramp = off_ramp
        self.has_gtg = has_gtg
        self.pop = pop
        self.can_shift_left = self.shift_left()
        self.can_move_forward = False
        self.can_shift_right = self.shift_right()
        self.income = self.init_income()
        self.length = 1
        self.freq_commuter = self.init_frequent()
        self.in_a_hurry = self.init_hurry()
        self.crashed = False
        self.horiz = horiz
        self.vertic = vertic
        self.speed = 0 # mph
        
    def init_income(self):
        """ Initializes income of a car based on city-data.
            
            Assumes income of car is the driver's income.
        """
        # function plan:
        # find list of on-ramps
        # associate them with a city
        # find city income
        # find percentage of lower, middle, and upper-class
        # set income based on if they are lower, middle, or upper-class
        # temporary return: 50000
        return 50000
        
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
            
    
