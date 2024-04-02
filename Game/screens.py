import pygame

class Button():
	def __init__(self, x, y, image, scale, text_input, font, text_topLeft = (0, 0)):
		width = int(image.get_width() * scale)
		height = int(image.get_height() * scale)
		self.image = pygame.transform.scale(image, (width, height))

		self.rect = self.image.get_rect()
		self.rect.topleft = (x, y)
		self.clicked = False

		self.font = font
		self.text_input = text_input
		if len(self.text_input) != 0:
			self.text = self.font.render(self.text_input, True, "white")
			self.text_rect = self.text.get_rect()
			self.text_rect.topleft = (0, 0)
			if (text_topLeft == (0, 0)):
				self.text_rect.topleft = (x + width / 3, y + height / 3)
			else:
				self.text_rect.topleft = text_topLeft

	def draw(self, screen):
		isClicked = False
		pos = pygame.mouse.get_pos()

		if len(self.text_input) == 0:
			if self.rect.collidepoint(pos):
				if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
					self.clicked = True
					isClicked = True
		else:
			if self.text_rect.collidepoint(pos):
				self.text = self.font.render(self.text_input, True, "green")
				if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
					self.clicked = True
					isClicked = True
			else:
				self.text = self.font.render(self.text_input, True, "white")

		if pygame.mouse.get_pressed()[0] == 0:
			self.clicked = False

		screen.blit(self.image, (self.rect.x, self.rect.y))
		if len(self.text_input) != 0:
			screen.blit(self.text, (self.text_rect.x, self.text_rect.y))

		return isClicked

def menu_screen(font):
	HEIGHT = 400
	WIDTH = 800

	background_image = pygame.transform.scale(pygame.image.load('Assets/background_images/background1.png'), (WIDTH, HEIGHT))
	button_image = pygame.image.load('Assets/button_images/button3.png')

	screen = pygame.display.set_mode((WIDTH, HEIGHT))
	pygame.display.set_caption('Menu')

	text = font.render("Welcome to Hide and Seek game", True, "blue")

	start_button = Button(480, 150, button_image, 0.08, 'PLAY', font)
	exit_button = Button(480, 250, button_image, 0.08, 'EXIT', font)

	running = True
	while running:
		screen.fill((153, 255, 255))
		screen.blit(background_image, (0, 0))
		screen.blit(text, (350, 50))

		if start_button.draw(screen):
			level_choose_screen(screen, font)
		if exit_button.draw(screen):
			running = False

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False

		pygame.display.flip()
	pygame.quit()

def level_choose_screen(screen, font):
	background_image = pygame.transform.scale(pygame.image.load('Assets/background_images/background2.png'), pygame.display.get_window_size())
	button_image = pygame.image.load('Assets/button_images/button3.png')
	x = 150
	y = 100
	level1_button = Button(x, y, button_image, 0.07, 'LEVEL 1', font, (x + 30, y + 23))
	level2_button = Button(x + 200, y, button_image, 0.07, 'LEVEL 2', font, (x + 230, y + 23))
	level3_button = Button(x + 400, y, button_image, 0.07, 'LEVEL 3', font, (x + 430, y + 23))
	level4_button = Button(x + 200, y + 90, button_image, 0.07, 'LEVEL 4', font, (x + 230, y + 113))

	exit_button_image = pygame.image.load('Assets/button_images/button4.png')
	exit_button = Button(0, 300, exit_button_image, 0.5, 'Back', font)

	text = font.render("CHOOSE A LEVEL TO PROCEED", True, "blue")

	running = True
	while running:
		screen.fill((153, 255, 255))
		screen.blit(background_image, (0, 0))
		screen.blit(text, (220, 35))

		if level1_button.draw(screen):
			map_choose_screen(screen, font)
		if level2_button.draw(screen):
			map_choose_screen(screen, font)
		if level3_button.draw(screen):
			map_choose_screen(screen, font)
		if level4_button.draw(screen):
			map_choose_screen(screen, font)
		if exit_button.draw(screen):
			running = False

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False

		pygame.display.flip()

def map_choose_screen(screen, font):
	background_image = pygame.transform.scale(pygame.image.load('Assets/background_images/background3.png'), pygame.display.get_window_size())
	button_image = pygame.image.load('Assets/button_images/button3.png')

	x = 400
	y = 50
	map1_button = Button(x - 200, y, button_image, 0.06, 'Map 1', font, (x - 165, y + 16))
	map2_button = Button(x - 100, y + 70, button_image, 0.06, 'Map 2', font, (x - 65, y + 86))
	map3_button = Button(x, y + 140, button_image, 0.06, 'Map 3', font, (x + 35, y + 156))
	map4_button = Button(x + 100, y + 210, button_image, 0.06, 'Map 4', font, (x + 135, y + 226))
	map5_button = Button(x + 200, y + 280, button_image, 0.06, 'Map 5', font, (x + 235, y + 296))

	exit_button_image = pygame.image.load('Assets/button_images/button5.png')
	exit_button = Button(0, 320, exit_button_image, 0.1, '', font)

	text = font.render("CHOOSE A MAP TO PROCEED", True, "blue")

	running = True
	while running:
		screen.fill((153, 255, 255))
		screen.blit(background_image, (0, 0))
		screen.blit(text, (50, 10))

		if map1_button.draw(screen):
			print('clicked')
		if map2_button.draw(screen):
			print('clicked')
		if map3_button.draw(screen):
			print('clicked')
		if map4_button.draw(screen):
			print('clicked')
		if map5_button.draw(screen):
			print('clicked')
		if exit_button.draw(screen):
			running = False


		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False

		pygame.display.flip()

pygame.init()
menu_screen(pygame.font.Font('freesansbold.ttf', 27))




