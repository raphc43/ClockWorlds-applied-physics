import pygame, random, copy
from pygame.sprite import Sprite

class ConstructEnemyShip():
	"""Base class"""
	def __init__(self, level):
		self.level = level
		self.ship_speed = (self.level + random.randrange(0, 1))	

	# Ship creation method/Factory
	def __call__(self, ship_type):
		return pygame.image.load(f'images/ships/{ship_type}.png').convert_alpha()
		


class EnemyShip(Sprite):	
	def __init__(self, clock_world_game, img, level):
		super().__init__()
		#self.ship_level = ship_level
		self.screen = clock_world_game.screen
		self.screen_rect = clock_world_game.screen.get_rect()
		self.ship_appear = True

		#self.ship = ConstructEnemyShip(1)

		# Assigning ships image
		self.image = img#pygame.image.load(f'images/ships/enemy ship 1.png').convert_alpha()#self.ship('enemy ship 1')
		self.image = pygame.transform.scale(self.image, (90, 90))

		# Assigning ships rect attributes
		self.rect = self.image.get_rect()
		self.rect.x = 0#1000
		self.rect.y = 0
		self.ship_speed = (level + 0.1)	
	
		self.deplete_heart_sentinel = False


	def enemy_ship_movement(self):
		"""Method to define enemy ship movement"""
		if self.ship_appear:
			self.rect.x -= self.ship_speed

	def detect_collisions(self, cannon_ball):
		if self.rect.colliderect(cannon_ball):
			self.ship_appear = False		
			pygame.mixer.Channel(1).play(pygame.mixer.Sound('audios/fire_sound.mp3'))

	def detect_wall_hit(self):
		if self.rect.x < -60:
			self.deplete_heart_sentinel = True
			#if self.rect.colliderect(self.screen_rect.left):


class Explosion(Sprite):
	"""A sprite class to define explosions"""
	def __init__(self, clock_world_game):
		super().__init__()
		#self.ship_level = ship_level
		self.screen = clock_world_game.screen
		self.screen_rect = clock_world_game.screen.get_rect()

		# Explosion
		self.image = pygame.image.load(f"images/explosion/explosion 1.png").convert_alpha()
		# Accumalator to decide when to change picture
		self.explosion_change = 0
		# Accumalator to change actual pictures
		self.explosion_change_picture = 1

		# Setting rect attributes
		self.rect = self.image.get_rect()
		self.rect.x = 0
		self.rect.y = 0

		
	def blit_explosions(self):
		"""Method to blit explosions"""
		if self.explosion_change_picture > 0:
			self.explosion_change += 1

			if self.explosion_change >= 10:				
				self.image = pygame.image.load(f"images/explosion/explosion {self.explosion_change_picture}.png").convert_alpha()			
				self.explosion_change_picture += 1

				# Setting it to zero to initiate another cycle
				self.explosion_change = 0

				if self.explosion_change_picture == 8:
					self.explosion_change_picture = 0			