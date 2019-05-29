<<<<<<< HEAD
# -*- coding: utf-8 -*-
"""
Created on Wed May 22 10:09:08 2019

@author: Tung Dinh
"""

import highway
import car
import numpy as np
# Simulate traffic on I405 North & South between Bothell and Lynnwood
class SimulationDriver:
    def __init__(self):
        self.highWay = None
        self.minPrice = 0.75
        self.maxPrice = 10.00
        self.start_shoulder = 15
        self.end_shoulder = 17
        self.start_tolling = 5
        self.end_tolling = 19
        self.gpl = 2
        self.etl = 1
        self.south_length = 8
        self.north_length = 8
        self.exits_north = [1, 3, 7]  # Exit 24, 26, I5 to Lynnwood
        self.exits_south = [3, 7]     # Exit 26, and 24 to Bothell
        # 0: no traffic, 0.5: low traffic, 1: medium traffic, 2: high traffic in 24 hrs
        self.peakHrs_north = [0, 0, 0, 0, 0, 0.5, 2, 2, 1,
                              0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 1, 2, 2, 1, 0.5, 0.5, 0.5, 0, 0]
        self.peakHrs_south = [0, 0, 0, 0, 0, 0.5, 2, 2, 1,
                              0.5, 0.5, 0.5, 0.5, 0.5, 1, 1, 2, 2, 1, 1, 0.5, 0.5, 0, 0]
        self.shoulder_north = []
        self.shoulder_south = []
        self.highWayGrid = self.initHighWay(self.highWay)
        # Number of car on I405 North
        self.carsOnNorth = self.initCars(direction='North') 
        # Number of car on I405 South
        self.carsOnSouth = self.initCars(direction='South') 
        self.carMaxAt_0 = 20
        self.carMaxAt_half = 80
        self.carMaxAt_1 = 120
        self.carMaxAt_2 = 240
    def initHighWay(self, highWay):
        highWay = []
        # Generate I405 South Highway
        highWay.append(highway.Highway(self.south_length, self.gpl, self.etl, 
                                            self.peakHrs_south, self.shoulder_south, self.minPrice,
                                            self.maxPrice, self.exits_south, self.start_shoulder,
                                            self.end_shoulder, self.end_tolling, self.end_tolling))
        # Generate I405 North Highway
        highWay.append(highway.Highway(self.north_length, self.gpl, self.etl,
                                            self.peakHrs_north, self.shoulder_north, self.minPrice,
                                            self.maxPrice, self.exits_north, self.start_shoulder,
                                            self.end_shoulder, self.end_tolling, self.end_tolling))
        # Generate exits on I405 South
        highWay[0]._generate_road(self.exits_south)
        # Generate exits on I405 North
        highWay[1]._generate_road(self.exits_south)
        return highWay
    def initCars(self, direction):
        cars = []
        # Generate number of cars in a specific time frame depending on peak hours
        if (direction == 'North'):
            for i in range(len(self.peakHrs_north)):
                if (self.peakHrs_north[i] == 0):
                    rand = np.random.randint(0, self.carMaxAt_0)
                    cars.append([])
                    for j in range(rand):
                        cars[i].append(car.Car(direction))
                elif (self.peakHrs_north[i] == 0.5):
                    rand = np.random.randint(
                        self.carMaxAt_0, self.carMaxAt_half)
                    cars.append([])
                    for j in range(rand):
                        cars[i].append(car.Car(direction))
                elif (self.peakHrs_north[i] == 1):
                    rand = np.random.randint(
                        self.carMaxAt_half, self.carMaxAt_1)
                    cars.append([])
                    for j in range(rand):
                        cars[i].append(car.Car(direction))
                else:
                    rand = np.random.randint(
                        self.carMaxAt_1, self.carMaxAt_2)
                    cars.append([])
                    for j in range(rand):
                        cars[i].append(car.Car(direction))
        elif (direction == 'South'):
            for i in range(len(self.peakHrs_south)):
                if (self.peakHrs_north[i] == 0):
                    rand = np.random.randint(0, self.carMaxAt_0)
                    cars.append([])
                    for j in range(rand):
                        cars[i].append(car.Car(direction))
                elif (self.peakHrs_north[i] == 0.5):
                    rand = np.random.randint(
                        self.carMaxAt_0, self.carMaxAt_half)
                    cars.append([])
                    for j in range(rand):
                        cars[i].append(car.Car(direction))
                elif (self.peakHrs_north[i] == 1):
                    rand = np.random.randint(
                        self.carMaxAt_half, self.carMaxAt_1)
                    cars.append([])
                    for j in range(rand):
                        cars[i].append(car.Car(direction))
                else:
                    rand = np.random.randint(
                        self.carMaxAt_1, self.carMaxAt_2)
                    cars.append([])
                    for j in range(rand):
                        cars[i].append(car.Car(direction))
        return cars

=======
# -*- coding: utf-8 -*-
"""
Created on Wed May 22 10:09:08 2019

@author: awsir
"""

>>>>>>> 41a67cf653dcfd4ea7133c9703a03af420e8034a
