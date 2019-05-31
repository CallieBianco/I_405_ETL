# This file contains methods that will be eventually added to car.py
import numpy as N

# For setters
# Note: The following values are place holders
GTG_PASS_PROB = 0.5
# https://cleantechnica.com/2016/10/14/common-mode-transportation
#-work-us-driving-alone-private-vehicle-us-census-data-reveals/
POP_PROBS = N.array([[1,2,3,4,5], [0.764, 0.884, 0.944, 0.974, 1]])
FREQ_COMM_PROB = 0.9

# For car move functions
VEH_LOCS_GRID = None # Placeholder
LANE_TYPE_GRID = None # Placeholder
HIGHWAY = None
ON_ETL = False
GOING_TO_ETL = True
ETL_ENTRY_COORD = (2,2) # (vertic, horiz). Placeholder
EXIT_COORD = (3,7) # (vertic, horiz). Placeholder
NEAR_EXIT_LENGTH = 7 # Note: This is a placeholder.
NEAR_ETL_LENGTH = 7
MAX_FORWARD_MOVES = 7 # Placeholder
vertic = 0
horiz = 0
off_ramp = "Bothell" # Placeholder


# Decides if car has good to go pass.
# Returns true or false.
def set_has_gtg():
    if N.random.uniform(0, 1) < GTG_PASS_PROB:
        return True
    else:
        return False

# Sets population of car
# Returns population of car
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
# Returns True or False
def set_freq_commuter():
    if N.random.uniform(0, 1) < FREQ_COMM_PROB:
        return True
    else:
        return False

def remove_old_loc(ver, hor):
    VEH_LOCS_GRID[ver, hor] = 0
    VEH_LOCS_GRID[ver - 1, hor] = 0

def add_new_loc(ver, hor):
    VEH_LOCS_GRID[ver, hor] = 1
    VEH_LOCS_GRID[ver - 1, hor] = 1

def can_shift_left():
    # Check if general purpose lane to left
    if LANE_TYPE_GRID[vertic, horiz - 1] != 0:
        return False
    if VEH_LOCS_GRID[vertic, horiz - 1] == 0 and \
            VEH_LOCS_GRID[vertic - 1, horiz - 1] == 0:
        return True
    else:
        return False

def can_shift_right():
    # Check if general purpose lane to right
    if LANE_TYPE_GRID[vertic, horiz + 1] != 0:
        return False
    if VEH_LOCS_GRID[vertic, horiz + 1] == 0 and \
            VEH_LOCS_GRID[vertic - 1, horiz + 1] == 0:
        return True
    else:
        return False

# Note: Do all cars take an exit located on the grid?
def get_max_left():
    max_moves = 0
    idx = vertic + 1
    while VEH_LOCS_GRID[idx, horiz - 1] == 0:
        max_moves += 1
        idx += 1
    return max_moves

def get_max_right():
    max_moves = 0
    idx = vertic + 1
    while VEH_LOCS_GRID[idx, horiz + 1] == 0:
        max_moves += 1
        idx += 1
    return max_moves

def get_max_forward():
    max_moves = 0
    idx = vertic + 1
    while VEH_LOCS_GRID[idx, horiz] == 0:
        max_moves += 1
        idx += 1
    return max_moves

def shift_left():
    remove_old_loc(vertic, horiz)
    horiz -= 1
    add_new_loc(vertic, horiz)
    

def shift_right():
    remove_old_loc(vertic, horiz)
    horiz += 1
    add_new_loc(vertic, horiz)

def move_forward(space_avail):
    moves = space_avail if space_avail < MAX_FORWARD_MOVES else \
            MAX_FORWARD_MOVES
    temp_vertic = vertic
    vertic += moves
    remove_old_loc(temp_vertic, horiz)
    add_new_loc(vertic, horiz)
    
def move_on_gpl():
    max_left = 0
    max_right = 0
    max_forward = 0
    if can_shift_left():
        max_left = get_max_left()
    if can_shift_right():
        max_right = get_max_right()
    max_forward = get_max_forward()
    if max_forward >= max_right and max_forward >= max_left:
        move_forward(max_forward)
    elif max_right >= max_left:
        shift_right()
        move_forward(max_right)
    else:
        shift_left()
        move_forward(max_left)

def move_on_etl():
    max_forward = get_max_forward()
    move_forward(max_forward)

def remove_car():
    exit_dict = HIGHWAY.string_to_int
    exit_idx = exit_dict[off_ramp]
    exit_ramp = HIGHWAY.exits_arr[exit_idx]
    exit_ramp.intake(self)

def go_to_exit():
    while can_shift_right():
        shift_right()
    space_until_exit = EXIT_COORD[0] - vertic
    max_forward = get_max_forward()
    min_move = space_until_exit if space_until_exit < max_forward else \
            max_forward
    move_forward(min_move)
    if vertic == EXIT_COORD[0] and horiz == EXIT_COORD[1]:
        remove_car()

def move_to_etl():
    while can_shift_left():
        shift_left()
    space_until_entrance = ETL_ENTRY_COORD[0] - vertic
    max_forward = get_max_forward()
    min_move = space_until_entrance if space_until_entrance < max_forward \
            else max_forward
    move_forward(min_move)
    if vertic == ETL_ENTRY_COORD[0]:
        shift_left()
        ON_ETL = True
        GOING_TO_ETL = False
    
        

def is_near_exit():
    if EXIT_COORD[0] - vertic <= NEAR_EXIT_LENGTH:
        return True
    return False

def is_near_etl():
    if ETL_ENTRY_COORD[0] - vertic <= NEAR_ETL_LENGTH:
        return True
    return False

def move():
    if GOING_TO_ETL:
        if is_near_etl():
            move_to_etl()
        else:
            move_on_gpl()     
    else:
        if is_near_exit():
            go_to_exit()
        else:
            if ON_ETL:
                move_on_etl()
            else:
                move_on_gpl()

# The following are just tests
# Test if the flow works
# Test if each function works
        