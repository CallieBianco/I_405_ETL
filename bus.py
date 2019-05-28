# -*- coding: utf-8 -*-
"""
Created on Wed May 22 10:08:18 2019

@author: awsir
"""

import numpy as np

class Bus:
    def __init__(self, x, y, gpm):
        self.length = 3
        self.route = np.zeros(3)
        self.near_exit = False
        self.in_etl = False
        self.coord_y = y
        self.coord_x = x
        self.grids_per_mile = gpm
        self.near_exit_condition = 0.5 * gpm #half mile
        self.range_checker = np.zeros((1, 3), dtype='f')
        
    def move(self, arr):
        """
        Pass in the whole highway
        """
        
        total_moved = 0
        if self.near_exit == False:
            self.near_exit = self._near_exit(arr)
        #NOTE : arr[] is the length, arr[][] is the width
        if self.near_exit == True:
            if arr[self.coord_y-1:self.coord_y+2, self.coord_x - 1, 0] == self.range_checker and arr[self.coord_y, self.coord_x - 1, 1] != 2:
                squares_moved, arr = self._shift_left(arr)
                total_moved += squares_moved
            squares_moved, arr = self._move_forward(arr) 
            total_moved += squares_moved
        elif arr[self.coord_y:self.coord_y + 3, self.coord_x, 0] == self.range_checker:
            squares_moved, arr = self._move_forward(arr)
            total_moved += squares_moved
        elif arr[self.coord_y-1:self.coord_y+2, self.coord_x + 1, 0] == self.range_checker and arr[self.coord_y, self.coord_x + 1, 1] != 2:
            squares_moved, arr = self._shift_right(arr)
            total_moved += squares_moved
            squares_moved, arr = self._move_forward(arr)
            total_moved += squares_moved
        elif arr[self.coord_y-1:self.coord_y+2, self.coord_x - 1, 0] == self.range_checker and arr[self.coord_y, self.coord_x - 1, 1] != 2:
            squares_moved, arr = self._shift_left(arr)
            total_moved += squares_moved
            squares_moved, arr = self._move_forward(arr)  
            total_moved += squares_moved
        
        return total_moved, arr
            
    def _move_forward(self, arr):
        squares_moved = 0
        while arr[self.coord_y:self.coord_y + 3, self.coord_x, 0] == self.range_checker:
            arr[self.coord_y - 1, self.coord_x, 0] == False
            arr[self.coord_y + 2, self.coord_x, 0] == True
            squares_moved += 1
            self.coord_y += 1
        
        return squares_moved, arr
        
    def _shift_left(self, arr):
        for i in range(3): 
            arr[self.coord_y - 1 + i, self.coord_x, 0] == False
            arr[self.coord_y - 1 + i, self.coord_x - 1, 0] == True
        self.coord_x -= 1
        
    def _shift_right(self, arr):
        for i in range(3): 
            arr[self.coord_y - 1 + i, self.coord_x, 0] == False
            arr[self.coord_y - 1 + i, self.coord_x + 1, 0] == True
        self.coord_x += 1
        
    def _near_exit(self, arr):
        for i in range(len(arr.exits_arr)):
            if self.y >= arr.exits_arr[i].y:
                continue
            elif self.y >= arr.exits_arr[i].y - self.near_exit_condition:
                return True
            
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                