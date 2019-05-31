

class Car2:
    def __init__(self, near_etl_length, near_exit_length, highway, \
            max_forward_moves):
        self.going_to_etl = True
        self.on_etl = True
        self.etl_entry_coord = [0,0] # (vertic, horiz)
        self.horiz = 0
        self.vertic = 0
        self.near_etl_length = near_etl_length
        self.exit_coord = [0,0]
        self.near_exit_length = near_exit_length
        self.highway = highway
        self.off_ramp = "PLACE HOLDER"
        self.max_forward_moves = max_forward_moves
    
    
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
    
    def shift_left(self):
        self.remove_old_loc(self.vertic, self.horiz)
        self.horiz -= 1
        self.add_new_loc(self.vertic, self.horiz)
        
    
    def shift_right(self):
        self.remove_old_loc(self.vertic, self.horiz)
        self.horiz += 1
        self.add_new_loc(self.vertic, self.horiz)
    
    def move_forward(self, space_avail):
        moves = space_avail if space_avail < self.max_forward_moves else \
                self.max_forward_moves
        temp_vertic = self.vertic
        self.vertic += moves
        self.remove_old_loc(temp_vertic, self.horiz)
        self.add_new_loc(self.vertic, self.horiz)
        
    def move_on_gpl(self):
        max_left = 0
        max_right = 0
        max_forward = 0
        if self.can_shift_left():
            max_left = self.get_max_left()
        if self.can_shift_right():
            max_right = self.get_max_right()
        max_forward = self.get_max_forward()
        if max_forward >= max_right and max_forward >= max_left:
            self.move_forward(max_forward)
        elif max_right >= max_left:
            self.shift_right()
            self.move_forward(max_right)
        else:
            self.shift_left()
            self.move_forward(max_left)
    
    def move_on_etl(self):
        max_forward = self.get_max_forward()
        self.move_forward(max_forward)
    
    def remove_car(self):
        exit_dict = self.highway.string_to_int
        exit_idx = exit_dict[self.off_ramp]
        exit_ramp = self.highway.exits_arr[exit_idx]
        exit_ramp.intake(self)
    
    def go_to_exit(self):
        while self.can_shift_right():
            self.shift_right()
        space_until_exit = self.exit_coord[0] - self.vertic
        max_forward = self.get_max_forward()
        min_move = space_until_exit if space_until_exit < max_forward else \
                max_forward
        self.move_forward(min_move)
        if self.vertic == self.exit_coord[0] and \
                self.horiz == self.exit_coord[1]:
            self.remove_car()
    
    def move_to_etl(self):
        while self.can_shift_left():
            self.shift_left()
        space_until_entrance = self.etl_entry_coord[0] - self.vertic
        max_forward = self.get_max_forward()
        min_move = space_until_entrance if space_until_entrance < max_forward \
                else max_forward
        self.move_forward(min_move)
        if self.vertic == self.etl_entry_coord[0]:
            self.shift_left()
            self.on_etl = True
            self.going_to_etl = False
        
    def is_near_exit(self):
        if self.exit_coord[0] - self.vertic <= self.near_exit_length:
            return True
        return False
    
    def is_near_etl(self):
        if self.etl_entry_coord[0] - self.vertic <= self.near_etl_length:
            return True
        return False
    
    def move(self, highway_grid):
        veh_locs_grid = highway_grid[:,:,0]
        lane_type_grid = highway_grid[:,:,1]
        if self.going_to_etl:
            if self.is_near_etl():
                self.move_to_etl()
            else:
                self.move_on_gpl()     
        else:
            if self.is_near_exit():
                self.go_to_exit()
            else:
                if self.on_etl:
                    self.move_on_etl()
                else:
                    self.move_on_gpl()