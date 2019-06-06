#=======================================================================
#                        General Documentation
#
    # Exit Object for I-405 Simulation
#
#-----------------------Additional Documentation------------------------

# Modification History:
# - 19 May 2019: exit.py created by Adam Sirkis
# - 04 June 2019: exit.py finalized by Adam Sirkis

# Notes:
# - Developed for Python 3.x

#=======================================================================
class Exit:
    def __init__(self, number, grids_per_mile, y, max_capacity=10):    
        """ COnstructor for Exit
        
        Method Arguments:
            - Number : a number representing the exit number relative to the entrance
            - grids_per_mile : the number fo grid squares per distance of the highway
            - y : number representing the coordinate lengthwise fo the exit
            - max_capacity  numbebr of vehicles it can hold
            
           """
        self.max = max_capacity
        self.count = 0
        self.number_dispensed = 0
        self.dispense_num = 50
        self.id = number
        self.y = y
        
    def intake(self, veh):
        """
        Take in vehicles
        
        Method arguments: 
            - veh : the vehicle to take in
        
        Return Values:
            - Bool representing if the inatek was successful
            """
        if self.count < self.max:
            self.count += 1
            return True
        else:
            return False
    
    def deplete(self):
        """
        Push out vehicles
        
        Method arguments: 
            - none
        
        Return Values:
            - none
            """
        if self.count >= self.dispense_num:
            self.count -= self.dispense_num
            self.number_dispensed += self.dispense_num
        else:
            self.number_dispensed += self.count
            self.count = 0
