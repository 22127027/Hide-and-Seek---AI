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
        self.valid_movement = []

    def check_diagonal_up_left(self, row, col):
        for i in range(1, self.vision_radius + 1):
            if ((row == self.position[0] - i and col == self.position[1] - i)):
                return True
        return False
    
    def check_diagonal_down(self, row, col):
        for i in range(1, self.vision_radius + 1):
            if (abs(row -  col) > abs (self.position[0] - self.position[1])):
                return True
        return False
    
    def check_invalid_vision_up_left(self, row, col):
        if len(self.invalid_vision_up_left) == 0:
            return True

        for tpl in self.invalid_vision_up_left:
            if not self.check_diagonal_up_left(row, col) and self.check_diagonal_down(row, col) and ( col == tpl[1] - 1 and ( row == tpl[0] or row == tpl[0] - 1)):
                return False
            elif not self.check_diagonal_up_left(row, col) and not self.check_diagonal_down(row, col) and ( row == tpl[0] - 1 and ( col == tpl[1] or col == tpl[1] - 1)):
                return False
            elif self.check_diagonal_up_left(tpl[0], tpl[1]) and (row == tpl[0] or col == tpl[1]):
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
                else:
                    self.invalid_vision_up_left.append((self.position[0] - row, self.position[1] - col))

    def agent_valid_vision(self):
        self.check_vision_left()
        self.check_vision_right()
        self.check_vision_up()
        self.check_vision_down()
        self.check_vision_up_left()
        

# Usage
filename = "D:/SourceCode/IoAI/Project1/5maps/test_map.txt"
current_map = Map()
current_map.read_txt_file(filename)

'''
print("Dimensions of the table:", current_map.num_rows, "rows,", current_map.num_cols, "columns")
print("Position of hiders:", current_map.hider_position)
print("Position of seeker:", current_map.seeker_position)
print("Position of obstacles:", current_map.obstacles_position)

for row in current_map.map_array:
   print(row)
'''

'''
seeker1 = Agent(current_map.seeker_position[0], 3, (current_map.num_rows, current_map.num_cols), current_map.map_array)
print(seeker1.position)
seeker1.agent_valid_vision()
print(seeker1.valid_vision_left[0])
print(seeker1.valid_vision_up[0])
print(seeker1.invalid_vision_up_left)
print(seeker1.valid_vision_up_left)
'''