import pygame
from pygame.sprite import Sprite

class Environment(Sprite):
	def __init__(self, clock_world_game):
		super().__init__()

		self.screen = clock_world_game.screen
		self.screen_rect = clock_world_game.screen.get_rect()

		# Land
		self.img_land = pygame.image.load('images/environment/land.png').convert_alpha()
		self.img_land_rect = self.img_land.get_rect()

		# Sky
		self.img_sky = pygame.image.load('images/environment/sky.png').convert_alpha()
		self.img_sky = pygame.transform.scale(self.img_sky, (1366, 768))
		self.img_sky_rect = self.img_land.get_rect()

		self.img_sky2 = pygame.image.load('images/environment/sky 2.png').convert_alpha()
		self.img_sky2 = pygame.transform.scale(self.img_sky2, (1366, 768))
		self.img_sky2_rect = self.img_land.get_rect()

		self.img_sky_rect.x = 0
		self.img_sky2_rect.x = 1365
	

	def blit_land(self):
		self.screen.blit(self.img_land, (-120, 730))
		self.screen.blit(self.img_land, (260, 730))
		self.screen.blit(self.img_land, (600, 730))
		self.screen.blit(self.img_land, (900, 730))

	def blit_sky(self):
		self.screen.blit(self.img_sky, (self.img_sky_rect.x, 0))
		self.screen.blit(self.img_sky2, (self.img_sky2_rect.x, 0))

		self.img_sky_rect.x -= 1
		self.img_sky2_rect.x -= 1

		# Animate weather
		if self.img_sky_rect.x < -1365:
			self.img_sky_rect.x = 1365

		elif self.img_sky2_rect.x < -1365:
			self.img_sky2_rect.x = 1365