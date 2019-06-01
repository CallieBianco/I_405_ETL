import numpy as N
import matplotlib.pyplot as plt
import time

class Car2:
    def __init__(self, near_etl_length, near_exit_length, highway, \
            max_forward_moves):
        self.going_to_etl = False
        self.on_etl = False
        self.etl_entry_coord = [0,0] # (vertic, horiz)
        self.horiz = 3
        self.vertic = 1
        self.near_etl_length = near_etl_length
        self.exit_coord = [19,4] # (vertic, horiz)
        self.near_exit_length = near_exit_length
        self.highway = highway
        self.off_ramp = "PLACE HOLDER"
        self.max_forward_moves = max_forward_moves
    
    
    def remove_old_loc(self, veh_locs_grid, ver, hor):
        veh_locs_grid[ver, hor] = 0
        veh_locs_grid[ver - 1, hor] = 0

    def add_new_loc(self, veh_locs_grid, ver, hor):
        veh_locs_grid[ver, hor] = 1
        veh_locs_grid[ver - 1, hor] = 1
    
    def can_shift_left(self, veh_locs_grid, lane_type_grid):
        # Check if general purpose lane to left
        if lane_type_grid[self.vertic, self.horiz - 1] != 0:
            return False
        if veh_locs_grid[self.vertic, self.horiz - 1] == 0 and \
                veh_locs_grid[self.vertic - 1, self.horiz - 1] == 0:
            return True
        else:
            return False
    
    def can_shift_right(self, veh_locs_grid, lane_type_grid):
        # Check if general purpose lane to right
        if lane_type_grid[self.vertic, self.horiz + 1] != 0:
            return False
        if veh_locs_grid[self.vertic, self.horiz + 1] == 0 and \
                veh_locs_grid[self.vertic - 1, self.horiz + 1] == 0:
            return True
        else:
            return False
    
    # Note: Do all cars take an exit located on the grid?
    def get_max_left(self, veh_locs_grid, grid_length):
        max_moves = 0
        idx = self.vertic + 1
        while idx < grid_length and veh_locs_grid[idx, self.horiz - 1] == 0:
            max_moves += 1
            idx += 1
        return max_moves
    
    def get_max_right(self, veh_locs_grid, grid_length):
        max_moves = 0
        idx = self.vertic + 1
        while idx < grid_length and veh_locs_grid[idx, self.horiz + 1] == 0:
            max_moves += 1
            idx += 1
        return max_moves
    
    def get_max_forward(self, veh_locs_grid, grid_length):
        max_moves = 0
        idx = self.vertic + 1
        while idx < grid_length and veh_locs_grid[idx, self.horiz] == 0:
            max_moves += 1
            idx += 1
        return max_moves
    
    def shift_left(self, veh_locs_grid):
        self.remove_old_loc(veh_locs_grid, self.vertic, self.horiz)
        self.horiz -= 1
        self.add_new_loc(veh_locs_grid, self.vertic, self.horiz)
        
    
    def shift_right(self, veh_locs_grid):
        self.remove_old_loc(veh_locs_grid, self.vertic, self.horiz)
        self.horiz += 1
        self.add_new_loc(veh_locs_grid, self.vertic, self.horiz)
    
    def move_forward(self, space_avail, veh_locs_grid):
        moves = space_avail if space_avail < self.max_forward_moves else \
                self.max_forward_moves
        temp_vertic = self.vertic
        self.vertic += moves
        self.remove_old_loc(veh_locs_grid, temp_vertic, self.horiz)
        self.add_new_loc(veh_locs_grid, self.vertic, self.horiz)
        
    def move_on_gpl(self, veh_locs_grid, lane_type_grid):
        max_left = 0
        max_right = 0
        max_forward = 0
        grid_length = N.size(veh_locs_grid[:, 0])
        if self.can_shift_left(veh_locs_grid, lane_type_grid):
            max_left = self.get_max_left(veh_locs_grid, grid_length)
        if self.can_shift_right(veh_locs_grid, lane_type_grid):
            max_right = self.get_max_right(veh_locs_grid, grid_length)
        max_forward = self.get_max_forward(veh_locs_grid, grid_length)
        if max_forward >= max_right and max_forward >= max_left:
            self.move_forward(max_forward, veh_locs_grid)
        elif max_right >= max_left:
            self.shift_right(veh_locs_grid)
            self.move_forward(max_right, veh_locs_grid)
        else:
            self.shift_left(veh_locs_grid)
            self.move_forward(max_left, veh_locs_grid)
    
    def move_on_etl(self, veh_locs_grid):
        grid_length = N.size(veh_locs_grid[:, 0])
        max_forward = self.get_max_forward(veh_locs_grid, grid_length)
        self.move_forward(max_forward, veh_locs_grid)
    
    def remove_car(self):
        print("Car removed")
        #exit_dict = self.highway.string_to_int
        #exit_idx = exit_dict[self.off_ramp]
        #exit_ramp = self.highway.exits_arr[exit_idx]
        #exit_ramp.intake(self)
    
    def go_to_exit(self, veh_locs_grid, lane_type_grid):
        while self.can_shift_right(veh_locs_grid, lane_type_grid):
            self.shift_right(veh_locs_grid)
        space_until_exit = self.exit_coord[0] - self.vertic
        grid_length = N.size(veh_locs_grid[:, 0])
        max_forward = self.get_max_forward(veh_locs_grid, grid_length)
        min_move = space_until_exit if space_until_exit < max_forward else \
                max_forward
        self.move_forward(min_move, veh_locs_grid)
        if self.vertic == self.exit_coord[0] and \
                self.horiz == self.exit_coord[1]:
            self.remove_car()
    
    def move_to_etl(self, veh_locs_grid, lane_type_grid):
        while self.can_shift_left(veh_locs_grid, lane_type_grid):
            self.shift_left(veh_locs_grid)
        space_until_entrance = self.etl_entry_coord[0] - self.vertic
        grid_length = N.size(veh_locs_grid[:, 0])
        max_forward = self.get_max_forward(veh_locs_grid, grid_length)
        min_move = space_until_entrance if space_until_entrance < max_forward \
                else max_forward
        self.move_forward(min_move, veh_locs_grid)
        if self.vertic == self.etl_entry_coord[0]:
            self.shift_left(veh_locs_grid)
            self.on_etl = True
            self.going_to_etl = False
        
    def is_near_exit(self):
        if self.exit_coord[0] - self.vertic <= self.near_exit_length:
            return True
        return False
    
    def update_nearest_etl(self):
        entry_arr = self.highway.etl_entry_arr
        for i in range(len(entry_arr)):
            if self.vertic <= entry_arr[i][0]:
                self.etl_entry_coord[0] = entry_arr[i][0]
                self.etl_entry_coord[1] = entry_arr[i][1]
    
    def is_near_etl(self):
        self.update_nearest_etl()
        if self.etl_entry_coord[0] - self.vertic <= self.near_etl_length:
            return True
        return False
    
    def move(self, highway_grid):
        veh_locs_grid = highway_grid[:,:,0]
        lane_type_grid = highway_grid[:,:,1]
        if self.is_near_etl() and self.want_to_move_to_ETL():
            self.move_to_etl(veh_locs_grid, lane_type_grid)
        else:
            if self.is_near_exit():
                self.go_to_exit(veh_locs_grid, lane_type_grid)
            else:
                if self.on_etl:
                    self.move_on_etl(veh_locs_grid)
                else:
                    self.move_on_gpl(veh_locs_grid, lane_type_grid)
            
            
            
        #if self.going_to_etl:
         #   if self.is_near_etl():
          #      self.move_to_etl(veh_locs_grid, lane_type_grid)
           # else:
            #    self.move_on_gpl(veh_locs_grid, lane_type_grid)     
        #else:
         #   if self.is_near_exit():
          #      self.go_to_exit(veh_locs_grid, lane_type_grid)
           # else:
            #    if self.on_etl:
             #       self.move_on_etl(veh_locs_grid)
              #  else:
               #     self.move_on_gpl(veh_locs_grid, lane_type_grid)

def animate(grid_steps):
    # create the figure
    fig = plt.figure()
    ax = fig.add_subplot(111)
    im = ax.imshow(N.array(grid_steps[0]))
    plt.show(block=False)
    
    # draw some data in loop
    for i in range(1, len(grid_steps)):
        #wait for a second
        time.sleep(1)
        #replace the image contents
        im.set_array(grid_steps[i])
        #redraw the figure
        fig.canvas.draw()


if __name__ == "__main__":
    grids = N.zeros((20, 6, 4))
    grids[:, 0, 1] = 2
    grids[:, -1, 1] = 2
    grids[:, 1, 1] = 1
    
    #Remove old and add new car location test
    car = Car2(7,7,None, 7)
    car.add_new_loc(grids[:,:,0], 1, 3)
    if grids[1,3,0] == 1 and grids[0,3,0] == 1:
        print("passed test 1")
    car.remove_old_loc(grids[:,:,0], 1, 3)
    if grids[1,3,0] == 0 and grids[0,3,0] == 0:
        print("passed test 2")
    
    # Able to shift test
    car.add_new_loc(grids[:,:,0], 1, 3)
    results = []
    for i in range(1,4):
        car.add_new_loc(grids[:,:,0], i, 2)
        car.add_new_loc(grids[:,:,0], i, 4)
        results.append(car.can_shift_left(grids[:,:,0], grids[:,:,1]))
        results.append(car.can_shift_right(grids[:,:,0], grids[:,:,1]))
        car.remove_old_loc(grids[:,:,0], i, 2)
        car.remove_old_loc(grids[:,:,0], i, 4)
    if results == [False, False, False, False, True, True]:
        print("passed test 3")
        
    # Shifting left or right test
    car.shift_left(grids[:,:,0])
    if grids[1,3,0] == 0 and grids[0,3,0] == 0 and \
            grids[1,2,0] == 1 and grids[0,2,0] == 1 and \
            car.vertic == 1 and car.horiz == 2:
        print("passed test 4")
    car.shift_right(grids[:,:,0])
    if grids[1,3,0] == 1 and grids[0,3,0] == 1 and \
            grids[1,2,0] == 0 and grids[0,2,0] == 0 and \
            car.vertic == 1 and car.horiz == 3:
        print("passed test 5")
    
    # Checking GPL travel and exiting
    #car.add_new_loc(grids[:,:,0], 1, 3)
    #car.add_new_loc(grids[:,:,0], 3, 3)
    #car.add_new_loc(grids[:,:,0], 3, 2)
    #grid_steps = []
    #grid_steps.append(N.ndarray.tolist(grids[:,:,0]))
    #car.move(grids)
    #grid_steps.append(N.ndarray.tolist(grids[:,:,0]))
    #car.move(grids)
    #grid_steps.append(N.ndarray.tolist(grids[:,:,0]))
    #car.move(grids)
    #grid_steps.append(N.ndarray.tolist(grids[:,:,0]))
    #animate(grid_steps)
    
    # ETL testing
    car.add_new_loc(grids[:,:,0], 1, 3)
    car.going_to_etl = True
    car.etl_entry_coord[0] = 6
    car.etl_entry_coord[1] = 1
    grid_steps = []
    grid_steps.append(N.ndarray.tolist(grids[:,:,0]))
    car.move(grids)
    grid_steps.append(N.ndarray.tolist(grids[:,:,0]))
    car.move(grids)
    grid_steps.append(N.ndarray.tolist(grids[:,:,0]))
    car.move(grids)
    grid_steps.append(N.ndarray.tolist(grids[:,:,0]))
    animate(grid_steps)
    
    
    
    
    