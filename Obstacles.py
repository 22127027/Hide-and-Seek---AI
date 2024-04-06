
class Obstacles:
    def __init__(self, top, left, bottom, right, index, map):
        self.top = top
        self.left = left
        self.bottom = bottom
        self.right = right
        self.index = index
    
    def check_go_up(self, current_map):
        up_pos = self.top - 1
        for i in range(self.left, self.right + 1):
            if up_pos < 0 or current_map.map_array[up_pos][i] != 0:
                return False
        return True
    
    def check_go_down(self, current_map):
        down_pos = self.bottom + 1
        for i in range(self.left, self.right + 1):
            if down_pos > current_map.num_rows - 1 or current_map.map_array[down_pos][i] != 0:
                return False
        return True

    def check_go_left(self, current_map):
        left_pos = self.left - 1
        for i in range(self.top, self.bottom + 1):
            if left_pos < 0 or current_map.map_array[i][left_pos] != 0:
                return False
        return True
    
    def check_go_right(self, current_map):
        right_pos = self.right + 1
        for i in range(self.top, self.bottom + 1):
            if right_pos > current_map.num_cols - 1 or current_map.map_array[i][right_pos] != 0:
                return False
        return True
    
    def move_up(self, current_map):
        if self.check_go_up(current_map):
            self.top -= 1
            for i in range(self.left, self.right + 1):
                current_map.map_array[self.top][i] = 4
                current_map.map_array[self.bottom][i] = 0
            self.bottom -= 1
            
            current_map.obstacles_position[self.index][0] = self.top
            current_map.obstacles_position[self.index][2] = self.bottom
            return True
        return False
            
    def move_down(self, current_map):
        if self.check_go_down(current_map):
            self.bottom += 1
            for i in range(self.left, self.right + 1):
                current_map.map_array[self.bottom][i] = 4
                current_map.map_array[self.top][i] = 0
            self.top += 1
            current_map.obstacles_position[self.index][0] = self.top
            current_map.obstacles_position[self.index][2] = self.bottom
            return True
        return False

    def move_left(self, current_map):
        if self.check_go_left(current_map):
            self.left -= 1
            for i in range(self.top, self.bottom + 1):
                current_map.map_array[i][self.left] = 4
                current_map.map_array[i][self.right] = 0
            self.right -= 1
            current_map.obstacles_position[self.index][1] = self.left
            current_map.obstacles_position[self.index][3] = self.right

            return True
        return False

    def move_right(self, current_map):
        if self.check_go_right(current_map):
            self.right += 1
            for i in range(self.top, self.bottom + 1):
                current_map.map_array[i][self.right] = 4
                current_map.map_array[i][self.left] = 0
            self.left += 1
            current_map.obstacles_position[self.index][1] = self.left
            current_map.obstacles_position[self.index][3] = self.right
            return True
        return False

    def return_top(self):
        return self.top
    
    def return_left(self):
        return self.left
    
    def return_bottom(self):
        return self.bottom

    def return_right(self):
        return self.right  
    
    def print_position(self):
        return f"Obstacle at ({self.top}, {self.left}) to ({self.bottom}, {self.right})"
    
        