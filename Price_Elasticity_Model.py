# -*- coding: utf-8 -*-
"""
Created on Tue Jun  4 14:05:49 2019

@author: awsir
"""

from car import Car

import numpy as np

import matplotlib.pyplot as plt



def price_elasticity_weights(props):

    """ Determines if the set of weights is valid

    """

    # determine most appropriate weights

    # On average between Lynnwood and Bothell both ways, 

    # data: https://www.wsdot.wa.gov/sites/default/files/2018/12/27/

    #       Toll-405-ETL-36-Month-Report.pdf

    # Proportion of cars expected to drive in ETL's: expected_proportion_use()

    expected = expected_proportion_use()

    

    # use average tolls to test: $5 during peak and $1.25 in non-peak

    PEAK = 5

    NON = 1.25

    NUM_CARS_NON_PEAK = 100

    NUM_CARS_PEAK = 200

    # simulate only tolling hours: 5am-7pm

    START = 5

    END = 19

    # peak avg speeds southbound (same proportion was northbound too)

    PEAK_ETL_SPEED = 39

    PEAK_GPL_SPEED = 25

    NON_ETL_SPEED = 60

    NON_GPL_SPEED = 55

    S_PEAK = np.arange(START, 10)

    N_PEAK = np.arange(15, END+1)

    S_NON = np.arange(10, END)

    N_NON = np.arange(START, 16)

    TOTAL_CARS = (NUM_CARS_PEAK*(len(S_PEAK))) + (NUM_CARS_NON_PEAK* \

                  (len(S_NON)))

    diff = 0

    for n in range(10):

        count = 0

        for i in range(len(S_PEAK)):

            for j in range(NUM_CARS_PEAK):

                sc = Car(direction='South')

                if sc.want_to_move_to_ETL(PEAK, S_PEAK[i], PEAK_ETL_SPEED, \

                                        PEAK_GPL_SPEED, props) == True:

                    count += 1
                speeds_change()

        for i in range(len(S_NON)):

            for j in range(NUM_CARS_NON_PEAK):

                sc = Car(direction='South')

                if sc.want_to_move_to_ETL(NON, S_NON[i], NON_ETL_SPEED, \

                                        NON_GPL_SPEED, props) == True:

                    count += 1
                speeds_change()
                
        for i in range(len(N_PEAK)):

            for j in range(NUM_CARS_PEAK):

                sc = Car(direction='North')

                if sc.want_to_move_to_ETL(PEAK, N_PEAK[i], PEAK_ETL_SPEED, \

                                        PEAK_GPL_SPEED, props) == True:

                    count += 1
                speeds_change()
        for i in range(len(N_NON)):

            for j in range(NUM_CARS_NON_PEAK):

                sc = Car(direction='North')

                if sc.want_to_move_to_ETL(NON, N_NON[i], NON_ETL_SPEED, \

                                        NON_GPL_SPEED, props) == True:

                    count += 1
                speeds_change()
        total = count / (TOTAL_CARS*2)

        diff += abs(expected - total)

    return diff / 10

    

        

def expected_proportion_use():

    """ Returns the expected proportion of cars that use the ETLs

    """

    # http://www.wsdot.wa.gov/sites/default/files/2019/05/13/

    # Toll-405ETL-Monthly-Volumes-Oct2014-Dec2018.pdf

    # using 2018 monthly data

    # using SR 522 and SR 527 totals for Bothell-Lynnwood estimation

    south_totals = np.array([55786, 57345, 59883, 59895, 60329, 62532, 61587, \

                    62702, 59820, 58926, 57742, 58144])

    south_etl = np.array([13881, 13994, 15044, 14767, 15604, 16564, 16560, \

                 16899, 15284, 14908, 14697, 15238])

    north_totals = np.array([53551, 55387, 57525, 57885, 58269, 60742, 59442, \

                    60388, 57753, 57527, 56007, 54317])

    north_etl = np.array([11066, 11149, 11775, 11818, 12041, 12794, 12509, \

                 12881, 12166, 12163, 11571, 11242])

                 

    south_proportion = (np.sum(south_etl)) / (np.sum(south_totals))

    north_proportion = (np.sum(north_etl)) / (np.sum(north_totals))

    return (south_proportion + north_proportion) / 2   



def find_best_weight():

    """ Determines the best score weights by finding the set of weights

        that make the proportion of ETL cars to GPL cars as close to 

        expected as possible.

        

        Note: Once I run it and find the best set of weights, I will take note 

              of it as the set to use; I don't want to run this function every

              time I run the want_to_move_to_ETL() function for time sake.

    """

    # order:

    # inc_score, time_score, commuter_score, gtg_score, hurry_score, speed_score

    # Weight distribution rules:

    # all values 1-10

    # inc_score is always at least the highest (can be tied)

    # hurry_score and speed_score are the next highest (can be flipped or tied)

    # gtg_score

    # time_score, commuter_score, and gtg_score will be at least 2 lower than inc

    ins = np.random.randint(7, 10, 100)

    ts = np.random.randint(2, 5, 100)

    cs = np.random.randint(2, 5, 100) 

    gs = np.random.randint(2, 5, 100)

    hs = np.random.randint(5, 10, 100)

    ss = np.random.randint(5, 10, 100)

    weights = np.zeros(len(ins))

    # test different weighted combinations adhering to weight distribution rules

    for i in range(len(ins)):

        weight = np.array([ins[i], ts[i], cs[i], gs[i], hs[i], ss[i]])

        diff = price_elasticity_weights(weight)

        # find difference in actual value vs. expected

        weights[i] = diff

    # return index where the difference is the smallest

    min_i = np.argmin(weights)

    # make sure income score is the highest (most important) weight

    if ins[min_i] < ss[min_i]:

        temp = ss[min_i]

        ss[min_i] = ins[min_i]

        ins[min_i] = temp

    return [ins[min_i], ts[min_i], cs[min_i], gs[min_i], hs[min_i], ss[min_i]]



#best_weight = find_best_weight()

#best_weight = [8, 2, 3, 3, 6, 8]

#expected - actual = .0055789



def speed_sensitivity():

    """ Analyzes how proportion of cars in ETLs vs GPL changes as speed 

        differences in the lanes change.



    """ 

    # use average tolls to test: $5 during peak and $1.25 in non-peak

    PEAK = 5

    NON = 1.25

    NUM_CARS_NON_PEAK = 100

    NUM_CARS_PEAK = 200

    # simulate tolling hours (non-tolling hours, ETLs act as regular lanes)

    START = 5

    END = 19

    # change speeds (as speeds in ETL get faster, number of cars wanting to move

    #                should increase)

    PEAK_ETL_SPEED = np.arange(30, 61)

    # will stay constant

    PEAK_GPL_SPEED = 30

    # keep at average

    NON_ETL_SPEED = 60

    NON_GPL_SPEED = 55

    S_PEAK = np.arange(START, 10)

    N_PEAK = np.arange(15, END+1)

    S_NON = np.arange(10, END)

    N_NON = np.arange(START, 15)

    TOTAL_CARS = (NUM_CARS_PEAK*(len(S_PEAK))) + (NUM_CARS_NON_PEAK* \

                  (len(S_NON)))

    changes_s = np.zeros(len(PEAK_ETL_SPEED))

    changes_n = np.zeros(len(PEAK_ETL_SPEED))

    SIM = 100

    """

    for k in range(SIM):

        for n in range(len(PEAK_ETL_SPEED)):

            count = 0

            for i in range(len(S_PEAK)):

                for j in range(NUM_CARS_PEAK):

                    sc = Car(direction='South')

                    if sc.want_to_move_to_ETL(PEAK, S_PEAK[i], PEAK_ETL_SPEED[n], \

                                            PEAK_GPL_SPEED) == True:

                        count += 1

            for i in range(len(S_NON)):

                for j in range(NUM_CARS_NON_PEAK):

                    sc = Car(direction='South')

                    if sc.want_to_move_to_ETL(NON, S_NON[i], NON_ETL_SPEED, \

                                              NON_GPL_SPEED) == True:

                        count += 1

            changes_s[n] += count / TOTAL_CARS

    changes_s /= SIM

    """

    for k in range(SIM):

        for n in range(len(PEAK_ETL_SPEED)):

            count = 0

            for i in range(len(N_PEAK)):

                for j in range(NUM_CARS_PEAK):

                    nc = Car(direction='North')

                    if nc.want_to_move_to_ETL(PEAK, N_PEAK[i], PEAK_ETL_SPEED[n], \

                                              PEAK_GPL_SPEED) == True:

                        count += 1

            for i in range(len(N_NON)):

                for j in range(NUM_CARS_NON_PEAK):

                    nc = Car(direction='North')

                    if nc.want_to_move_to_ETL(NON, N_NON[i], NON_ETL_SPEED, \

                                              NON_GPL_SPEED) == True:

                        count += 1

            changes_n[n] += count / TOTAL_CARS

    changes_n /= SIM

    

    plt.plot(PEAK_ETL_SPEED - 30, changes_n)

    plt.title("Northbound: Proportion of Total Cars in ETLs as \n \

              Speed Difference Increases")

    plt.xlabel("MPH Faster than GPL")

    plt.ylabel("Proportion of Cars in ETL")

    plt.show()   

    

def price_sensitivity():

    """ Analyzes how proportion of cars in ETLs vs GPL changes as toll price

        changes.

        

    """ 

    # Change peak prices

    PEAK = np.arange(.75, 10, .25)

    # keep at average

    NON = 1.25

    NUM_CARS_NON_PEAK = 100

    NUM_CARS_PEAK = 200

    # simulate tolling hours (non-tolling hours, ETLs act as regular lanes)

    START = 5

    END = 19

    # Use average speeds (northbound is same proportion as southbound)

    PEAK_ETL_SPEED = 39

    PEAK_GPL_SPEED = 25

    NON_ETL_SPEED = 60

    NON_GPL_SPEED = 55

    S_PEAK = np.arange(START, 10)

    N_PEAK = np.arange(15, END+1)

    S_NON = np.arange(10, END)

    N_NON = np.arange(START, 15)

    TOTAL_CARS = (NUM_CARS_PEAK*(len(S_PEAK))) + (NUM_CARS_NON_PEAK* \

                  (len(S_NON)))

    #for n in range(10):

    changes_s = np.zeros(len(PEAK))

    changes_n = np.zeros(len(PEAK))

    SIM = 100

    """

    for k in range(SIM):

        for n in range(len(PEAK)):

            count = 0

            for i in range(len(S_PEAK)):

                for j in range(NUM_CARS_PEAK):

                    sc = Car(direction='South')

                    if sc.want_to_move_to_ETL(PEAK[n], S_PEAK[i], PEAK_ETL_SPEED, \

                                            PEAK_GPL_SPEED) == True:

                        count += 1

            for i in range(len(S_NON)):

                for j in range(NUM_CARS_NON_PEAK):

                    sc = Car(direction='South')

                    if sc.want_to_move_to_ETL(NON, S_NON[i], NON_ETL_SPEED, \

                                              NON_GPL_SPEED) == True:

                        count += 1

            changes_s[n] += count / TOTAL_CARS

    changes_s /= SIM

    """

    for k in range(SIM):

        for n in range(len(PEAK)):

            count = 0

            for i in range(len(N_PEAK)):

                for j in range(NUM_CARS_PEAK):

                    nc = Car(direction='North')

                    if nc.want_to_move_to_ETL(PEAK[n], N_PEAK[i], PEAK_ETL_SPEED, \

                                              PEAK_GPL_SPEED) == True:

                        count += 1

            for i in range(len(N_NON)):

                for j in range(NUM_CARS_NON_PEAK):

                    nc = Car(direction='North')

                    if nc.want_to_move_to_ETL(NON, N_NON[i], NON_ETL_SPEED, \

                                              NON_GPL_SPEED) == True:

                        count += 1

            changes_n[n] += count / TOTAL_CARS

    changes_n /= SIM

    

    plt.plot(PEAK, changes_n, 'r')

    plt.title("Northbound: Proportion of Total Cars in ETLs as \n \

              ETL Toll Price Increases")

    plt.xlabel("Toll Price ($)")

    plt.ylabel("Proportion of Cars in ETL")

    plt.show() 

    

def speed_price_sensitivity():

    """ Analyzes how proportion of cars in ETLs vs GPL changes as toll price

        changes and as speed differences change.

        

    """ 

    # Change peak prices

    PEAK = np.arange(.75, 10, .25)

    # keep at average

    NON = 1.25

    NUM_CARS_NON_PEAK = 100

    NUM_CARS_PEAK = 200

    # simulate tolling hours (non-tolling hours, ETLs act as regular lanes)

    START = 5

    END = 19

    # Use average speeds (northbound is same proportion as southbound)

    PEAK_ETL_SPEED = np.arange(30, 67)

    PEAK_GPL_SPEED = 30

    NON_ETL_SPEED = 60

    NON_GPL_SPEED = 55

    S_PEAK = np.arange(START, 10)

    N_PEAK = np.arange(15, END+1)

    S_NON = np.arange(10, END)

    N_NON = np.arange(START, 15)

    TOTAL_CARS = (NUM_CARS_PEAK*(len(S_PEAK))) + (NUM_CARS_NON_PEAK* \

                  (len(S_NON)))

    #for n in range(10):

    changes_s = np.zeros(len(PEAK))

    changes_n = np.zeros(len(PEAK))

    SIM = 100

    """

    for k in range(SIM):

        for n in range(len(PEAK)):

            count = 0

            for i in range(len(S_PEAK)):

                for j in range(NUM_CARS_PEAK):

                    sc = Car(direction='South')

                    if sc.want_to_move_to_ETL(PEAK[n], S_PEAK[i], PEAK_ETL_SPEED[n], \

                                            PEAK_GPL_SPEED) == True:

                        count += 1

            for i in range(len(S_NON)):

                for j in range(NUM_CARS_NON_PEAK):

                    sc = Car(direction='South')

                    if sc.want_to_move_to_ETL(NON, S_NON[i], NON_ETL_SPEED, \

                                              NON_GPL_SPEED) == True:

                        count += 1

            changes_s[n] += count / TOTAL_CARS

    changes_s /= SIM

    """

    for k in range(SIM):

        for n in range(len(PEAK)):

            count = 0

            for i in range(len(N_PEAK)):

                for j in range(NUM_CARS_PEAK):

                    nc = Car(direction='North')

                    if nc.want_to_move_to_ETL(PEAK[n], N_PEAK[i], PEAK_ETL_SPEED[n], \

                                              PEAK_GPL_SPEED) == True:

                        count += 1

            for i in range(len(N_NON)):

                for j in range(NUM_CARS_NON_PEAK):

                    nc = Car(direction='North')

                    if nc.want_to_move_to_ETL(NON, N_NON[i], NON_ETL_SPEED, \

                                              NON_GPL_SPEED) == True:

                        count += 1

            changes_n[n] += count / TOTAL_CARS

    changes_n /= SIM

    

    plt.plot(PEAK, changes_n, 'm')

    plt.title("Northbound: Proportion of Total Cars in ETLs as \n \

            ETL Toll Price Increases and Speed Difference Increases")

    plt.xlabel("Toll Price ($)")

    plt.ylabel("Proportion of Cars in ETL")

    plt.show() 

    

def speeds_change():

    """ Determines if the set of weights is valid

    """

    # determine most appropriate weights

    # On average between Lynnwood and Bothell both ways, 

    # data: https://www.wsdot.wa.gov/sites/default/files/2018/12/27/

    #       Toll-405-ETL-36-Month-Report.pdf

    # Proportion of cars expected to drive in ETL's: expected_proportion_use()

    expected = expected_proportion_use()

    

    # use average tolls to test: $5 during peak and $1.25 in non-peak

    PEAK = np.arange(.75, 10, .25)

    # keep at average

    NON = 1.25

    NUM_CARS_NON_PEAK = 5000

    NUM_CARS_PEAK = 10000

    # simulate only tolling hours: 5am-7pm

    START = 5

    END = 19

    # peak avg speeds southbound (same proportion was northbound too)

    # start at average speeds

    PEAK_ETL_SPEED = 60

    PEAK_GPL_SPEED = 60

    NON_ETL_SPEED = 60

    NON_GPL_SPEED = 60

    S_PEAK = np.arange(START, 10)

    N_PEAK = np.arange(15, END+1)

    S_NON = np.arange(10, END)

    N_NON = np.arange(START, 16)

    # https://www.omnicalculator.com/everyday-life/traffic-density

    TOTAL_CARS = (NUM_CARS_PEAK*(len(S_PEAK))) + (NUM_CARS_NON_PEAK* \

                  (len(S_NON)))

    SIM = 1

    diff = 0

    tol_gpl = 0

    tol_etl = 0

    for k in range(SIM):

        for n in range(len(PEAK)):

            print("Peak toll = " + str(PEAK[n]))

            count = 0

            for i in range(len(S_PEAK)):

                num_cars_gpl = 0

                num_cars_etl = 0

                for j in range(NUM_CARS_PEAK):

                    sc = Car(direction='South')

                    num_cars_gpl += 1

                    # speeds are affected

                    if sc.want_to_move_to_ETL(PEAK[n], S_PEAK[i], PEAK_ETL_SPEED, \

                                            PEAK_GPL_SPEED, [8, 2, 3, 3, 6, 8]) == True:

                        count += 1

                        num_cars_etl += 1

                        num_cars_gpl -= 1

                # total cars on gpl's and etl's so far

                tol_gpl += num_cars_gpl

                tol_etl += num_cars_etl

                # number of cars per hour

                gpl_flow = num_cars_gpl

                etl_flow = num_cars_etl

                # total cars over total length

                g_density = tol_gpl / 60

                e_density = tol_etl / 60

                # update speeds

                PEAK_ETL_SPEED = etl_flow / e_density

                PEAK_GPL_SPEED = gpl_flow / g_density

                if PEAK_GPL_SPEED <= 0.0:

                    PEAK_GPL_SPEED = 60

                print("Time: " + str(i))

                print("New ETL speed: " + str(PEAK_ETL_SPEED))

                print("New GPL speed: " + str(PEAK_GPL_SPEED))

                print(num_cars_gpl)

                print(num_cars_etl)

                    

        for i in range(len(S_NON)):

            for j in range(NUM_CARS_NON_PEAK):

                sc = Car(direction='South')

                num_cars_gpl += 1

                if sc.want_to_move_to_ETL(NON, S_NON[i], NON_ETL_SPEED, \

                                        NON_GPL_SPEED, [8, 2, 3, 3, 6, 8]) == True:

                    count += 1

                    num_cars_etl += 1

                    num_cars_gpl -= 1

        """

        for i in range(len(N_PEAK)):

            for j in range(NUM_CARS_PEAK):

                sc = Car(direction='North')

                if sc.want_to_move_to_ETL(PEAK, N_PEAK[i], PEAK_ETL_SPEED, \

                                        PEAK_GPL_SPEED, props) == True:

                    count += 1

        for i in range(len(N_NON)):

            for j in range(NUM_CARS_NON_PEAK):

                sc = Car(direction='North')

                if sc.want_to_move_to_ETL(NON, N_NON[i], NON_ETL_SPEED, \

                                        NON_GPL_SPEED, props) == True:

                    count += 1

        """

        print("GPL: " + str(num_cars_gpl))

        print("ETL: " + str(num_cars_etl))



    

#speed_sensitivity()

#price_sensitivity()

#speed_price_sensitivity()