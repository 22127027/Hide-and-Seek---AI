import random
import heapq
from colorama import init, Fore, Style
import copy

ANNOUNCE_RANGE = 3
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
            #Announcement Cyan
            elif map_array[row][col] == 5:
                print(Fore.CYAN + str(map_array[row][col]), end = " ")
            #Else White
            else:
                print(Style.RESET_ALL + str(map_array[row][col]), end = " ")
        print()

class Agent:
    #Agent k pass nguyen map vo duoc, Hider store 1 cai map khac vs Seeker
    def __init__(self, position, vision_radius, bound, map):
        self.position = position
        self.vision_radius = vision_radius
        self.bound = bound
        self.score = 0
        # self.map_array = map.map_array
        self.map = map
        
        self.directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1 , 1), (-1, -1)] # go right, left, down, up, down_right, down_left, up_right, up_left 
        self.directions_word = ["right", "left", "down", "up", "down_right", "down_left", "up_right", "up_left"]
        self.current_direction = None


        self.valid_vision = []

        self.invalid_vision_left = False
        self.invalid_vision_up = False
        self.invalid_vision_down = False
        self.invalid_vision_right = False

        self.invalid_vision_up_left = []
        self.invalid_vision_up_right = []
        self.invalid_vision_down_left = []
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
                if (not self.check_diagonal(row, col, direction) and self.check_diagonal_down(row, col, direction) and (col == tpl_col - 1 and (row == tpl_row or row == tpl_row - 1))) or \
                   (not self.check_diagonal(row, col, direction) and not self.check_diagonal_down(row, col, direction) and (row == tpl_row - 1 and (col == tpl_col or col == tpl_col - 1))) or \
                   (self.check_diagonal(tpl_row, tpl_col, direction) and (row == tpl_row or col == tpl_col)) or \
                   (self.check_diagonal(tpl_row, tpl_col, direction) and self.check_diagonal(row, col, direction)):
                    return False
            elif direction == 'up_right':
                if (not self.check_diagonal(row, col, direction) and not self.check_diagonal_down(row, col, direction) and (col == tpl_col + 1 and (row == tpl_row or row == tpl_row - 1))) or \
                   (not self.check_diagonal(row, col, direction) and self.check_diagonal_down(row, col, direction) and (row == tpl_row - 1 and (col == tpl_col or col == tpl_col + 1))) or \
                   (self.check_diagonal(tpl_row, tpl_col, direction) and (row == tpl_row or col == tpl_col)) or \
                   (self.check_diagonal(tpl_row, tpl_col, direction) and self.check_diagonal(row, col, direction)):
                    return False
            elif direction == 'down_left':
                if (not self.check_diagonal(row, col, direction) and not self.check_diagonal_down(row, col, direction) and (col == tpl_col - 1 and (row == tpl_row or row == tpl_row + 1))) or \
                   (not self.check_diagonal(row, col, direction) and self.check_diagonal_down(row, col, direction) and (row == tpl_row + 1 and (col == tpl_col or col == tpl_col - 1))) or \
                   (self.check_diagonal(tpl_row, tpl_col, direction) and (row == tpl_row or col == tpl_col)) or \
                   (self.check_diagonal(tpl_row, tpl_col, direction) and self.check_diagonal(row, col, direction)):
                    return False
            elif direction == 'down_right':
                if (not self.check_diagonal(row, col, direction) and self.check_diagonal_down(row, col, direction) and (col == tpl_col + 1 and (row == tpl_row or row == tpl_row + 1))) or \
                   (not self.check_diagonal(row, col, direction) and not self.check_diagonal_down(row, col, direction) and (row == tpl_row + 1 and (col == tpl_col or col == tpl_col + 1))) or \
                   (self.check_diagonal(tpl_row, tpl_col, direction) and (row == tpl_row or col == tpl_col)) or \
                   (self.check_diagonal(tpl_row, tpl_col, direction) and self.check_diagonal(row, col, direction)):
                    return False
                    
        return True

    def check_vision_in_diagonal_direction(self, direction):
        for row in range(1, self.vision_radius + 1):
            for col in range(1, self.vision_radius + 1):
                if direction == 'up_left':
                    if self.position[0] - row >= 0 and self.position[1] - col >= 0 and self.check_invalid_vision(self.position[0] - row, self.position[1] - col, direction) and (self.map.map_array[self.position[0] - row][self.position[1] - col] != 1 and self.map.map_array[self.position[0] - row][self.position[1] - col] != 4):
                        self.valid_vision.append((self.position[0] - row, self.position[1] - col))
                    elif self.position[0] - row >= 0 and self.position[1] - col >= 0:
                        self.invalid_vision_up_left.append((self.position[0] - row, self.position[1] - col))

                elif direction == 'up_right':
                    if self.position[0] - row >= 0 and self.position[1] + col < self.bound[1] and self.check_invalid_vision(self.position[0] - row, self.position[1] + col, direction) and (self.map.map_array[self.position[0] - row][self.position[1] + col] != 1 and self.map.map_array[self.position[0] - row][self.position[1] + col] != 4):
                        self.valid_vision.append((self.position[0] - row, self.position[1] + col))
                    elif self.position[0] - row >= 0 and self.position[1] + col < self.bound[1]:
                        self.invalid_vision_up_right.append((self.position[0] - row, self.position[1] + col))

                elif direction == 'down_left':
                    if self.position[0] + row < self.bound[0] and self.position[1] - col >= 0 and self.check_invalid_vision(self.position[0] + row, self.position[1] - col, direction) and (self.map.map_array[self.position[0] + row][self.position[1] - col] != 1 and self.map.map_array[self.position[0] + row][self.position[1] - col] != 4):
                        self.valid_vision.append((self.position[0] + row, self.position[1] - col))
                    elif self.position[0] + row < self.bound[0] and self.position[1] - col >= 0:
                        self.invalid_vision_down_left.append((self.position[0] + row, self.position[1] - col))

                elif direction == 'down_right':
                    if self.position[0] + row < self.bound[0] and self.position[1] + col < self.bound[1] and self.check_invalid_vision(self.position[0] + row, self.position[1] + col, direction) and (self.map.map_array[self.position[0] + row][self.position[1] + col] != 1 and self.map.map_array[self.position[0] + row][self.position[1] + col] != 4):
                        self.valid_vision.append((self.position[0] + row, self.position[1] + col))
                    elif self.position[0] + row < self.bound[0] and self.position[1] + col < self.bound[1]:
                        self.invalid_vision_down_right.append((self.position[0] + row, self.position[1] + col))

    def check_vision_in_direction(self, direction):
        for i in range(1, self.vision_radius + 1):
            if direction == 'left':
                if self.position[1] - i >= 0 and self.map.map_array[self.position[0]][self.position[1] - i] != 1 and self.map.map_array[self.position[0]][self.position[1] - i] != 4 and not self.invalid_vision_left:
                    self.valid_vision.append((self.position[0], self.position[1] - i))
                else:
                    self.invalid_vision_left = True
                    self.invalid_vision_up_left.append((self.position[0], self.position[1] - i))
                    self.invalid_vision_down_left.append((self.position[0], self.position[1] - i))
            elif direction == 'right':
                if self.position[1] + i < self.bound[1] and self.map.map_array[self.position[0]][self.position[1] + i] != 1 and self.map.map_array[self.position[0]][self.position[1] + i] != 4 and not self.invalid_vision_right:
                    self.valid_vision.append((self.position[0], self.position[1] + i))
                else:
                    self.invalid_vision_right = True
                    self.invalid_vision_up_right.append((self.position[0], self.position[1] + i))
                    self.invalid_vision_down_right.append((self.position[0], self.position[1] + i))
            elif direction == 'up':
                if self.position[0] - i >= 0 and self.map.map_array[self.position[0] - i][self.position[1]] != 1 and self.map.map_array[self.position[0] - i][self.position[1]] != 4 and not self.invalid_vision_up:
                    self.valid_vision.append((self.position[0] - i, self.position[1]))
                else:
                    self.invalid_vision_up = True
                    self.invalid_vision_up_left.append((self.position[0] - i, self.position[1]))
                    self.invalid_vision_up_right.append((self.position[0] - i, self.position[1]))
            elif direction == 'down':
                if self.position[0] + i < self.bound[0] and self.map.map_array[self.position[0] + i][self.position[1]] != 1 and self.map.map_array[self.position[0] + i][self.position[1]] != 4 and not self.invalid_vision_down:
                    self.valid_vision.append((self.position[0] + i, self.position[1]))
                else:
                    self.invalid_vision_down = True
                    self.invalid_vision_down_left.append((self.position[0] + i, self.position[1]))
                    self.invalid_vision_down_right.append((self.position[0] + i, self.position[1]))
    
    def clear_current_vision(self):
        self.valid_vision.clear()

        self.invalid_vision_up_left.clear()
        self.invalid_vision_up_right.clear()
        self.invalid_vision_down_left.clear()
        self.invalid_vision_down_right.clear()

    def find_agent_valid_vision(self):
        for i in range (0, 4):
            self.check_vision_in_direction(self.directions_word[i])
        
        for i in range (4, 8):
            self.check_vision_in_diagonal_direction(self.directions_word[i])

    def agent_go_right(self):
        print("Right")
        self.move()

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
        self.hiderNum = len(map.hider_position)
        self.moves = 0

    def catch(self, hider_position):
        return self.position == hider_position

    def updatePoint(self, hider_position):
        # Catch hider
        if (self.catch(hider_position)):
            self.score += 20
        else:
            self.score -= 1
    
    def printSeekerMap(self):
        printMap(self.map_array)

    def updateSeeker(self, position):
        self.map.map_array[self.position[0]][self.position[1]] = 0
        self.map.map_array[position[0]][position[1]] = 3
        self.position = position
        self.moves += 1
        if (self.map.map_array[position[0]][position[1]] == 2):
            self.score += 20
        else:
            self.score -= 1
        
    # def updateHiderPosition(self, position):
    #     self.map.map_array[position[0]][position[1]] = 2
    
    def print_vision(self):
        print (len(self.valid_vision_right))
        for i in range(len(self.valid_vision_left)):
            print("Vision left: ", self.valid_vision_left[i])
        for i in range(len(self.valid_vision_right)):
            print("Vision right: ", self.valid_vision_right[i])
        for i in range(len(self.valid_vision_up)):
            print("Vision up: ", self.valid_vision_up[i])
        for i in range(len(self.valid_vision_down)):
            print("Vision down: ", self.valid_vision_down[i])
        for i in range(len(self.valid_vision_up_left)):
            print("Vision up left: ", self.valid_vision_up_left[i])
        for i in range(len(self.valid_vision_up_right)):
            print("Vision up right: ", self.valid_vision_up_right[i])
        for i in range(len(self.valid_vision_down_left)):
            print("Vision down left: ", self.valid_vision_down_left[i])
        for i in range(len(self.valid_vision_down_right)):
            print("Vision down right: ", self.valid_vision_down_right[i])

class Hider(Agent):
    def __init__(self, position, vision_radius, bound, map):
        Agent.__init__(self, position, vision_radius, bound, map)
        self.id = 2
        self.hiderPotentialList = []
        self.announce_coordinate = ()
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

        if (self.position[0] + ANNOUNCE_RANGE > self.map.num_rows - 1):
            index = 1
            while True:
                if (self.position[0] + ANNOUNCE_RANGE - index <= self.map.num_rows - 1):
                    bottom = self.position[0] + ANNOUNCE_RANGE - index
                    break
                else: index = index + 1

        if (self.position[1] + ANNOUNCE_RANGE > self.map.num_cols - 1):
            index = 1
            while True:
                if (self.position[1] + ANNOUNCE_RANGE - index <= self.map.num_rows - 1):
                    right = self.position[1] + ANNOUNCE_RANGE - index
                    break
                else: index = index + 1


        matrix_range = []
        rows = bottom + 1 - top
        cols = right + 1 - left
        for i in range(top, bottom + 1):
            row = []
            for j in range(left, right + 1):
                if (self.map.map_array[i][j] != None):
                  row.append(self.map.map_array[i][j])
            
            matrix_range.append(row)

        return matrix_range, rows, cols, top, left, bottom, right
    
    def announce(self):
        rows = 0
        cols = 0
        matrix_range, rows, cols, top, left, bottom, right = self.unit_range()
        
        while True:
            rand_row_index = random.randint(0, rows - 1)
            rand_col_index = random.randint(0, cols - 1)
            if (self.map.map_array[rand_row_index + top][rand_col_index + left] == 0):
                self.map.map_array[rand_row_index + top][rand_col_index + left] = 5
                break
            
        # matrix_range[rand_row_index][rand_col_index] = 5

        self.announce_coordinate = (rand_row_index + top, rand_col_index + left)
        self.hiderPotentialList.append(self.announce_coordinate)
        
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

def hiderPosInVision(Seeker, Map):
    for valid in Seeker.valid_vision:
        if Map.map_array[valid[0]][valid[1]] == 2:
            return valid
    return (-1, -1)

def calculateHeuristic(current, goal):
    return abs(current[0] - goal[0]) + abs(current[1] - goal[1])

def generateNextRandomGoal(Map):
    (x, y) = (random.randint(0, Map.num_rows - 1), random.randint(0, Map.num_cols - 1))
    return (x, y)

def announcementPosHeard(Seeker):
    for valid in Seeker.valid_vision:
        if Seeker.map.map_array[valid[0]][valid[1]] == 5:
            return valid
    return (-1, -1)
    
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
    map_arr = copy.deepcopy(Seeker.map.map_array)
    for i in range (0, len(map_arr)):
        for j in range (0, len(map_arr[0])):
            if map_arr[i][j] == 2 or map_arr[i][j] == 5:
                map_arr[i][j] = 0
    
    expandedList = set()
    frontier = []
    #Generate the initial state and allocate the heuristic value and push it to the frontier
    initialState = SearchState(Seeker.position, goalPosition, None, calculateHeuristic(Seeker.position, goalPosition), map_arr)

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

def traceHider(currentSeeker, current_map):
    #Search duong di tu Seeker toi vi tri cua Hider khi phat hien
    finalState = a_star(currentSeeker, current_map.hider_position[0])
  
    path = trackPath(finalState)
    print("Path to the hider: ")
    for i, state in enumerate(path):
        print("Step", i + 1, ": Go to ", state.currentPosition)
    for i in range(len(path)):
        currentSeeker.updateSeeker(path[i].currentPosition)
        currentSeeker.updatePoint(current_map.hider_position[0])
        printMap(currentSeeker.map.map_array)
        print()
        #Sau khi bat duoc hider, giam so luong no xuong 1, neu khong con hider thi end game
    currentSeeker.hiderNum -= 1
    print("1 Hider is caught")    

def generateNextRandomGoal(Map, chosen_area):
    M = len(Map.map_array)    # Number of rows in the map
    N = len(Map.map_array[0]) # Number of columns in the map

    # Define the four areas of the map
    area1 = (0, 0, M//2, N//2)           # Top-left area
    area2 = (0, N//2, M//2, N)           # Top-right area
    area3 = (M//2, N//2, M, N)           # Bottom-right area
    area4 = (M//2, 0, M, N//2)           # Bottom-lelf area

    areas = [area1, area2, area3, area4] # List of areas

    # Check if the chosen_area is valid
    if chosen_area < 1 or chosen_area > 4:
        raise ValueError("Invalid chosen_area. Must be between 1 and 4.")
    
    # Select the specified area
    area = areas[chosen_area - 1]
    
    # Generate random (x, y) coordinates in the selected area
    x = random.randint(area[0], area[2] - 1)
    y = random.randint(area[1], area[3] - 1)
    
    # Check if Map[x][y] is not equal to 1
    while Map.map_array[x][y] == 1 or Map.map_array == 4:
        # Generate new random (x, y) coordinates in the selected area
        x = random.randint(area[0], area[2] - 1)
        y = random.randint(area[1], area[3] - 1)
    
    return (x, y)

#MAIN
level = input("Enter the level: ")
if level == "1":
    print()
    print("----------------------------------------------------------")
    print("Khoi tao Map")
    #Khoi tao map
    current_map2 = Map()
    current_map2.read_txt_file("test_map2.txt")
    printMap(current_map2.map_array)

    print("----------------------------------------------------------")
    print("Khoi tao Seeker")
    #Khoi tao seeker
    bound = (current_map2.num_rows, current_map2.num_cols)
    currentSeeker = Seeker(current_map2.seeker_position[0], 3, bound, current_map2)
    #Khoi tao hider
    print("Khoi tao Hider")
    currentHider = Hider(current_map2.hider_position[0], 3, bound, current_map2)

    print("----------------------------------------------------------")
    print("Game Start")
    #Tim area cua seeker
    M = len(current_map2.map_array)    # Number of rows in the map
    N = len(current_map2.map_array[0]) # Number of columns in the map
    area1 = (0, 0, M//2, N//2)           # Top-left area
    area2 = (0, N//2, M//2, N)           # Top-right area
    area3 = (M//2, 0, M, N//2)           # Bottom-left area
    area4 = (M//2, N//2, M, N)           # Bottom-right area
    areas = [area1, area2, area3, area4] # List of areas
    # Determine the Seeker's current area
    seeker_area = None
    for i, area in enumerate(areas):
        if area[0] <= currentSeeker.position[0] < area[2] and area[1] <= currentSeeker.position[1] < area[3]:
            seeker_area = i + 1
            break
    if seeker_area is None:
        raise ValueError("Seeker's position is not within any area.")
    
    #Thuat toan search Hider o day
    while (currentSeeker.hiderNum > 0):
        #Tao ra 1 vi tri ngau nhien, cho Seeker di toi day, (Vi tri nay khong duoc la tuong, obstacles)
        randomPosition = generateNextRandomGoal(current_map2, seeker_area)
        print("Random Position Seeker will explore: ", randomPosition)
        seeker_area += 1
        if (seeker_area > 4):
            seeker_area = 1

        #Search duong di tu Seeker toi vi tri ngau nhien nay
        finalState = a_star(currentSeeker, randomPosition)
        path = trackPath(finalState)
        print("PATH TO THIS RANDOM POSITION")

        #in ra cac step can di tu vi tri cua seeker den vi tri ngau nhien nay
        for i, state in enumerate(path):
            print("Step", i + 1, ": explore", state.currentPosition)
        
        #Seeker bat dau di chuyen
        print("Seeker is moving...")
        for i in range(len(path)):
            currentSeeker.updateSeeker(path[i].currentPosition) #cap nhat vi tri cua Seeker sau moi lan di chuyen
            currentSeeker.clear_current_vision()
            currentSeeker.find_agent_valid_vision()
            printMap(currentSeeker.map.map_array)
            
            #Annoucement 1st time
            if (currentSeeker.moves == 5):
                currentHider.announce()
            #Neu trong luc di ma Hider nam trong vision cua Seeker thi thay doi lo trinh di
            
            hider_pos = hiderPosInVision(currentSeeker, current_map2)
            announcePos = announcementPosHeard(currentSeeker)

            if (hider_pos != (-1, -1)): 
                print("Hider found at position: ", hider_pos)
                traceHider(currentSeeker, current_map2)
                break

            if announcePos != (-1, -1):
                print("Annoucement found at position: ", announcePos)
                tempFinalState = a_star(currentSeeker, announcePos)
                tempPath = trackPath(tempFinalState)
                print("Path to ANNOUCEMENT: ")
                for i, state in enumerate(tempPath):
                    print("Step", i + 1, ": Go to ", state.currentPosition)
                for i in range(len(tempPath)):
                    currentSeeker.updateSeeker(tempPath[i].currentPosition)
                    currentSeeker.clear_current_vision()
                    currentSeeker.find_agent_valid_vision()
                    
                    printMap(currentSeeker.map.map_array)
                    print()
                    hider_pos = hiderPosInVision(currentSeeker, current_map2)
                    if (hider_pos != (-1, -1)):
                        traceHider(currentSeeker, current_map2)
                        break
                break
        if (currentSeeker.hiderNum == 0):
            break 

    print("End Game")
    print("Score: ", currentSeeker.score)
    print("Total moves: ", currentSeeker.moves)