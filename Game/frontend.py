from backend import current_map, Agent, Hider
import pygame

ANNOUNCE_RANGE = 3
SEEKER_VISION_RADIUS = 3
map_ratio = current_map.num_rows / current_map.num_cols

INFO_BAR = 70
HEIGHT = 500
WIDTH = HEIGHT / map_ratio
HEIGHT += INFO_BAR

pygame.init()

screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption("HideAndSeek")
timer = pygame.time.Clock()
fps = 60
font = pygame.font.Font('freesansbold.ttf', 20)

def draw_board(current_map):
	block_edge = (HEIGHT - INFO_BAR) / current_map.num_rows

	for i in range(current_map.num_rows):
		for j in range(current_map.num_cols):
			top = j * block_edge
			left = INFO_BAR + i * block_edge

			pygame.draw.rect(screen, 'pink', (top, left, block_edge, block_edge), 1)

			if current_map.map_array[i][j] == 1:
				pygame.draw.circle(screen, 'white', (top + block_edge / 2, left + block_edge / 2), block_edge / 2)
			if current_map.map_array[i][j] == 2:
				oly = block_edge / 8
				#draw star
				star = [
					(top, left + oly * 3),
					(top + oly * 3, left + oly * 3),
					(top + oly * 4, left),
					(top + oly * 5, left + oly * 3),
					(top + oly * 8, left + oly * 3),
					(top + oly * 5.4, left + oly * 4),
					(top + oly * 8, left + oly * 8),
					(top + oly * 4, left + oly * 5),
					(top, left + oly * 8),
					(top + oly * 2.6, left + oly * 4)
				]
				pygame.draw.polygon(screen, (204, 204, 0), star)
			if current_map.map_array[i][j] == 3:
				oly = block_edge / 8
				#draw sun
				pygame.draw.circle(screen, 'red', (top + block_edge / 2, left + block_edge / 2), block_edge / 4)
				pygame.draw.line(screen, 'red', (top, left), (top + oly * 2, left + oly * 2), 2)
				pygame.draw.line(screen, 'red', (top + oly * 4, left), (top + oly * 4, left + oly * 1.5), 2)
				pygame.draw.line(screen, 'red', (top + oly * 8, left), (top + oly * 6, left + oly * 2), 2)
				pygame.draw.line(screen, 'red', (top + oly * 8, left + oly * 4), (top + oly * 6.5, left + oly * 4), 2)
				pygame.draw.line(screen, 'red', (top + oly * 8, left + oly * 8), (top + oly * 6, left + oly * 6), 2)
				pygame.draw.line(screen, 'red', (top + oly * 4, left + oly * 8), (top + oly * 4, left + oly * 6.5), 2)
				pygame.draw.line(screen, 'red', (top, left + oly * 8), (top + oly * 2, left + oly * 6), 2)
				pygame.draw.line(screen, 'red', (top, left + oly * 4), (top + oly * 1.5, left + oly * 4), 2)

				#Draw vision
				seeker = Agent((i, j), SEEKER_VISION_RADIUS, (current_map.num_rows, current_map.num_cols), current_map.map_array)
				seeker.agent_valid_vision()
				listOfValidVision = []
				for valid in seeker.valid_vision_left:
					listOfValidVision.append(valid)
				for valid in seeker.valid_vision_up_left:
					listOfValidVision.append(valid)
				for valid in seeker.valid_vision_up:
					listOfValidVision.append(valid)
				for valid in seeker.valid_vision_up_right:
					listOfValidVision.append(valid)
				for valid in seeker.valid_vision_right:
					listOfValidVision.append(valid)
				for valid in seeker.valid_vision_down_right:
					listOfValidVision.append(valid)
				for valid in seeker.valid_vision_down:
					listOfValidVision.append(valid)
				for valid in seeker.valid_vision_down_left:
					listOfValidVision.append(valid)	
				for valid in listOfValidVision:
					top_ = valid[1] * block_edge
					left_ = INFO_BAR + valid[0] * block_edge
					#Blending transparently
					s = pygame.Surface((block_edge, block_edge), pygame.SRCALPHA)
					s.fill((255, 0, 0, 64))
					screen.blit(s, (top_, left_))

			if current_map.map_array[i][j] == 4:
				pygame.draw.circle(screen, (32, 32, 32), (top + block_edge / 2, left + block_edge / 2), block_edge / 2)
			if current_map.map_array[i][j] == 5:
				pygame.draw.circle(screen, 'blue', (top + block_edge / 2, left + block_edge / 2), block_edge / 3, 1)
				pygame.draw.circle(screen, 'blue', (top + block_edge / 2, left + block_edge / 2), block_edge / 4, 1)
				pygame.draw.circle(screen, 'blue', (top + block_edge / 2, left + block_edge / 2), block_edge / 5, 1)
				pygame.draw.circle(screen, 'blue', (top + block_edge / 2, left + block_edge / 2), block_edge / 6, 1)

				
				
running = True
while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

	timer.tick(fps)
	screen.fill((64, 64, 64))
	draw_board(current_map)

	pygame.display.flip()

pygame.quit()

