import pygame, math, time
from pygame.sprite import Sprite
from pygame.locals import *

class Cannon(Sprite):
	def __init__(self, clock_world_game):
		super().__init__()
		self.screen = clock_world_game.screen
		self.screen_rect = clock_world_game.screen.get_rect()

		self.pressed_keys = clock_world_game.pressed_keys

		# Resources for cannon
		self.cannon = pygame.image.load('images/cannon/cannon.png').convert_alpha()

		#self.cannon = pygame.transform.scale(self.cannon, (190, 180))
		self.cannon = pygame.transform.rotate(self.cannon, 9)

		# Cannon stand
		self.cannon_stand = pygame.image.load('images/cannon/cannon stand.png').convert_alpha()

		self.cannon_ball = pygame.image.load('images/cannon/cannon ball.png').convert_alpha()

		self.cannon_ball = pygame.transform.scale(self.cannon_ball, (25, 25))
		#self.cannon_ball = pygame.transform.scale(self.cannon_ball, (200, 2))

		self.recoil_loop = 0
		self.recoil_back = False
		self.recoil_mode = False
		

		# Resources of fire
		self.fire_pic = pygame.image.load('images/cannon/fire.png').convert_alpha()
		self.fire_pic = pygame.transform.scale(self.fire_pic, (130, 60))
		self.fire_pic = pygame.transform.rotate(self.fire_pic, 6)

		self.fire = False
		self.fire_sound_loop = 0
		self.fire_sound_active = False
		self.fire_loop = 0

		
		self.launch_character_loop = 0

		# Resources for special geometrical drawings
		self.degree_circle = pygame.image.load('images/geometry/degree circle.png').convert_alpha()
		self.degree_circle_ball = pygame.transform.scale(self.degree_circle, (70, 50))
		self.degree_circle_real = pygame.transform.scale(self.degree_circle, (50, 30))

		self.angle = 0
		self.radar_len = 200

		# trajectory resources
		self.f_init_velocity = 0
		self.f_x_velocity = 0
		self.f_init_y_velocity = 0
		self.F_INIT_Y_VELOCITY = 0 # Constant intial Y velocity
		self.f_final_y_velocity = 0
		self.f_final_velocity = 0
		self.y_init = 0 # Y co-ordinate itself just before launch
		self.G = 0.9 # Acceleration due to gravity
		self.ball_appear = False

		self.copy_x_velocity = 0
		self.copy_y_velocity = 0

		self.stop_angle_calculation = False

		self.myfont = pygame.font.SysFont("Century Gothic", 20)
		self.angle_font = pygame.font.SysFont("Century Gothic", 13)

		# Resources postion
		# Static cannon because we don't want to move the cannon
		self.static_cannon_x = 100
		self.static_cannon_y = 630

		self.cannon_ball_rect = self.cannon_ball.get_rect()
		self.cannon_ball_rect.x = 0
		self.cannon_ball_rect.y = 0


		self.cannon_operator_mode = False
		self.launch_character_mode = False
		self.fall = False
		self.pause = False

		# Variable to decide when to update cannon ball's co-ordinates
		self.launch_sentinel = 0

		self.store_calculation = False

	def cannon_action(self):
		self._cannon_trajectory_calculation()

		# Code to limit fire picture duration
		if self.fire:
			self.fire_loop += 0.5

		if self.fire_loop == 6:
			self.fire = False
			self.fire_loop = 0

		# Code to limit recoil duration
		self.recoil_loop += 3
	
		if self.recoil_loop == 39 and self.recoil_mode:
			self.static_cannon_x += 45
			self.recoil_mode = False

		elif self.recoil_loop > 40:
			self.recoil_loop = 0

		
    
  	  	# Code to limit launch character duration
		self.launch_character_loop += 0.5

		if self.launch_character_loop > 20:
			self.launch_character_loop = 0

		if self.launch_character_loop == 20 and self.launch_character_mode:
			self.launch_character_mode = False

		#-----------------------------------------------------

		# Line rotation
		if self.pressed_keys['e']:
			self.angle += 3
		elif self.pressed_keys['q']:
			self.angle -= 3

		# Projectile's Charged Velocity
		if self.pressed_keys['lctrl']:
			self.f_init_velocity -= 0.16
			self.radar_len -= 0.8

		if self.pressed_keys['rctrl']:
			self.f_init_velocity += 0.16
			self.radar_len += 0.8

		# Angle limiter
		if self.angle > 0:
			self.angle = 0
		if self.angle < -90:
			self.angle = -90

		# Flight Velocity limiter
		if self.f_init_velocity < 18:
			self.f_init_velocity = 18
			self.radar_len = 200

		elif self.f_init_velocity > 50:
			self.f_init_velocity = 50
			self.radar_len = 12700

		if self.pressed_keys['alt']:
			self.cannon_operator_mode = True
		else:
			self.cannon_operator_mode = False




	def _cannon_trajectory_calculation(self):
		# Trajectory Calculation
		self.radar = (self.static_cannon_x+170, self.static_cannon_y+26)
		self.angle_x = self.radar[0] + math.cos(math.radians(self.angle)) * self.radar_len
		self.angle_y = self.radar[1] + math.sin(math.radians(self.angle)) * self.radar_len

		if self.pressed_keys['r'] and self.f_init_velocity > 0:
			if self.stop_angle_calculation == False:
				self.cannon_ball_rect.x = self.static_cannon_x+170
				self.cannon_ball_rect.y = self.static_cannon_y+42

			if self.angle < 0:
				# Angular or vertical launch 
				self.f_x_velocity = abs(self.f_init_velocity) * math.cos(math.radians(abs(self.angle)))
				self.f_init_y_velocity = abs(self.f_init_velocity) * math.sin(math.radians(abs(self.angle)))
				
			if self.angle == 0:
				# Horizontal launch
				self.f_x_velocity = self.f_init_velocity
				self.f_init_y_velocity = 0

			self._cannon_trajectory_shot()

	def _cannon_trajectory_shot(self):
		if self.cannon_ball_rect.x > self.screen_rect.right:
			self.fall = False			
			self.pressed_keys['tab'] = False
			self.stop_angle_calculation = False
			self.ball_appear = False

			self.store_calculation = False

			self.launch_sentinel = 0
			
		elif self.cannon_ball_rect.y < self.screen_rect.top:
			self.fall = False			
			self.pressed_keys['tab'] = False
			self.stop_angle_calculation = False
			self.ball_appear = False

			self.store_calculation = False

			self.launch_sentinel = 0

		if not self.store_calculation and self.pressed_keys['tab']:
				self.copy_x_velocity = self.f_x_velocity
				self.copy_y_velocity = self.f_init_y_velocity
				self.store_calculation = True

		if self.pressed_keys['tab']:
			self.ball_appear = True
			self.fire_sound_active = True			
			self.stop_angle_calculation = True

			if self.recoil_back:
				self.fire = True
				pygame.mixer.Channel(0).play(pygame.mixer.Sound('audios/explosion.mp3'))
				self.launch_character_mode = True
				self.recoil_mode = True
				self.recoil_back = False
				self.static_cannon_x -= 45

			if self.fall == False:				
				self.launch_sentinel += 1
				if self.launch_sentinel >= 2:
					self.copy_y_velocity -= self.G
					self.cannon_ball_rect.x += self.copy_x_velocity
					self.cannon_ball_rect.y -= self.copy_y_velocity
					self.launch_sentinel = 0
				

				if self.copy_y_velocity <= 0:					
					self.fall = True

			
			if self.fall:
				self.launch_sentinel += 1
				if self.launch_sentinel >= 2:
					self.copy_y_velocity += self.G
					self.cannon_ball_rect.x += self.copy_x_velocity
					self.cannon_ball_rect.y += self.copy_y_velocity
					self.launch_sentinel = 0

				if self.cannon_ball_rect.y >= 730:								
					self.fall = False			
					self.pressed_keys['tab'] = False
					self.stop_angle_calculation = False
					self.ball_appear = False

					self.store_calculation = False

	def blit_cannon(self):
		self.label_1 = self.angle_font.render(f"{abs(round(self.angle, 3))} \N{DEGREE SIGN}", 1, (0,0,0)) 
		self.label_2 = self.angle_font.render(f"v = {round(self.f_init_velocity, 3)} m/s", 1, (0,0,0)) 

		
		if self.cannon_operator_mode == False:
			self.screen.blit(self.cannon, (self.static_cannon_x, self.static_cannon_y))
			self.screen.blit(self.cannon_stand, (self.static_cannon_x, self.static_cannon_y+60))
		else:
			self.screen.blit(self.cannon, (self.static_cannon_x, self.static_cannon_y))
			self.screen.blit(self.cannon_stand, (self.static_cannon_x, self.static_cannon_y+60))
			if self.ball_appear:
				self.screen.blit(self.cannon_ball, (self.cannon_ball_rect.x, self.cannon_ball_rect.y))
			if self.pressed_keys['r']:
				self.screen.blit(self.label_1, (self.static_cannon_x+30, self.static_cannon_y-10))
				self.screen.blit(self.label_2, (self.static_cannon_x+90, self.static_cannon_y+80))

				self.screen.blit(self.degree_circle_real, (self.static_cannon_x+30, self.static_cannon_y-25))
			
				if self.fire:
					self.screen.blit(self.fire_pic, (self.static_cannon_x+220, self.static_cannon_y-20))

			# Angle rendering
			if self.pressed_keys['r']:
				pygame.draw.line(self.screen, Color("black"), self.radar, (self.angle_x, self.angle_y), 1)