from car import Car
import numpy as np

def price_elasticity_weights(props, tol):
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
    good_count = 0
    for n in range(10):
        count = 0
        for i in range(len(S_PEAK)):
            for j in range(NUM_CARS_PEAK):
                sc = Car(direction='South')
                if sc.want_to_move_to_ETL(PEAK, S_PEAK[i], PEAK_ETL_SPEED, \
                                        PEAK_GPL_SPEED, props) == True:
                    count += 1
        for i in range(len(S_NON)):
            for j in range(NUM_CARS_NON_PEAK):
                sc = Car(direction='South')
                if sc.want_to_move_to_ETL(NON, S_NON[i], NON_ETL_SPEED, \
                                        NON_GPL_SPEED, props) == True:
                    count += 1
        if expected - tol < (count / TOTAL_CARS) < expected + tol:
            good_count += 1
    print(str(props) + ": " + str(good_count))
    if good_count >= 7:
        print("Good weights")
        print(props)
        return -1
    else:
        return good_count
        
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

def find_best_prop():
    """ Work in progress.
    """
    # order:
    # inc_score, time_score, commuter_score, gtg_score, hurry_score, speed_score
    # parameters:
    # all values 1-10
    # inc_score is always at least the highest (can be tied)
    # hurry_score and speed_score are the next highest (can be flipped or tied)
    # gtg_score
    # time_score, commuter_score, and gtg_score will be at least 2 lower than inc
    ins = 3
    ts = 1
    cs = 1
    gs = 1
    hs = 3
    ss = 3
    weight = np.array([ins, ts, cs, gs, hs, ss])
    good = False
    good_weights = []
    while(good == False):
        score = price_elasticity_weights(weight, .02)
        if score == -1:
            good_weights.append(weight)
            good = True
        elif score == 0 and ins <= 10:
            weight += 1
    good = False
    if len(good_weights) == 1:
        while(good == False):
            score = price_elasticity_weights(good_weights[0], .01)
            if score == -1:
                good_weights.append(weight)
                good = True
            elif 0 < score < 7 and ins <= 10:
                weight += 1
            elif score == 0 and ins <= 10:
                ins += 1
                hs += 1
                ss += 1
    
