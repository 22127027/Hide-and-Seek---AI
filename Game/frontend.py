import backend
import pygame

currentMap = backend.current_map

pygame.init()

INFO_BAR = 70
HEIGHT = 500 + INFO_BAR
WIDTH = 1000

screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption("HideAndSeek")
timer = pygame.time.Clock()
fps = 60
font = pygame.font.Font('freesansbold.ttf', 20)

def draw_board(current_map):
	block_edge = (HEIGHT - INFO_BAR) / current_map.num_rows

	for i in range(current_map.num_rows):
		for j in range(current_map.num_cols):
			pygame.draw.rect(screen, 'red', (j * block_edge, INFO_BAR + i * block_edge, block_edge, block_edge), 1)
			if current_map.map_array[i][j] == 1:
				pygame.draw.circle(screen, 'white', (j * block_edge + block_edge / 2, INFO_BAR + i * block_edge + block_edge / 2), block_edge / 3)


running = True
while running:
	timer.tick(fps)
	screen.fill('black')
	draw_board(currentMap)

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

	pygame.display.flip()

pygame.quit()

