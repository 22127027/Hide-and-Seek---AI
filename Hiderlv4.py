class Agent:
  def pull(self, current_map):
        position = self.position
        for obstacle in self.obstacles_list:
            if obstacle.return_top() <= self.position[0] <= obstacle.return_bottom() :
                if (self.position[1] - obstacle.return_right() == 1):
                    while True: 
                        if (self.position[1] == current_map.num_cols - 1 or current_map.map_array[self.position[0]][self.position[1] + 1] != 0):
                            break
                        else:
                            self.agent_go_right()
                            if (obstacle.check_go_right(current_map) == False):
                                self.agent_go_left()
                                break
                            obstacle.move_right(current_map)
                            current_map.map_array = self.map.map_array
                            

                    return True
                
                elif(self.position[1] - obstacle.return_left() == -1):
                    while True: 
                        if (self.position[1] == 0 or current_map.map_array[self.position[0]][self.position[1] - 1] != 0):
                            break
                        else:
                            self.agent_go_left()
                            if (obstacle.check_go_left(current_map) == False):
                                self.agent_go_right()
                                break
                            obstacle.move_left(current_map)
                            current_map.map_array = self.map.map_array

                    return True
            elif obstacle.return_left() <= self.position[1] <= obstacle.return_right():
                if(self.position[0] - obstacle.return_bottom() == 1):
                    while True:
                        if (self.position[0] == current_map.num_rows - 1 or current_map.map_array[self.position[0] + 1][self.position[1]] != 0):
                            break
                        else:
                            self.agent_go_down()
                            if (obstacle.check_go_down(current_map) == False):
                                self.agent_go_up()
                                break
                            obstacle.move_down(current_map)
                            current_map.map_array = self.map.map_array

                    return True
                elif (self.position[0] - obstacle.return_top() == -1):
                    while True:
                        if (self.position[0] == 0 or current_map.map_array[self.position[0] - 1][self.position[1]] != 0):
                            break
                        else:
                            self.agent_go_up()
                            if (obstacle.check_go_down(current_map) == False):
                                self.agent_go_down()
                                break
                            obstacle.move_up(current_map)
                            current_map.map_array = self.map.map_array

                    return True
                
        
        return False
  

class Hider(Agent):
    def __init__(self, position, vision_radius, bound, map, id=0, score=0):
        Agent.__init__(self, position, vision_radius, bound, map, id=0, score=0)
        self.map.map_array = copy.deepcopy(map.map_array)
        for i in range (0, len(self.map.map_array)):
            for j in range (0, len(self.map.map_array[i])):
                if self.map.map_array[i][j] == 3:
                    self.map.map_array[i][j] = 0
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
                if (self.map_array[i][j] != None):
                  row.append(self.map_array[i][j])
            
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


        self.map.map_array[rand_row_index + top][rand_col_index + left] = 5
        announce_coordinate = (rand_row_index + top, rand_col_index + left)
        

        return announce_coordinate
    
    def Move(self, seeker_position):        # Level 3
        neighbors = []
        distances = []
        top = self.position[0] - 1
        bottom = self.position[0] + 1
        left = self.position[1] - 1
        right = self.position[1] + 1
        for i in range(top, bottom + 1):
            for j in range(left, right + 1):
                if (self.position != (i, j)):
                    neighbors.append((i, j))
                    if (top < 0 or left < 0 or bottom > self.bound[0] - 1 or right > self.bound[1] - 1 or self.map[i][j] != 0):
                        distance = -1
                    else:
                        distance = ((seeker_position[0] - i)**2 + (seeker_position[1] - j)**2)**0.5
                    distances.append(distance)

        print(neighbors)
        print(distances)
        index = 0
        for i in range(len(distances)):
            if (distances[i] == max(distances)):
                index = i
                break
        # 0: up-left, 1: up, 2: up-right, 3: left, 4: right, 5: down-left, 6: down, 7: down-right 
        print(index)        
        if (index == 0):
            self.agent_go_up_left()        # Move up left
        elif (index == 1):
            self.agent_go_up()        # Move up
        elif (index == 2):
            self.agent_go_up_right()        # Move up right
        elif (index == 3):
            self.agent_go_left()        # Move left
        elif (index == 4):
            self.agent_go_right()        # Move right
        elif (index == 5):
            self.agent_go_down_left()        # Move down left
        elif (index == 6):
            self.agent_go_down()        # Move down
        elif (index == 7):
            self.agent_go_down_right()        # Move down right

    def printHiderMap(self):
        printMap(self.map_array)

    def findCellsAroundObstacles(self, current_map):
        self.load_obstacles(current_map)
        obstacle = self.obstacles_list[0]
        if (self.position[1] < obstacle.left):
            frontierLeft = []
            minDistance = self.bound[1]
            indexMin = 0
            for i in range(obstacle.top, obstacle.bottom + 1):
                frontierLeft.append(i)
                if (abs(self.position[0] - i) < minDistance):
                    minDistance = abs(self.position[0] - i)
                    indexMin = i

            goalCell = (indexMin, obstacle.left - 1)
            return goalCell
        elif (self.position[1] > obstacle.right):
            frontierRight = []
            minDistance = self.bound[1]
            indexMin = 0
            for i in range(obstacle.top, obstacle.bottom + 1):
                frontierRight.append(i)
                if (abs(self.position[0] - i) < minDistance):
                    minDistance = abs(self.position[0] - i)
                    indexMin = i

            goalCell = (indexMin, obstacle.right + 1)
            return goalCell
    
        elif (obstacle.left <= self.position[1] <= obstacle.right and self.position[0] < obstacle.top):
            frontierTop = []
            minDistance = self.bound[0]
            indexMin = 0
            for i in range(obstacle.left, obstacle.right + 1):
                frontierTop.append(i)
                if (abs(self.position[1] - i) < minDistance):
                    minDistance = abs(self.position[1] - i)
                    indexMin = i

            goalCell = (obstacle.top - 1, indexMin)
            return goalCell
        
        elif (obstacle.left <= self.position[1] <= obstacle.right and self.position[0] > obstacle.top):
            frontierBottom = []
            minDistance = self.bound[0]
            indexMin = 0
            for i in range(obstacle.left, obstacle.right + 1):
                frontierBottom.append(i)
                if (abs(self.position[1] - i) < minDistance):
                    minDistance = abs(self.position[1] - i)
                    indexMin = i

            goalCell = (obstacle.bottom + 1, indexMin)
            return goalCell
        
    def printHiderMap(self):
        printMap(self.map_array)
    def updateHider(self, position):
        self.map.map_array[self.position[0]][self.position[1]] = 0
        self.map.map_array[position[0]][position[1]] = 2
        self.position = position
    #def updateHiderPosition(self, position):
        #self.map_array[position[0]][position[1]] = 2


