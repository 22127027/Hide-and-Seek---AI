import pygame

class Button():
	def __init__(self, x, y, image, scale):
		width = image.get_width()
		height = image.get_height()
		self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
		self.rect = self.image.get_rect()
		self.rect.topleft = (x, y)
		self.clicked = False

	def draw(self, screen):
		isClicked = False
		pos = pygame.mouse.get_pos()

		if self.rect.collidepoint(pos):
			if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
				self.clicked = True
				isClicked = True
		if pygame.mouse.get_pressed()[0] == 0:
			self.clicked = False


		screen.blit(self.image, (self.rect.x, self.rect.y))
		return isClicked

def menu_screen():
	HEIGHT = 500
	WIDTH = 1000

	button_image = pygame.image.load('Assets/button_images/button1.png')

	screen = pygame.display.set_mode((WIDTH, HEIGHT))
	pygame.display.set_caption('Menu')

	button = Button(100, 200, button_image, 0.05)

	running = True
	while running:
		screen.fill((64,64,64))
		if button.draw(screen):
			print('clicked')

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False

		pygame.display.flip()
	pygame.quit()

menu_screen()




