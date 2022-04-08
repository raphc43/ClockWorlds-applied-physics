import pygame, math
from pygame.sprite import Sprite
from pygame.locals import *

#from pygame import collidepoint

class PausedUI(Sprite):
	"""Class to describe game User Interface while paused"""

	def __init__(self, clock_world_game):
		super().__init__()
		self.screen = clock_world_game.screen
		self.screen_rect = clock_world_game.screen.get_rect()

		self.pressed_keys = clock_world_game.pressed_keys

		# Resources for start button
		self.start_button_font = pygame.font.SysFont("candara", 20)
		self.start_button_text = self.start_button_font.render("Press Start", 1, 
			Color("White"))

		# Rect attributes of Start button's container(ellipse)
		self.rect = pygame.Rect(590, 560, 140, 50)

		# Resources for main title
		self.title_font = pygame.font.SysFont("century gothic", 70)
		self.title_text = self.title_font.render("ClockWorlds", 1, 
			Color('Black'))

		# Resources for description
		self.text_font = pygame.font.SysFont("century gothic", 20, italic=True)
		self.text = self.text_font.render("Utilize Retkin's artillery skills to protect " 
			"Earth from aliens", 1, 
			Color('Black'))

		# Resources for game over
		self.image = pygame.image.load(f'images/UI/game over.png')
		#self.rect = self.image.get_rect()
		#self.image = pygame.transform.scale(self.image, (30, 30))

	def render_ui(self):
		"""Method to display UI to screen"""		
		pygame.draw.ellipse(self.screen, Color('Black'), self.rect)

		self.screen.blit(self.start_button_text, (617, 580))

		self.screen.blit(self.title_text, (460, 300))

		self.screen.blit(self.text, (420, 700))

	def blit_game_over(self):
		#pygame.draw.rect(self.screen, (0,0,0), (500, 500, 300, 200))
		self.screen.blit(self.image, (320, 280))
