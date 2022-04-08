import pygame, math
from pygame.sprite import Sprite
from cannon import Cannon

class Character(Sprite):
	def __init__(self, clock_world_game):
		super().__init__()

		self.screen = clock_world_game.screen
		self.screen_rect = clock_world_game.screen.get_rect()

		self.pressed_keys = clock_world_game.pressed_keys
		self.acceleration = clock_world_game.acceleration
		self.cannon_operator_mode = clock_world_game.cannon.cannon_operator_mode
		self.direction_indicator = clock_world_game.direction_indicator

		
		self.img = pygame.image.load('images/character/static 1.png').convert_alpha()

		#self.img = pygame.transform.scale(self.img, (80, 80))
		self.img_rect = self.img.get_rect()

		self.img_rect.midbottom = self.screen_rect.midbottom
		# Store a decimal value for the Character's horizontal position.
		self.x = float(self.img_rect.x)
		self.y = float(self.img_rect.y)

		# Resources for character animation
		self.static_picture = self.img
		self.static_picture_loop = 0
		self.static_pic_change_loop = 0

		self.running_picture = self.img
		self.running_picture_loop = 0
		self.running_picture_change_loop = 0

		# Cannon operator mode poses
		self.static_cannon_pose = pygame.image.load('images/character/static cannon pose.png').convert_alpha()
		self.static_cannon_pose = pygame.transform.scale(self.static_cannon_pose, (80, 120))

		self.launch_character = pygame.image.load('images/character/launch character.png').convert_alpha()
		self.launch_character = pygame.transform.scale(self.launch_character, (100, 120))


	def _right_movement(self):
		'''Method to define right movement'''
		if self.pressed_keys['shift']:
			self.acceleration += 9
			''' The derivative of 1.1**x equals 0.09 * 1.1 ** (x or self.acceleration)'''
			self.x += 0.09 * 1.1 ** self.acceleration
			return True

		elif self.acceleration <= 0:
			self.x += 3.5
			return True
		
		elif self.acceleration > 0:
			self.acceleration -= 9
			self.x += 0.09 * 1.1 ** self.acceleration
			return True

	def _left_movement(self):
		'''Method to define left movement'''
		if self.pressed_keys['shift']:
			self.acceleration += 9
			self.x -= 0.09 * 1.1 ** self.acceleration
			return True

		elif self.acceleration <= 0:
			self.x -= 3.5
			return True
		
		elif self.acceleration > 0:
			self.acceleration -= 9
			self.x -= 0.09 * 1.1 ** self.acceleration
			return True

	def character_movement(self, cannon_operator_mode, launch_character_mode):
		'''Method to define and apply the overall movements of the character'''

		if not cannon_operator_mode:
			# The following will only execute if 'COM' is set false

			# Right and Left movement
			if self.pressed_keys['right'] and self.img_rect.right < self.screen_rect.right:
				self._right_movement()										

			if self.pressed_keys['left'] and self.img_rect.left > 0:
				self._left_movement()
			
			# Acceleration limiter
			if self.acceleration > 40:
				self.acceleration = 40
			elif self.acceleration < 0:
				self.acceleration = 0

			self._character_animation()


		# Code to decide and assign suitable pictures
		if cannon_operator_mode and launch_character_mode:
			self.img = self.launch_character
		elif cannon_operator_mode:
			self.img = self.static_cannon_pose

		else:
			if self.pressed_keys['right'] or self.pressed_keys['left']:
				self.img = self.running_picture
			#elif self.acceleration>0: 
				#self.img = self.running_picture
			else:
				self.img = self.static_picture

		# Updating img_rect.x and y(to affect co-ordinates)
		self.img_rect.x = self.x
		self.img_rect.y = self.y


	def _character_animation(self):
		if self.static_picture_loop == 3:
			self.static_picture_loop = 1

		elif self.static_pic_change_loop == 45:
			self.static_picture_loop += 1
			self.static_pic_change_loop = 0

			if self.direction_indicator['left']:
				self.static_picture = pygame.image.load(f'images/character/left static {str(self.static_picture_loop)}.png').convert_alpha()
			else:
				self.static_picture = pygame.image.load(f'images/character/static {str(self.static_picture_loop)}.png').convert_alpha()
		else:
			self.static_pic_change_loop += 0.5


		if self.running_picture_loop == 8:
			self.running_picture_loop = 1

		# Faster Animation for accelerated motion
		elif self.running_picture_change_loop == 3 and self.pressed_keys['shift']:
			self.running_picture_loop += 1
			self.running_picture_change_loop = 0

			if self.pressed_keys['left']:
				self.running_picture = pygame.image.load(f'images/character/left running {str(self.running_picture_loop)}.png').convert_alpha()
			else:
				self.running_picture = pygame.image.load(f'images/character/running {str(self.running_picture_loop)}.png').convert_alpha()

		# Normal Animation for constant motion
		elif self.running_picture_change_loop == 7:
			self.running_picture_loop += 1
			self.running_picture_change_loop = 0

			if self.pressed_keys['left']:
				self.running_picture = pygame.image.load(f'images/character/left running {str(self.running_picture_loop)}.png').convert_alpha()
			else:
				self.running_picture = pygame.image.load(f'images/character/running {str(self.running_picture_loop)}.png').convert_alpha()	
		else:
			self.running_picture_change_loop += 0.5


	def blit_character(self, cannon_operator_mode, static_cannon_x, static_cannon_y):
		if not cannon_operator_mode:
			self.screen.blit(self.img, (self.img_rect.x, self.img_rect.y))
		else:
			self.screen.blit(self.img, (static_cannon_x-30, static_cannon_y+20))