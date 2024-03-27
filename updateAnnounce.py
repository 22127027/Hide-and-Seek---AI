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
                    row_data = [int(char) for char in line.strip("\n").split()]
                    self.obstacles_position.append(row_data)

            # Remove the last element from obstacles_position if it's empty
            if self.obstacles_position and not self.obstacles_position[-1]:
                self.obstacles_position.pop()


    def createMap(self, level):
        # Assume that level is 1
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
    def __init__(self, position, vision_radius, bound, map, score=0):
        self.position = position
        self.vision_radius = vision_radius
        self.score = score
        self.bound = bound
        self.map = map

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

    def check_diagonal_up_left(self, row, col):
        for i in range(1, self.vision_radius + 1):
            if ( row == self.position[0] - i and col == self.position[1] - i):
                return True
        return False

    def check_diagonal_up_right(self, row, col):
        for i in range(1, self.vision_radius + 1):
            if (row == self.position[0] - i and col == self.position[1] + i):
                return True
        return False

    def check_diagonal_down_left(self, row, col):
        for i in range(1, self.vision_radius + 1):
            if ( row == self.position[0] + i and col == self.position[1] - i):
                return True
        return False
    
    def check_diagonal_down_right(self, row, col):
        for i in range(1, self.vision_radius + 1):
            if ( row == self.position[0] + i and col == self.position[1] + i):
                return True
        return False
    
    
    def check_diagonal_down_of_up_left(self, row, col):
        for _ in range(1, self.vision_radius + 1):
            if (abs(row - col) > abs (self.position[0] - self.position[1])):
                return True
        return False
    
    def check_diagonal_down_of_up_right(self, row, col):
        for _ in range(1, self.vision_radius + 1):
            if (abs(row - col) < abs (self.position[0] - self.position[1])):
                return True
        return False
    
    def check_diagonal_down_of_down_left(self, row, col):
        for _ in range(1, self.vision_radius + 1):
            if (abs(row + col) > abs (self.position[0] + self.position[1])):
                return True
        return False
    
    def check_diagonal_down_of_down_right(self, row, col):
        for _ in range(1, self.vision_radius + 1):
            if (abs(row + col) < abs (self.position[0] + self.position[1])):
                return True
        return False
    
    def check_invalid_vision_up_left(self, row, col):
        if len(self.invalid_vision_up_left) == 0:
            return True

        for tpl in self.invalid_vision_up_left:
            if not self.check_diagonal_up_left(row, col) and self.check_diagonal_down_of_up_left(row, col) and ( col == tpl[1] - 1 and ( row == tpl[0] or row == tpl[0] - 1)):
                return False
            elif not self.check_diagonal_up_left(row, col) and not self.check_diagonal_down_of_up_left(row, col) and ( row == tpl[0] - 1 and ( col == tpl[1] or col == tpl[1] - 1)):
                return False
            elif self.check_diagonal_up_left(tpl[0], tpl[1]) and (row == tpl[0] or col == tpl[1]):
                return False
            elif self.check_diagonal_up_left(tpl[0], tpl[1]) and self.check_diagonal_up_left(row, col):
                return False
        return True
    
    def check_invalid_vision_up_right(self, row, col):
        if len(self.invalid_vision_up_right) == 0:
            return True

        for tpl in self.invalid_vision_up_right:
            if not self.check_diagonal_up_right(row, col) and not self.check_diagonal_down_of_up_right(row, col) and ( col == tpl[1] + 1 and ( row == tpl[0] or row == tpl[0] - 1)):
                return False
            elif not self.check_diagonal_up_right(row, col) and self.check_diagonal_down_of_up_right(row, col) and ( row == tpl[0] - 1 and ( col == tpl[1] or col == tpl[1] + 1)):
                return False
            elif self.check_diagonal_up_right(tpl[0], tpl[1]) and (row == tpl[0] or col == tpl[1]):
                return False
            elif self.check_diagonal_up_right(tpl[0], tpl[1]) and self.check_diagonal_up_right(row, col):
                return False
        return True
    
    def check_invalid_vision_down_left(self, row, col):
        if len(self.invalid_vision_down_left) == 0:
            return True

        for tpl in self.invalid_vision_down_left:
            if not self.check_diagonal_down_left(row, col) and not self.check_diagonal_down_of_down_left(row, col) and ( col == tpl[1] - 1 and ( row == tpl[0] or row == tpl[0] + 1)):
                return False
            elif not self.check_diagonal_down_left(row, col) and self.check_diagonal_down_of_down_left(row, col) and ( row == tpl[0] + 1 and ( col == tpl[1] or col == tpl[1] - 1)):
                return False
            elif self.check_diagonal_down_left(tpl[0], tpl[1]) and (row == tpl[0] or col == tpl[1]):
                return False
            elif self.check_diagonal_down_left(tpl[0], tpl[1]) and self.check_diagonal_down_left(row, col):
                return False
        return True
    
    def check_invalid_vision_down_right(self, row, col):
        if len(self.invalid_vision_down_right) == 0:
            return True

        for tpl in self.invalid_vision_down_right:
            if not self.check_diagonal_down_right(row, col) and self.check_diagonal_down_of_down_right(row, col) and ( col == tpl[1] + 1 and ( row == tpl[0] or row == tpl[0] + 1)):
                return False
            elif not self.check_diagonal_down_right(row, col) and not self.check_diagonal_down_of_down_right(row, col) and ( row == tpl[0] + 1 and ( col == tpl[1] or col == tpl[1] + 1)):
                return False
            elif self.check_diagonal_down_right(tpl[0], tpl[1]) and (row == tpl[0] or col == tpl[1]):
                return False
            elif self.check_diagonal_down_right(tpl[0], tpl[1]) and self.check_diagonal_down_right(row, col):
                return False
        return True

    def check_vision_left(self):
        for i in range(1, self.vision_radius + 1):
            if self.position[1] - i >= 0 and self.map[self.position[0]][self.position[1] - i] == 0:
                self.valid_vision_left.append((self.position[0], self.position[1] - i))
            else:
                return
    
    def check_vision_right(self):
        for i in range (1, self.vision_radius + 1):
            if self.position[1] + i < self.bound[1] and self.map[self.position[0]][self.position[1] + i] == 0:
                self.valid_vision_right.append((self.position[0], self.position[1] + i))
            else:
                return

    def check_vision_up(self):
        for i in range(1, self.vision_radius + 1):
            if self.position[0] - i >= 0 and self.map[self.position[0] - i][self.position[1]] == 0:
                self.valid_vision_up.append((self.position[0] - i, self.position[1]))
            else:
                return
    
    def check_vision_down(self):
        for i in range (1, self.vision_radius + 1):
            if self.position[0] + i < self.bound[0] and self.map[self.position[0] + i][self.position[1]] == 0:
                self.valid_vision_down.append((self.position[0] + i, self.position[1]))
            else:
                return
    
    def check_vision_up_left(self):
        for row in range (1, self.vision_radius + 1):
            for col in range (1, self.vision_radius + 1):
                if self.position[0] - row >= 0 and self.position[1] - col >= 0 and self.check_invalid_vision_up_left(self.position[0] - row, self.position[1] - col) and self.map[self.position[0] - row][self.position[1] - col] == 0:
                    self.valid_vision_up_left.append((self.position[0] - row, self.position[1] - col))
                elif self.position[0] - row >= 0 and self.position[1] - col >= 0:
                    self.invalid_vision_up_left.append((self.position[0] - row, self.position[1] - col))

    def check_vision_up_right(self):
        for row in range (1, self.vision_radius + 1):
            for col in range (1, self.vision_radius + 1):
                if self.position[0] - row >= 0 and self.position[1] + col < self.bound[1] and self.check_invalid_vision_up_right(self.position[0] - row, self.position[1] + col) and self.map[self.position[0] - row][self.position[1] + col] == 0:
                    self.valid_vision_up_right.append((self.position[0] - row, self.position[1] + col))
                elif self.position[0] - row >= 0 and self.position[1] + col < self.bound[1]:
                    self.invalid_vision_up_right.append((self.position[0] - row, self.position[1] + col))

    def check_vision_down_left(self):
        for row in range (1, self.vision_radius + 1):
            for col in range (1, self.vision_radius + 1):
                if self.position[0] + row < self.bound[0] and self.position[1] - col >= 0 and self.check_invalid_vision_down_left(self.position[0] + row, self.position[1] - col) and self.map[self.position[0] + row][self.position[1] - col] == 0:
                    self.valid_vision_down_left.append((self.position[0] + row, self.position[1] - col))
                elif self.position[0] + row < self.bound[0] and self.position[1] - col >= 0:
                    self.invalid_vision_down_left.append((self.position[0] + row, self.position[1] - col))

    def check_vision_down_right(self):
        for row in range (1, self.vision_radius + 1):
            for col in range (1, self.vision_radius + 1):
                if self.position[0] + row < self.bound[0] and self.position[1] + col < self.bound[1] and self.check_invalid_vision_down_right(self.position[0] + row, self.position[1] + col) and self.map[self.position[0] + row][self.position[1] + col] == 0:
                    self.valid_vision_down_right.append((self.position[0] + row, self.position[1] + col))
                elif self.position[0] + row < self.bound[0] and self.position[1] + col < self.bound[1]:
                    self.invalid_vision_down_right.append((self.position[0] + row, self.position[1] + col))

    def agent_valid_vision(self):
        self.check_vision_left()
        self.check_vision_right()
        self.check_vision_up()
        self.check_vision_down()

        self.check_vision_up_left()
        self.check_vision_up_right()
        self.check_vision_down_left()
        self.check_vision_down_right()


class Hider(Agent):
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
'''
seeker1 = Agent(current_map.seeker_position[0], 3, (current_map.num_rows, current_map.num_cols), current_map.map_array)
print(seeker1.position)
seeker1.agent_valid_vision()
print(seeker1.invalid_vision_up_left)
print(seeker1.valid_vision_up_left)
print(seeker1.invalid_vision_down_right)
print(seeker1.valid_vision_down_right)
'''


for i in range(len(current_map.hider_position)):
  hider = Hider(current_map.hider_position[i], 3, (current_map.num_rows, current_map.num_cols), current_map.map_array)
  hider.announce(5)
  for row in current_map.map_array:
      print(row)

  print()