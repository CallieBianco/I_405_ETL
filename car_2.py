# This file contains methods that will be eventually added to car.py
import numpy as N

GTG_PASS_PROB = 0.5
POP_PROBS = N.array([[0,1,2,3], [0.2, 0.5, 0.8, 1]])
FREQ_COMM_PROB = 0.5

# Decides if car has good to go pass.
# Returns true or false.
def set_has_gtg():
    if N.random.uniform(0, 1) < GTG_PASS_PROB:
        return True
    else:
        return False

# Sets population of car
def set_pop():
    rand = N.random.uniform(0, 1)
    pop = None
    idx = 0
    while pop is None:
        if rand < POP_PROBS[1, idx]:
            pop = POP_PROBS[0, idx]
        else:
            idx += 1
    return pop

# Sets if car is freq commuter
def set_freq_commuter():
    if N.random.uniform(0, 1) < FREQ_COMM_PROB:
        return True
    else:
        return False