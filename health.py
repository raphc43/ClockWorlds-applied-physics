import pygame
from pygame.sprite import Sprite

class Heart(Sprite):
	def __init__(self, clock_world_game):
		super().__init__()

		self.screen = clock_world_game.screen
		self.screen_rect = clock_world_game.screen.get_rect()

		# Assigning heart image and rect
		self.image = pygame.image.load(f'images/health/heart.png').convert_alpha()
		self.rect = self.image.get_rect()
		self.image = pygame.transform.scale(self.image, (30, 30))

		# Assigning heart's rect attributes		
		self.rect.x = 577
		self.rect.y = 35

		# Heart sentinel to decide as to how many
		# hearts to blit
		self.heart_sentinel = 5

		self.game_over = False

	def blit_hearts(self):
		if self.heart_sentinel > 0:
			self.screen.blit(self.image, (self.rect.x, self.rect.y))
		if self.heart_sentinel > 1:
			self.screen.blit(self.image, (self.rect.x+30, self.rect.y))
		if self.heart_sentinel > 2:
			self.screen.blit(self.image, (self.rect.x+60, self.rect.y))
		if self.heart_sentinel > 3:
			self.screen.blit(self.image, (self.rect.x+90, self.rect.y))
		if self.heart_sentinel > 4:
			self.screen.blit(self.image, (self.rect.x+120, self.rect.y))

		if self.heart_sentinel < 0:
			self.game_over = True