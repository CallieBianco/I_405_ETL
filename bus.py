# -*- coding: utf-8 -*-
"""
Created on Wed May 22 10:08:18 2019

@author: awsir
"""

import numpy as np

class Bus:
    def __init__(self, x, y):
        self.length = 3
        self.route = np.zeros(3)
        self.near_exit = False
        self.in_etl = False
        self.coord_y = y
        self.coord_x = x
        
    def move(self, arr):
        if self.near_exit:
            if arr[2, 2:5, 1] == False:
                self.shift_right(arr[1:, 1:5])
            self._move_forward(arr[2, 1:5])
        elif not self.in_etl:
            self._shift_left(arr[0:2, 1:5, 0])
        elif arr[1, 0:2, 0] == False:
            self._move_forward(arr[1, 1:5])
        elif arr[0, 0:6, 0] == False and arr[0, 0:6, 1] == False:
            self.shift_left(arr[0:2, 1:5])
            self._move_forward(arr[0, 1:5])
        elif arr[2, 0:6, 0] == False and arr[0, 0:6, 1] == False:
            self.shift_right(arr[1:, 1:5])
            self._move_forward(arr[2, 1:5])
            
    def _move_forward(self, arr):
        arr[0, 0, 0] = True
        arr[0, -1, 0] = False
        self.coord_y += 1
        
    def _shift_left(self, arr):
        arr[1, 0:4, 0] = False
        arr[0, 0:4, 0] = True
        self.coord_x -= 1
        
    def _shift_right(self, arr):
        arr[0, 0:4, 0] = False
        arr[1, 0:4, 0] = True
        self.coord_x += 1