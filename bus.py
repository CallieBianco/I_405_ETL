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
import numpy as np

class Bus:
    def __init__(self, x, y, gpm):
        """ Constructor for a Bus object
        
        Method Arguments:
            - x : int-like representing location on the highway
            - y : int-like representing location on the highway
            - gpm : int-like representing the maximum number of squares a vehicle can move
            
            
        Member vaiables:
            - near_exit : bool representing if the object is clsoe to an exit object
            - in_etl : bool repesenting which type of lane the us is in
            - y : int representing vertical distance along the grid
            - x : int representing horizontal lane position
            - max : aximum number of squares for each move
            - near_exit_condition : condition for being said to be near an exit
            - exit : an exit object that the bus needs to be near to exit
        """
        self.near_exit = False
        self.in_etl = False
        self.y = int(y)
        self.x = int(x)
        self.near_exit_condition = 0.5 * gpm #half mile
        self.max = gpm
        self.exit = None
        
    def move(self, arr, timestep):
        """
        MOve behavior for the Bus object
        
        Method Arguments:
            - arr : a Highway for the object to move on and update
            - timestep : the time interval used
            
        Returns:
            An int indicating the number of squaes moved, 
            the updated highway, and 
            a bool about whether or not the bus exited
        """
        self.exit = self._gen_exit(arr)
        exited = False
        total_moved = 0
        if self.near_exit == False:
            self.near_exit = self._near_exit(arr.grid_per_mile)
        #NOTE : arr[] is the length, arr[][] is the width
        if self.near_exit == True:
            if arr.grid[self.y-1, self.x - 1, 0] == 0 and \
            arr.grid[self.y, self.x - 1, 1] != 2 and \
            arr.grid[self.y, self.x - 1, 0] == 0 and \
            arr.grid[self.y+1, self.x - 1, 0] == 0:
                squares_moved, arr = self._shift_left(arr)
                total_moved += squares_moved
            squares_moved, arr, exited = self._move_forward(arr) 
            total_moved += squares_moved
            
        elif arr.grid[self.y+1, self.x, 0] ==  0 and \
        arr.grid[self.y + 2, self.x, 0] ==  0:
            squares_moved, arr, exited = self._move_forward(arr)
            total_moved += squares_moved
        elif arr.grid[self.y-1, self.x + 1, 0] == 0 and \
        arr.grid[self.y, self.x + 1, 1] != 2 and \
        arr.grid[self.y, self.x + 1, 0] == 0 and \
        arr.grid[self.y+1, self.x + 1, 0] == 0:
            squares_moved, arr, exited  = self._shift_right(arr)
            total_moved += squares_moved
            squares_moved, arr, exited  = self._move_forward(arr)
            total_moved += squares_moved
        elif arr.grid[self.y-1, self.x - 1, 0] == 0 \
        and arr.grid[self.y, self.x - 1, 1] != 2 and \
        arr.grid[self.y, self.x - 1, 0] == 0 and \
        arr.grid[self.y+1, self.x - 1, 0] == 0:
            squares_moved, arr, exited  = self._shift_left(arr)
            total_moved += squares_moved
            squares_moved, arr, exited  = self._move_forward(arr)  
            total_moved += squares_moved
        if self.y + arr.grid_per_mile >= arr.length * arr.grid_per_mile:
            exited = True
        if exited == True:
            arr.grid[self.y - 1, self.x, 0] = False
            arr.grid[self.y, self.x, 0] = False
            arr.grid[self.y + 1, self.x, 0] = False    
            arr.grid[self.y + 2, self.x, 0] = False 
            arr.grid[self.y - 2, self.x, 0] = False 
        if arr.grid[self.y, self.x, 1] == 1:
            self.in_etl = True
        else:
            self.in_etl = False
        return total_moved, arr, exited
            
    def _move_forward(self, arr):
        """
        Move the vehicle forward
        
        Method Arguments:
            - arr : highway for the object to move on
            
        Returns:
            An int indicating the number of squaes moved, 
            the updated highway, and 
            a bool about whether or not the bus exited
            
        """
        squares_moved = 0
        while arr.grid[self.y+1, self.x, 0] == 0 and \
        arr.grid[self.y + 2, self.x, 0] == 0 and \
        arr.grid[self.y + 3, self.x, 0] == 0 and \
        squares_moved < self.max:
            if self.y >= self.exit.y:
                return squares_moved, arr, True
            if self.y + arr.grid_per_mile >= arr.length * arr.grid_per_mile:
                return squares_moved, arr, True
            arr.grid[self.y - 1, self.x, 0] = False
            arr.grid[self.y + 2, self.x, 0] = True
            squares_moved += 1
            self.y += 1
        
        return squares_moved, arr, False
        
    def _shift_left(self, arr):
        """
        Move the vehicle left
        
        Method Arguments:
            - arr : highway for the object to move on
            
        Returns:
            An int indicating the number of squaes moved, 
            the updated highway, and 
            a bool about whether or not the bus exited
            
        """
        for i in range(3): 
            arr.grid[self.y - 1 + i, self.x, 0] = False
            arr.grid[self.y - 1 + i, self.x - 1, 0] = True
        self.x -= 1
        
        return 1, arr
        
    def _shift_right(self, arr):
        """
        Move the vehicle right
        
        Method Arguments:
            - arr : highway for the object to move on
            
        Returns:
            An int indicating the number of squaes moved, 
            the updated highway, and 
            a bool about whether or not the bus exited
            
        """
        for i in range(3): 
            arr.grid[self.y - 1 + i, self.x, 0] = False
            arr.grid[self.y - 1 + i, self.x + 1, 0] = True
        self.x += 1
        
        return 1, arr
        
    def _near_exit(self, gpm):
        """
        Determine if the bus is near an exit
            
        Method arguments:
            - gpm : int regarding the maximum amount the bbus can move
            
        Reutrns:
            - bool
        """
        return self.y >= self.exit.y - (0.1 * gpm)
            
    def _gen_exit(self, arr):
        """
        Find the next exit to go to
        
        Method arguments:
            - arr : Highway to determine the next exit from
            
        Returns:
            - Exit object
        """
        for i in range(len(arr.exits_arr)):
            if self.y < arr.exits_arr[i].y:
                return arr.exits_arr[i]
            return arr.exits_arr[-1]
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                