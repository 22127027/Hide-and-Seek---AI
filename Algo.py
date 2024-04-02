import random
import heapq
from colorama import init, Fore, Style
import copy

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
        # Assume that level is 4
        for obstacle in self.obstacles_position:
            top = obstacle[0]
            left = obstacle[1]
            bottom = obstacle[2]
            right = obstacle[3]
            for i in range(top, bottom + 1):
                for j in range(left, right + 1):
                    self.map_array[i][j] = 4
    
    def updateMap(self, map_array):
        self.map_array = map_array


def printMap(map_array):
    init()
    for row in range(0, len(map_array)):
        for col in range(0, len(map_array[row])):
            if map_array[row][col] == 1:
                print(Fore.YELLOW + str(map_array[row][col]), end = " ")
            #Hider Blue
            elif map_array[row][col] == 2:
                print(Fore.BLUE + str(map_array[row][col]), end = " ")
            #Seeker Red
            elif map_array[row][col] == 3:
                print(Fore.RED + str(map_array[row][col]), end = " ")
            #Obstacle Green 
            elif map_array[row][col] == 4:
                print(Fore.GREEN + str(map_array[row][col]), end = " ")
            #Else White
            else:
                print(Style.RESET_ALL + str(map_array[row][col]), end = " ")
        print()

filename = "test_map.txt"
current_map = Map()
current_map.read_txt_file(filename)

print("Dimensions of the table:", current_map.num_rows, "rows,", current_map.num_cols, "columns")
print("Position of hiders:", current_map.hider_position)
print("Position of seeker:", current_map.seeker_position)
print("Position of obstacles:", current_map.obstacles_position)

printMap(current_map.map_array)
current_map.createMap(1)

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

class Agent:
    #Agent k pass nguyen map vo duoc, Hider store 1 cai map khac vs Seeker
    def __init__(self, position, vision_radius, bound, map):
        self.position = position
        self.vision_radius = vision_radius
        self.bound = bound
        self.score = 0
        self.map_array = map.map_array

        self.directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1 , 1), (-1, -1)] # go right, left, down, up, down_right, down_left, up_right, up_left 
        self.directions_word = ["right", "left", "down", "up", "down_right", "down_left", "up_right", "up_left"]
        self.current_direction = None

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

        self.obstacles_list = []
        # self.load_obstacles()

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
            self.check_vision_in_direction(self.directions_word[i])
        
        for i in range (4, 8):
            self.check_vision_in_diagonal_direction(self.directions_word[i])

    def move(self, direction_index):
        self.position = tuple(map(sum, zip(self.position, self.directions[direction_index])))
        self.current_direction = self.directions_word[direction_index]

    def agent_go_right(self):
        print("Right")
        self.move(0)

    def agent_go_left(self):
        print("Left")
        self.move(1)

    def agent_go_down(self):
        print("Down")
        self.move(2)

    def agent_go_up(self):
        print("Up")
        self.move(3)

    def agent_go_down_right(self):
        print("Down Right")
        self.move(4)

    def agent_go_down_left(self):
        print("Down Left")
        self.move(5)

    def agent_go_up_right(self):
        print("Up Right")
        self.move(6)

    def agent_go_up_left(self):
        print("Up Left")
        self.move(7)
    

    # def load_obstacles(self):
    #     for obstacle_pos in current_map.obstacles_position:
    #         pos = [int(x) for x in obstacle_pos.split()]
    #         obs = Obstacles(pos[0], pos[1], pos[2], pos[3], current_map.obstacles_position.index(obstacle_pos))
    #         self.obstacles_list.append(obs)

    def push(self):
        for obstacle in self.obstacles_list:
            if obstacle.return_top() <= self.position[0] <= obstacle.return_bottom():
                if(self.position[1] - obstacle.return_right() == 1):
                    obstacle.move_left()
                    self.agent_go_left()
                    return True
                elif(self.position[1] - obstacle.return_left() == -1):
                    obstacle.move_right()
                    self.agent_go_right()
                    return True
            elif obstacle.return_left() <= self.position[1] <= obstacle.return_right():
                if(self.position[0] - obstacle.return_bottom() == 1):
                    obstacle.move_up()
                    self.agent_go_up()
                    return True
                elif (self.position[0] - obstacle.return_top() == -1):
                    obstacle.move_down()
                    self.agent_go_down()
                    return True        
        return False

    def pull(self):
        for obstacle in self.obstacles_list:
            if obstacle.return_top() <= self.position[0] <= obstacle.return_bottom():
                if(self.position[1] - obstacle.return_right() == 1):
                    self.agent_go_right()
                    obstacle.move_right()
                    return True
                elif(self.position[1] - obstacle.return_left() == -1):
                    self.agent_go_left()
                    obstacle.move_left()
                    return True
            elif obstacle.return_left() <= self.position[1] <= obstacle.return_right():
                if(self.position[0] - obstacle.return_bottom() == 1):
                    self.agent_go_down()
                    obstacle.move_down()
                    return True
                elif (self.position[0] - obstacle.return_top() == -1):
                    self.agent_go_up()
                    obstacle.move_up()
                    return True
        return False


class Seeker(Agent): 
    def __init__(self, position, vision_radius, bound, map):
        Agent.__init__(self, position, vision_radius, bound, map)
        self.map_array = copy.deepcopy(map.map_array)
        self.hiderNum = len(map.hider_position)
        for i in range (0, len(self.map_array)):
            for j in range (0, len(self.map_array[i])):
                if self.map_array[i][j] == 2:
                    self.map_array[i][j] = 0

    def catch(self, hider_position):
        return self.position == hider_position

    def updatePoint(self, level, hider_position):
        # Catch hider
        if (self.catch(self, hider_position)):
            self.point = 20
        else:
            self.point -= 1
    
    def printSeekerMap(self):
        printMap(self.map_array)
    def updateSeeker(self, position):
        self.map_array[self.position[0]][self.position[1]] = 0
        self.map_array[position[0]][position[1]] = 3
        self.position = position
    def updateHiderPosition(self, position):
        self.map_array[position[0]][position[1]] = 2
    

# class Hider(Agent):
#     def __init__(self, position, vision_radius, bound, map, id=0, score=0):
#         Agent.__init__(self, position, vision_radius, bound, map, id=0, score=0)
#         self.id = 2
#     def unit_range(self):
#         top = self.position[0] - ANNOUNCE_RANGE
#         left = self.position[1] - ANNOUNCE_RANGE
#         bottom = self.position[0] + ANNOUNCE_RANGE
#         right = self.position[1] + ANNOUNCE_RANGE

#         if (self.position[0] - ANNOUNCE_RANGE < 0):
#             index = 1
#             while True:
#                 if (self.position[0] - ANNOUNCE_RANGE + index >= 0):
#                     top = self.position[0] - ANNOUNCE_RANGE + index
#                     break
#                 else: index = index + 1
#         if (self.position[1] - ANNOUNCE_RANGE < 0):
#             index = 1
#             while True:
#                 if (self.position[1] - ANNOUNCE_RANGE + index >= 0):
#                     left = self.position[1] - ANNOUNCE_RANGE + index
#                     break
#                 else: index = index + 1

#         if (self.position[0] + ANNOUNCE_RANGE > current_map.num_rows - 1):
#             index = 1
#             while True:
#                 if (self.position[0] + ANNOUNCE_RANGE - index <= current_map.num_rows - 1):
#                     bottom = self.position[0] + ANNOUNCE_RANGE - index
#                     break
#                 else: index = index + 1

#         if (self.position[1] + ANNOUNCE_RANGE > current_map.num_cols - 1):
#             index = 1
#             while True:
#                 if (self.position[1] + ANNOUNCE_RANGE - index <= current_map.num_rows - 1):
#                     right = self.position[1] + ANNOUNCE_RANGE - index
#                     break
#                 else: index = index + 1


#         matrix_range = []
#         rows = bottom + 1 - top
#         cols = right + 1 - left
#         for i in range(top, bottom + 1):
#             row = []
#             for j in range(left, right + 1):
#                 if (current_map.map_array[i][j] != None):
#                   row.append(current_map.map_array[i][j])
            
#             matrix_range.append(row)

#         return matrix_range, rows, cols, top, left, bottom, right
    
#     def announce(self, seekers_moves):
#         if (seekers_moves == 5):
#             rows = 0
#             cols = 0
#             matrix_range, rows, cols, top, left, bottom, right = self.unit_range()
#             while True:
#                 rand_row_index = random.randint(0, rows - 1)
#                 rand_col_index = random.randint(0, cols - 1)
#                 if (matrix_range[rand_row_index][rand_col_index] == 0):
#                     break
                
#             matrix_range[rand_row_index][rand_col_index] = 5
#             for row in matrix_range:
#                 print(row)
#             print()


#         current_map.map_array[rand_row_index + top][rand_col_index + left] = 5     
#         announce_coordinate = (rand_row_index + top, rand_col_index + left)
        
#         return announce_coordinate


# #ALGORITHM GOES HERE

def trackPath(finalState): #Function to track the path from initial to the goal
    path = []
    currentState = finalState #Backtrack from Goal
    while currentState is not None:
        path.insert(0, currentState)
        currentState = currentState.parent #Backtrack till reaching the root
    return path

def checkGoal(currentState): #Check if the current state is the goal state
    if currentState.currentPosition == currentState.goalPosition:
        return True
    return False

def isHiderInVision(Seeker, Map):
    min_x = max(0, Seeker.position[0] - 3)
    max_x = min(Map.num_rows - 1, Seeker.position[0] + 3)
    min_y = max(0, Seeker.position[1] - 3)
    max_y = min(Map.num_cols - 1, Seeker.position[1] + 3)
    
    # Iterate through the cells within the Seeker's vision range
    for x in range(min_x, max_x + 1):
        for y in range(min_y, max_y + 1):
            if Map.map_array[x][y] == 2:  # Check if Hider is in vision
                print("Hider found at position: ", x, y)
                # Seeker.updateGoal((x, y))
                return True
    return False

# def isHiderAllCaught():
#     if Seeker.position == Hider.position:
#         return True
#     return False

def isAnnouncementHeard(Seeker):
    for i in range(len(Seeker.vision)):
        for j in range(len(Seeker.vision[i])):
            if Seeker.vision[i][j] == 5:
                print("Announcement heard at position: ", i, j)
                return True
    return False

def calculateHeuristic(current, goal):
    return abs(current[0] - goal[0]) + abs(current[1] - goal[1])

def generateNextRandomGoal(Seeker, Map):
    (x, y) = (random.randint(0, Map.num_rows - 1), random.randint(0, Map.num_cols - 1))
    return (x, y)

class SearchState:
    def __init__(self, current_position, goal_position, parent, heuristic, map_array):
        self.currentPosition = current_position 
        self.goalPosition = goal_position
        self.parent = parent
        self.heuristic = heuristic
        self.map_array = map_array
        if parent:
            self.cost = parent.cost + 1 
        else:
            self.cost = 0

    #Priority: Node with lowest "cost + heuristic" in heap will be pop first
    def __lt__(self, other):
        total_self_cost = self.cost + self.heuristic
        total_other_cost = other.cost + other.heuristic
        return  total_self_cost < total_other_cost

    def moveUp(self):
        if self.currentPosition[0] > 0 and self.map_array[self.currentPosition[0] - 1][self.currentPosition[1]] == 0:
            new_position = (self.currentPosition[0] - 1, self.currentPosition[1])
            return SearchState(new_position, self.goalPosition, self, calculateHeuristic(new_position, self.goalPosition), self.map_array)
        else:
            return None
    
    def moveDown(self):
        if self.currentPosition[0] < len(self.map_array) - 1 and self.map_array[self.currentPosition[0] + 1][self.currentPosition[1]] == 0:
            new_position = (self.currentPosition[0] + 1, self.currentPosition[1])
            return SearchState(new_position, self.goalPosition, self, calculateHeuristic(new_position, self.goalPosition), self.map_array)
        else:
            return None

    def moveLeft(self):
        if self.currentPosition[1] > 0 and self.map_array[self.currentPosition[0]][self.currentPosition[1] - 1] == 0:
            new_position = (self.currentPosition[0], self.currentPosition[1] - 1)
            return SearchState(new_position, self.goalPosition, self, calculateHeuristic(new_position, self.goalPosition), self.map_array)
        else:
            return None
    
    def moveRight(self):
        if self.currentPosition[1] < len(self.map_array[0]) - 1 and self.map_array[self.currentPosition[0]][self.currentPosition[1] + 1] == 0:
            new_position = (self.currentPosition[0], self.currentPosition[1] + 1)
            return SearchState(new_position, self.goalPosition, self, calculateHeuristic(new_position, self.goalPosition), self.map_array)
        else:
            return None
    
    def moveUpRight(self):
        if self.currentPosition[0] > 0 and self.currentPosition[1] < len(self.map_array[0]) - 1 and self.map_array[self.currentPosition[0] - 1][self.currentPosition[1] + 1] == 0:
            new_position = (self.currentPosition[0] - 1, self.currentPosition[1] + 1)
            return SearchState(new_position, self.goalPosition, self, calculateHeuristic(new_position, self.goalPosition), self.map_array)
        else:
            return None
    
    def moveUpLeft(self):
        if self.currentPosition[0] > 0 and self.currentPosition[1] > 0 and self.map_array[self.currentPosition[0] - 1][self.currentPosition[1] - 1] == 0:
            new_position = (self.currentPosition[0] - 1, self.currentPosition[1] - 1)
            return SearchState(new_position, self.goalPosition, self, calculateHeuristic(new_position, self.goalPosition), self.map_array)
        else:
            return None
        
    def moveDownRight(self):
        if self.currentPosition[0] < len(self.map_array) - 1 and self.currentPosition[1] < len(self.map_array[0]) - 1 and self.map_array[self.currentPosition[0] + 1][self.currentPosition[1] + 1] == 0:
            new_position = (self.currentPosition[0] + 1, self.currentPosition[1] + 1)
            return SearchState(new_position, self.goalPosition, self, calculateHeuristic(new_position, self.goalPosition), self.map_array)
        else:
            return None
    
    def moveDownLeft(self):
        if self.currentPosition[0] < len(self.map_array) - 1 and self.currentPosition[1] > 0 and self.map_array[self.currentPosition[0] + 1][self.currentPosition[1] - 1] == 0:
            new_position = (self.currentPosition[0] + 1, self.currentPosition[1] - 1)
            return SearchState(new_position, self.goalPosition, self, calculateHeuristic(new_position, self.goalPosition), self.map_array)
        else:
            return None

    def get_successors(self):
        successors = []
        # Generate the successors of the current state in 4 direction (UP, DOWN, LEFT, RIGHT)
        successors.append(self.moveUp())
        successors.append(self.moveDown())
        successors.append(self.moveLeft())
        successors.append(self.moveRight())
        successors.append(self.moveUpRight())
        successors.append(self.moveUpLeft())
        successors.append(self.moveDownRight())
        successors.append(self.moveDownLeft())

        # Remove None values from the list of successors
        successors = [successor for successor in successors if successor is not None]
        return successors


def a_star(Seeker, goalPosition):
    expandedList = set()
    frontier = []
    #Generate the initial state and allocate the heuristic value and push it to the frontier
    # print(type(Seeker.position))
    initialState = SearchState(Seeker.position, goalPosition, None, calculateHeuristic(Seeker.position, goalPosition), Seeker.map_array)

    heapq.heappush(frontier, initialState)
    while frontier:
        currentState = heapq.heappop(frontier) #Pop the state with the lowest cost + heuristic value from the frontier
        if checkGoal(currentState): #Late-goal test
            return currentState
        else:
            expandedList.add(currentState) #After pop, add to the expanded list
            successors = currentState.get_successors() #Generate the successors of the current state
            for successor in successors:
                if successor not in expandedList: #Check whether the successor is in the expanded list previously, if no -> push to frontier
                    heapq.heappush(frontier, successor) #Push the successor to the frontier

# def traceHider(Seeker, Hider):
#     finalState = a_star(Seeker, Hider.position)
#     path = trackPath(finalState)

#MAIN
level = input("Enter the level: ")
if level == "1":
    print()
    print("----------------------------------------------------------")
    print("Test Map 2")
    current_map2 = Map()
    current_map2.read_txt_file("test_map2.txt")
    printMap(current_map2.map_array)
    print()
    print("----------------------------------------------------------")
    bound = (current_map2.num_rows, current_map2.num_cols)
    currentSeeker = Seeker(current_map2.seeker_position[0], 3, bound, current_map2)

    # randomPosition = generateNextRandomGoal(currentSeeker, current_map2)
    randomPosition = (6, 19)
    print("Random Position Seeker will explore: ", randomPosition)
    print()
    print("----------------------------------------------------------")
    finalState = a_star(currentSeeker, randomPosition)
    path = trackPath(finalState)
    print("Path to the random position: ")
    for i, state in enumerate(path):
        print("Step", i + 1, ": explore", state.currentPosition)
    print()
    for i in range(len(path)):
        currentSeeker.updateSeeker(path[i].currentPosition)
        
        print()
        currentSeeker.printSeekerMap()
        if (isHiderInVision(currentSeeker, current_map2)):
            finalState = a_star(currentSeeker, current_map2.hider_position[0])
            print("Update Seeker Map")
            currentSeeker.updateHiderPosition(current_map2.hider_position[0])
            path = trackPath(finalState)
            print("Path to the hider: ")
            for i, state in enumerate(path):
                print("Step", i + 1, ": Go to ", state.currentPosition)
            print("----------------------------------------------------------")
            for i in range(len(path)):
                currentSeeker.updateSeeker(path[i].currentPosition)
                print()
                currentSeeker.printSeekerMap()
            # if (isHiderCaught(currentSeeker, current_map2.hider_position[0])):
            print("Hider caught")
            break
    print("End Game")

if level == "2":
    print()
    print("----------------------------------------------------------")
    print("Test Map 3")
    current_map3 = Map()
    current_map3.read_txt_file("test_map3.txt")
    printMap(current_map3.map_array)
    print()
    print("----------------------------------------------------------")
    print("Seeker Map")
    bound = (current_map3.num_rows, current_map3.num_cols)
    currentSeeker = Seeker(current_map3.seeker_position[0], 3, bound, current_map3)

    # randomPosition = generateNextRandomGoal(currentSeeker, current_map2)
    randomPosition = (6, 19)
    print("Random Position Seeker will explore: ", randomPosition)
    print()
    print("----------------------------------------------------------")
    finalState = a_star(currentSeeker, randomPosition)
    path = trackPath(finalState)
    print("Path to the random position: ")
    for i, state in enumerate(path):
        print("Step", i + 1, ": explore", state.currentPosition)
    print()
    for i in range(len(path)):
        currentSeeker.updateSeeker(path[i].currentPosition)
        print()
        
        if (isHiderInVision(currentSeeker, current_map3)):
            finalState = a_star(currentSeeker, current_map3.hider_position[0])
            print("Update Seeker Map")
            currentSeeker.updateHiderPosition(current_map3.hider_position[0])
            path = trackPath(finalState)
            print("Path to the hider: ")
            for i, state in enumerate(path):
                print("Step", i + 1, ": Go to ", state.currentPosition)
            print("----------------------------------------------------------")
            for i in range(len(path)):
                currentSeeker.updateSeeker(path[i].currentPosition)
                print()
            current_map3.map_array[currentSeeker.position[0]][currentSeeker.position[1]] = 0
            printMap(current_map3.map_array)
            currentSeeker.hiderNum -= 1
            print(currentSeeker.hiderNum)
            print("Hider caught")
            break

    randomPosition = (8, 13)
    finalState = a_star(currentSeeker, randomPosition)
    path = trackPath(finalState)
    print("Path to the random position: ")
    for i, state in enumerate(path):
        print("Step", i + 1, ": explore", state.currentPosition)
    print()
    for i in range(len(path)):
        currentSeeker.updateSeeker(path[i].currentPosition)
        print()
        currentSeeker.printSeekerMap()
        if (isHiderInVision(currentSeeker, current_map3)):
            finalState = a_star(currentSeeker, current_map3.hider_position[1])
            print("Update Seeker Map")
            currentSeeker.updateHiderPosition(current_map3.hider_position[1])
            path = trackPath(finalState)
            print("Path to the hider: ")
            for i, state in enumerate(path):
                print("Step", i + 1, ": Go to ", state.currentPosition)
            print("----------------------------------------------------------")
            for i in range(len(path)):
                currentSeeker.updateSeeker(path[i].currentPosition)
                print()
                currentSeeker.printSeekerMap()
            current_map3.map_array[currentSeeker.position[0]][currentSeeker.position[1]] = 0
            printMap(current_map3.map_array)
            currentSeeker.hiderNum -= 1
            print(currentSeeker.hiderNum)
            print("Hider caught")
            break
    print("End Game")

    # Seeker = Seeker(current_map.seeker_position[0], 3, (current_map.num_rows, current_map.num_cols), current_map.map_array)

    # finalState = a_star(Seeker, generateNextRandomGoal(Seeker, Map))
    # path = trackPath(finalState)
    # for i, state in enumerate(path):
    #     print(f"Step {i+1}:") 
    #     print()