from car import Car
import numpy as N

EXPECTED_FREQ_COMM_AVG = 0.5
EXPECTED_POP_AVG = 1.5
EXPECTED_HAS_GTG_AVG = 0.5
MAX_AVG_ERR = 0.1

def car_setters_test():
    auto_veh = Car()
    freq_comm_avg = 0
    pop_avg = 0
    has_gtg_avg = 0
    for i in range(5000):
        freq_comm_avg += auto_veh.set_freq_commuter()
        pop_avg += auto_veh.set_pop()
        has_gtg_avg += auto_veh.set_has_gtg()
    freq_comm_avg /= 5000
    pop_avg /= 5000
    has_gtg_avg /= 5000
    if N.absolute(EXPECTED_FREQ_COMM_AVG - freq_comm_avg) <= 0.1:
        print("set_freq_commuter() passed")
    else:
        print("set_freq_commuter() may have some issues")
    if N.absolute(EXPECTED_POP_AVG - pop_avg) <= 0.1:
        print("set_pop() passed")
    else:
        print("set_pop() may have some issues")
    if N.absolute(EXPECTED_HAS_GTG_AVG - has_gtg_avg) <= 0.1:
        print("set_has_gtg() passed")
    else:
        print("set_has_gtg() may have some issues")
        
    

def car_test():
    car_setters_test()
    
if __name__ == "__main__":
    car_test()

