from backend import *
from screens import menu_screen, Button
import pygame

ANNOUNCE_RANGE = 3
SEEKER_VISION_RADIUS = 3
HIDER_VISION_RADIUS = 2

INFO_BAR = 70
HEIGHT = 500
WIDTH = None
HEIGHT += INFO_BAR
block_edge = None

def setScreen(current_map):
	map_ratio = current_map.num_rows / current_map.num_cols
	WIDTH = HEIGHT / map_ratio
	block_edge = (HEIGHT - INFO_BAR) / current_map.num_rows
	return WIDTH, block_edge

pygame.init()
screen = pygame.display.init()
timer = pygame.time.Clock()
fps = 30
font = pygame.font.Font('freesansbold.ttf', 27)
counter = 0

def getWallImage(block_edge):
	return pygame.transform.scale(pygame.image.load('Assets/wall_images/ice.png'), (block_edge, block_edge))
def getHiderImages(block_edge):
	hider_images = []
	for i in range(1, 5):
		hider_images.append(pygame.transform.scale(pygame.image.load(f'Assets/hider_images/freefire{i}.png'), (block_edge, block_edge)))
	return hider_images
def getSeekerImages(block_edge):
	seeker_images = []
	for i in range(1, 5):
		seeker_images.append(pygame.transform.scale(pygame.image.load(f'Assets/seeker_images/water{i}.png'), (block_edge, block_edge)))
	return seeker_images
def getObstacleImage(block_edge):
	return pygame.transform.scale(pygame.image.load('Assets/obstacle_images/bush.png'), (block_edge, block_edge))
def getAnnounceImage(block_edge):
	return pygame.transform.scale(pygame.image.load('Assets/announce_images/sparkle.png'), (block_edge, block_edge))

def setImage(block_edge):
	listOfImage = []
	listOfImage.append(getWallImage(block_edge))
	listOfImage.append(getHiderImages(block_edge))
	listOfImage.append(getSeekerImages(block_edge))
	listOfImage.append(getObstacleImage(block_edge))
	listOfImage.append(getAnnounceImage(block_edge))
	return listOfImage

def draw_board(screen, current_map, block_edge, listOfImage):
	for i in range(current_map.num_rows):
		for j in range(current_map.num_cols):
			top = j * block_edge
			left = INFO_BAR + i * block_edge

			pygame.draw.rect(screen, 'pink', (top, left, block_edge, block_edge), 1)

			if current_map.map_array[i][j] == 1:
				screen.blit(listOfImage[0], (top, left))
			if current_map.map_array[i][j] == 2:
				draw_agent(current_map, i, j, False, block_edge, listOfImage)
			if current_map.map_array[i][j] == 3:
				draw_agent(current_map, i, j, True, block_edge, listOfImage)
			if current_map.map_array[i][j] == 4:
				screen.blit(listOfImage[3], (top, left))
			if current_map.map_array[i][j] == 5:
				screen.blit(listOfImage[4], (top, left))
		
def draw_agent(current_map, i, j, isSeeker, block_edge, listOfImage):
	VISION_RADIUS = 0
	VISION_COLOR = 0
	top =  j * block_edge
	left = INFO_BAR + i * block_edge
	if isSeeker == True:
		screen.blit(listOfImage[2][counter // 10], (top, left))
		VISION_RADIUS = SEEKER_VISION_RADIUS
		VISION_COLOR = (0, 128, 255, 64)
	else:
		screen.blit(listOfImage[1][counter // 10], (top, left))
		VISION_RADIUS = HIDER_VISION_RADIUS
		VISION_COLOR = (255, 128, 0, 64)
	#Draw vision
	agent = Agent((i, j), VISION_RADIUS, (current_map.num_rows, current_map.num_cols), current_map)
	agent.find_agent_valid_vision()
	
	for valid in agent.valid_vision:
		top_ = valid[1] * block_edge
		left_ = INFO_BAR + valid[0] * block_edge
		#Blending transparently
		s = pygame.Surface((block_edge, block_edge), pygame.SRCALPHA)
		s.fill(VISION_COLOR)
		screen.blit(s, (top_, left_))

def gamePlay(level, screen, current_map, block_edge, listOfImage):
	global counter
	if level == 1:
		print()
		print("----------------------------------------------------------")
		print("Khoi tao Seeker")
		#Khoi tao seeker
		bound = (current_map.num_rows, current_map.num_cols)
		currentSeeker = Seeker(current_map.seeker_position[0], SEEKER_VISION_RADIUS, bound, current_map)
		#Khoi tao hider
		print("Khoi tao Hider")
		currentHider = Hider(current_map.hider_position[0], HIDER_VISION_RADIUS, bound, current_map)
		#Thuat toan search Hider o day
		seeker_area = getSeekerArea(current_map, currentSeeker)
		while (currentSeeker.hiderNum > 0):
			#Tao ra 1 vi tri ngau nhien, cho Seeker di toi day, (Vi tri nay khong duoc la tuong, obstacles)
			randomPosition = generateNextRandomGoal(current_map, seeker_area)
			seeker_area += 1
			if (seeker_area > 8):
				seeker_area = 1
			print("Random Position Seeker will explore: ", randomPosition)
			print()
			print("----------------------------------------------------------")

			#Search duong di tu Seeker toi vi tri ngau nhien nay
			finalState = a_star(currentSeeker, randomPosition)
			path = trackPath(finalState)
			print("Path to the random position: ")

			#in ra cac step can di tu vi tri cua seeker den vi tri ngau nhien nay
			#for i, state in enumerate(path):
			#    print("Step", i + 1, ": explore", state.currentPosition)

			#Seeker bat dau di chuyen
			for i in range(len(path)):
				timer.tick(fps)
				if counter < 39:
					counter += 1
				else:
					counter = 0

				currentSeeker.updateSeeker(path[i].currentPosition) #cap nhat vi tri cua Seeker sau moi lan di chuyen

				screen.fill((64, 64, 64))
				draw_board(screen, current_map, block_edge, listOfImage)
				for event in pygame.event.get():
					if event.type == pygame.QUIT:
						break
				pygame.display.flip()
				#for row in current_map2.map_array:
				#   print(row)

				#Neu trong luc di ma Hider nam trong vision cua Seeker thi thay doi lo trinh di
				currentSeeker.clear_current_vision()
				currentSeeker.find_agent_valid_vision()
				#print(Seeker.valid_vision)
				hider_pos = isHiderInVision(currentSeeker, current_map)
				if (hider_pos != (-1, -1)): 
				#Search duong di tu Seeker toi vi tri cua Hider khi phat hien
					finalState = a_star(currentSeeker, hider_pos)
					currentSeeker.updateHiderPosition(hider_pos)
					path = trackPath(finalState)
					print("Path to the hider: ")
					for i, state in enumerate(path):
						print("Step", i + 1, ": Go to ", state.currentPosition)
						print("----------------------------------------------------------")
						for i in range(len(path)):
							timer.tick(fps)
							if counter < 39:
								counter += 1
							else:
								counter = 0
							currentSeeker.updateSeeker(path[i].currentPosition)

							screen.fill((64, 64, 64))
							draw_board(screen, current_map, block_edge, listOfImage)
							for event in pygame.event.get():
								if event.type == pygame.QUIT:
									break
							pygame.display.flip()
                    #Sau khi bat duoc hider, giam so luong no xuong 1, neu khong con hider thi end game
					currentSeeker.hiderNum -= 1
                    #currentSeeker.printSeekerMap()
					print("Hider caught")       
					print("End Game")
					break
            #currentSeeker.printSeekerMap()

level_map = []
running = True
while running:
	timer.tick(fps)
	if counter < 39:
		counter += 1
	else:
		counter = 0

	if len(level_map) == 0:
		menu_screen(font, level_map)
		if len(level_map) != 2:
			break
		pygame.display.quit()

	if level_map[0] == 1:
		print()
		print("----------------------------------------------------------")
		print("Khoi tao Map")
		current_map = Map()
		current_map.read_txt_file("Assets/maps/map0.txt")
		current_map.createMap(1)

		WIDTH, block_edge = setScreen(current_map)
		listOfImage = setImage(block_edge)

		screen = pygame.display.set_mode([WIDTH, HEIGHT])
		pygame.display.set_caption("HideAndSeek_Level1_Map0")

		printMap(current_map.map_array)
		print()
		gamePlay(1, screen, current_map, block_edge, listOfImage)
		level_map.clear()

	screen.fill((64, 64, 64))

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

	pygame.display.flip()

pygame.quit()

