import random

ANNOUNCE_RANGE = 2
class Map:
    def __init__(self):
        self.hider_position = []
        self.seeker_position = []
        self.obstacles_position = []
        self.map_array = []
        self.num_rows = 0
        self.num_cols = 0

    def read_txt_file(self, filename):
        count = 0  # Initialize count variable
        with open(filename, 'r') as file:
            dimensions = file.readline().strip().split()
            self.num_rows, self.num_cols = map(int, dimensions)

            for row_idx, line in enumerate(file):
                if count < self.num_rows:
                    elements = line.strip().split()

                    for col_idx, element in enumerate(elements):
                        if element == '2':
                            self.hider_position.append((row_idx, col_idx))
                        elif element == '3':
                            self.seeker_position.append((row_idx, col_idx))
                    
                    row_data = [int(char) for char in line.strip("\n").split()]
                    self.map_array.append(row_data)

                    count += 1
                else:
                    self.obstacles_position.append(line.strip("\n"))

            # Remove the last element from obstacles_position if it's empty
            if self.obstacles_position and not self.obstacles_position[-1]:
                self.obstacles_position.pop()


    def createMap(self, level):
        # Assume that level is 4
        for obstacle in self.obstacles_position:
            top = obstacle[0]
            left = obstacle[1]
            bottom = obstacle[2]
            right = obstacle[3]

            for i in range(top, bottom + 1):
                for j in range(left, right + 1):
                    self.map_array[i][j] = 4



# Usage
filename = "map.txt"
current_map = Map()
current_map.read_txt_file(filename)

print("Dimensions of the table:", current_map.num_rows, "rows,", current_map.num_cols, "columns")
print("Position of hiders:", current_map.hider_position)
print("Position of seeker:", current_map.seeker_position)
print("Position of obstacles:", current_map.obstacles_position)
current_map.createMap(1)

class Agent:
    def __init__(self, position, vision_radius, bound, map, id=0, score=0):
        
        self.id = id
        self.position = position
        self.vision_radius = vision_radius
        self.score = score
        self.bound = bound
        self.map = map

        self.direction = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1 , 1), (-1, -1)] # go right, left, down, up
        self.direction_word = ["right", "left", "down", "up", "down_right", "down_left"]
        self.action = None
        self.valid_vision_left = []
        self.valid_vision_right = []
        self.valid_vision_up = []
        self.valid_vision_down = []

        self.valid_vision_up_left = []
        self.invalid_vision_up_left = []

        self.valid_vision_up_right = []
        self.invalid_vision_up_right = []

        self.valid_vision_down_left = []
        self.invalid_vision_down_left = []

        self.valid_vision_down_right = []
        self.invalid_vision_down_right = []

        self.valid_movement = []

    def check_diagonal(self, row, col, direction):
        for i in range(1, self.vision_radius + 1):
            if (direction == 'up_left' and row == self.position[0] - i and col == self.position[1] - i) or \
               (direction == 'up_right' and row == self.position[0] - i and col == self.position[1] + i) or \
               (direction == 'down_left' and row == self.position[0] + i and col == self.position[1] - i) or \
               (direction == 'down_right' and row == self.position[0] + i and col == self.position[1] + i):
                return True
        return False

    def check_diagonal_down(self, row, col, direction):
        for _ in range(1, self.vision_radius + 1):
            if (direction == 'up_left' and abs(row - col) > abs (self.position[0] - self.position[1])) or \
               (direction == 'up_right' and abs(row - col) < abs (self.position[0] - self.position[1])) or \
               (direction == 'down_left' and abs(row + col) > abs (self.position[0] + self.position[1])) or \
               (direction == 'down_right' and abs(row + col) < abs (self.position[0] + self.position[1])):
                return True
        return False
    
    def check_invalid_vision(self, row, col, direction):
        invalid_direction_attr = "invalid_vision_" + direction
        invalid_direction = getattr(self, invalid_direction_attr, [])
        
        if len(invalid_direction) == 0:
            return True

        for tpl in invalid_direction:
            tpl_row, tpl_col = tpl[0], tpl[1]
            if direction == 'up_left':
                if not self.check_diagonal(row, col, direction) and self.check_diagonal_down(row, col, direction) and (col == tpl_col - 1 and (row == tpl_row or row == tpl_row - 1)) or \
                not self.check_diagonal(row, col, direction) and not self.check_diagonal_down(row, col, direction) and (row == tpl_row - 1 and (col == tpl_col or col == tpl_col - 1)) or \
                self.check_diagonal(tpl_row, tpl_col, direction) and (row == tpl_row or col == tpl_col) or \
                self.check_diagonal(tpl_row, tpl_col, direction) and self.check_diagonal(row, col, direction):
                    return False
            elif direction == 'up_right':
                if not self.check_diagonal(row, col, direction) and not self.check_diagonal_down(row, col, direction) and (col == tpl_col + 1 and (row == tpl_row or row == tpl_row - 1)) or \
                not self.check_diagonal(row, col, direction) and self.check_diagonal_down(row, col, direction) and (row == tpl_row - 1 and (col == tpl_col or col == tpl_col + 1)) or \
                self.check_diagonal(tpl_row, tpl_col, direction) and (row == tpl_row or col == tpl_col) or \
                self.check_diagonal(tpl_row, tpl_col, direction) and self.check_diagonal(row, col, direction):
                    return False
            elif direction == 'down_left':
                if not self.check_diagonal(row, col, direction) and not self.check_diagonal_down(row, col, direction) and (col == tpl_col - 1 and (row == tpl_row or row == tpl_row + 1)) or \
                not self.check_diagonal(row, col, direction) and self.check_diagonal_down(row, col, direction) and (row == tpl_row + 1 and (col == tpl_col or col == tpl_col - 1)) or \
                self.check_diagonal(tpl_row, tpl_col, direction) and (row == tpl_row or col == tpl_col) or \
                self.check_diagonal(tpl_row, tpl_col, direction) and self.check_diagonal(row, col, direction):
                    return False
            elif direction == 'down_right':
                if not self.check_diagonal(row, col, direction) and self.check_diagonal_down(row, col, direction) and (col == tpl_col + 1 and (row == tpl_row or row == tpl_row + 1)) or \
                not self.check_diagonal(row, col, direction) and not self.check_diagonal_down(row, col, direction) and (row == tpl_row + 1 and (col == tpl_col or col == tpl_col + 1)) or \
                self.check_diagonal(tpl_row, tpl_col, direction) and (row == tpl_row or col == tpl_col) or \
                self.check_diagonal(tpl_row, tpl_col, direction) and self.check_diagonal(row, col):
                    return False
                    
        return True
    
    def check_vision_in_diagonal_direction(self, direction):
        for row in range(1, self.vision_radius + 1):
            for col in range(1, self.vision_radius + 1):
                if direction == 'up_left':
                    if self.position[0] - row >= 0 and self.position[1] - col >= 0 and self.check_invalid_vision(self.position[0] - row, self.position[1] - col, direction) and self.map[self.position[0] - row][self.position[1] - col] == 0:
                        self.valid_vision_up_left.append((self.position[0] - row, self.position[1] - col))
                    elif self.position[0] - row >= 0 and self.position[1] - col >= 0:
                        self.invalid_vision_up_left.append((self.position[0] - row, self.position[1] - col))

                elif direction == 'up_right':
                    if self.position[0] - row >= 0 and self.position[1] + col < self.bound[1] and self.check_invalid_vision(self.position[0] - row, self.position[1] + col, direction) and self.map[self.position[0] - row][self.position[1] + col] == 0:
                        self.valid_vision_up_right.append((self.position[0] - row, self.position[1] + col))
                    elif self.position[0] - row >= 0 and self.position[1] + col < self.bound[1]:
                        self.invalid_vision_up_right.append((self.position[0] - row, self.position[1] + col))

                elif direction == 'down_left':
                    if self.position[0] + row < self.bound[0] and self.position[1] - col >= 0 and self.check_invalid_vision(self.position[0] + row, self.position[1] - col, direction) and self.map[self.position[0] + row][self.position[1] - col] == 0:
                        self.valid_vision_down_left.append((self.position[0] + row, self.position[1] - col))
                    elif self.position[0] + row < self.bound[0] and self.position[1] - col >= 0:
                        self.invalid_vision_down_left.append((self.position[0] + row, self.position[1] - col))

                elif direction == 'down_right':
                    if self.position[0] + row < self.bound[0] and self.position[1] + col < self.bound[1] and self.check_invalid_vision(self.position[0] + row, self.position[1] + col, direction) and self.map[self.position[0] + row][self.position[1] + col] == 0:
                        self.valid_vision_down_right.append((self.position[0] + row, self.position[1] + col))
                    elif self.position[0] + row < self.bound[0] and self.position[1] + col < self.bound[1]:
                        self.invalid_vision_down_right.append((self.position[0] + row, self.position[1] + col))


    
    def check_vision_in_direction(self, direction):
        for i in range(1, self.vision_radius + 1):
            if direction == 'left':
                if self.position[1] - i >= 0 and self.map[self.position[0]][self.position[1] - i] == 0:
                    self.valid_vision_left.append((self.position[0], self.position[1] - i))
                else:
                    break
            elif direction == 'right':
                if self.position[1] + i < self.bound[1] and self.map[self.position[0]][self.position[1] + i] == 0:
                    self.valid_vision_right.append((self.position[0], self.position[1] + i))
                else:
                    break
            elif direction == 'up':
                if self.position[0] - i >= 0 and self.map[self.position[0] - i][self.position[1]] == 0:
                    self.valid_vision_up.append((self.position[0] - i, self.position[1]))
                else:
                    break
            elif direction == 'down':
                if self.position[0] + i < self.bound[0] and self.map[self.position[0] + i][self.position[1]] == 0:
                    self.valid_vision_down.append((self.position[0] + i, self.position[1]))
                else:
                    break

    def agent_valid_vision(self):
        for i in range (0, 4):
            self.check_vision_in_direction(self.direction_word[i])
        
        for i in range (4, 8):
            self.check_vision_in_diagonal_direction(self.direction_word[i])

    def move(self, direction_index):
        self.position = tuple(map(sum, zip(self.position, self.directions[direction_index])))

    def agent_go_right(self):
        self.move(0)

    def agent_go_left(self):
        self.move(1)

    def agent_go_down(self):
        self.move(2)

    def agent_go_up(self):
        self.move(3)

    def agent_go_down_right(self):
        self.move(4)

    def agent_go_down_left(self):
        self.move(5)

    def agent_go_up_right(self):
        self.move(6)

    def agent_go_up_left(self):
        self.move(7)

        
class Obstacles:
    def __init__(self, top, left, bottom, right, index):
        self.top = top
        self.left = left
        self.bottom = bottom
        self.right = right
        self.index = index
    
    def check_go_up(self):
        up_pos = self.top - 1
        for i in range(self.left, self.right + 1):
            if (up_pos < 0 or current_map.map_array[up_pos][i] != 0):
                return False
        return True
    
    def check_go_down(self):
        down_pos = self.bottom + 1
        for i in range(self.left, self.right + 1):
            if (down_pos > current_map.num_rows - 1 or current_map.map_array[down_pos][i] != 0):
                return False
        return True

    def check_go_left(self):
        left_pos = self.left - 1
        for i in range(self.top, self.bottom + 1):
            if (left_pos < 0 or current_map.map_array[i][left_pos] != 0):
                return False
        return True
    
    def check_go_right(self):
        right_pos = self.right + 1
        for i in range(self.top, self.bottom + 1):
            if (right_pos > current_map.num_cols - 1 or current_map.map_array[i][right_pos] != 0):
                return False
        return True
    
    def move_up(self):
        self.top = self.top - 1
        for i in range(self.left, self.right + 1):
            current_map.map_array[self.top][i] = 4
            current_map.map_array[self.bottom][i] = 0

        self.bottom = self.bottom - 1

        current_map.obstacles_position[self.index][0] = self.top
        current_map.obstacles_position[self.index][2] = self.bottom
            
    def move_down(self):
        self.bottom = self.bottom + 1
        for i in range(self.left, self.right + 1):
            current_map.map_array[self.bottom][i] = 4
            current_map.map_array[self.top][i] = 0

        self.top = self.top + 1
        current_map.obstacles_position[self.index][0] = self.top
        current_map.obstacles_position[self.index][2] = self.bottom

    def move_left(self):
        self.left = self.left - 1
        for i in range(self.top, self.bottom + 1):
            current_map.map_array[i][self.left] = 4
            current_map.map_array[i][self.right] = 0
            
        self.right = self.right - 1
        current_map.obstacles_position[self.index][1] = self.left
        current_map.obstacles_position[self.index][3] = self.right

    def move_right(self):
        self.right = self.right + 1
        for i in range(self.top, self.bottom + 1):
            current_map.map_array[i][self.right] = 4
            current_map.map_array[i][self.left] = 0

        self.left = self.left - 1
        current_map.obstacles_position[self.index][1] = self.left
        current_map.obstacles_position[self.index][3] = self.right



class Hider(Agent):
    def __init__(self, position, vision_radius, bound, map, id=0, score=0):
        Agent.__init__(self, position, vision_radius, bound, map, id=0, score=0)
        self.id = 2
    def unit_range(self):
        top = self.position[0] - ANNOUNCE_RANGE
        left = self.position[1] - ANNOUNCE_RANGE
        bottom = self.position[0] + ANNOUNCE_RANGE
        right = self.position[1] + ANNOUNCE_RANGE

        if (self.position[0] - ANNOUNCE_RANGE < 0):
            index = 1
            while True:
                if (self.position[0] - ANNOUNCE_RANGE + index >= 0):
                    top = self.position[0] - ANNOUNCE_RANGE + index
                    break
                else: index = index + 1
        if (self.position[1] - ANNOUNCE_RANGE < 0):
            index = 1
            while True:
                if (self.position[1] - ANNOUNCE_RANGE + index >= 0):
                    left = self.position[1] - ANNOUNCE_RANGE + index
                    break
                else: index = index + 1

        if (self.position[0] + ANNOUNCE_RANGE > current_map.num_rows - 1):
            index = 1
            while True:
                if (self.position[0] + ANNOUNCE_RANGE - index <= current_map.num_rows - 1):
                    bottom = self.position[0] + ANNOUNCE_RANGE - index
                    break
                else: index = index + 1

        if (self.position[1] + ANNOUNCE_RANGE > current_map.num_cols - 1):
            index = 1
            while True:
                if (self.position[1] + ANNOUNCE_RANGE - index <= current_map.num_rows - 1):
                    right = self.position[1] + ANNOUNCE_RANGE - index
                    break
                else: index = index + 1


        matrix_range = []
        rows = bottom + 1 - top
        cols = right + 1 - left
        for i in range(top, bottom + 1):
            row = []
            for j in range(left, right + 1):
                if (current_map.map_array[i][j] != None):
                  row.append(current_map.map_array[i][j])
            
            matrix_range.append(row)

        return matrix_range, rows, cols, top, left, bottom, right
    def announce(self, seekers_moves):
        if (seekers_moves == 5):
            rows = 0
            cols = 0
            matrix_range, rows, cols, top, left, bottom, right = self.unit_range()
            while True:
                rand_row_index = random.randint(0, rows - 1)
                rand_col_index = random.randint(0, cols - 1)
                if (matrix_range[rand_row_index][rand_col_index] == 0):
                    break
                
            matrix_range[rand_row_index][rand_col_index] = 5
            for row in matrix_range:
                print(row)
            print()


        current_map.map_array[rand_row_index + top][rand_col_index + left] = 5     
        announce_coordinate = (rand_row_index + top, rand_col_index + left)
        

        return announce_coordinate
    
    

class Seeker(Agent): 
    def __init__(self, position, vision_radius, bound, map, id=0, score=0):
        Agent.__init__(self, position, vision_radius, bound, map, id=0, score=0)
        self.id = 3
    def catch(self, hider_position):
        return self.position == hider_position
    
    def updatePoint(self, level, hider_position):
        # Catch hider
        if (self.catch(self, hider_position)):
            self.point = 20
        else:
            self.point -= 1


obstacles_list = []
for i in range(len(current_map.obstacles_position)):
    obs = Obstacles(current_map.obstacles_position[i][0], current_map.obstacles_position[i][1], current_map.obstacles_position[i][2], current_map.obstacles_position[i][3], i)
    obstacles_list.append(obs)

    if (obstacles_list[i].check_go_down()):
        obstacles_list[i].move_down()
    else:
        print("Can not move")

    

for row in current_map.map_array:
    print(row)

print(current_map.obstacles_position)
'''
seeker1 = Seeker(current_map.seeker_position[0], 3, (current_map.num_rows, current_map.num_cols), current_map.map_array)
print(seeker1.position)
seeker1.agent_valid_vision()
print(seeker1.invalid_vision_up_left)
print(seeker1.valid_vision_up_left)
print(seeker1.invalid_vision_down_right)
print(seeker1.valid_vision_down_right)
seeker1.agent_go_down()
for row in current_map.map_array:
    print(row)

for i in range(len(current_map.hider_position)):
    hider = Hider(current_map.hider_position[i], 3, (current_map.num_rows, current_map.num_cols), current_map.map_array)
    announce_position = hider.announce(5)
    for row in current_map.map_array:
        print(row)

    print()
    current_map.map_array[announce_position[0]][announce_position[1]] = 0
'''