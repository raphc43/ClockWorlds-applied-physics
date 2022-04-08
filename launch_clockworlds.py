import pygame, sys, time
from pygame.locals import *

from paused_ui import PausedUI
from character import Character
from environment import Environment
from enemy_ships import EnemyShip, Explosion
from cannon import Cannon
from health import Heart
from pygame.sprite import Group
import random

class ClockWorld:
	'''Main class of ClockWorld'''
	def __init__(self):	
		pygame.init()	
		pygame.display.set_caption('Clock World')
		pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

		self.screen = pygame.display.get_surface()


		
		#------------------------------------------------------------------------------
		self.pressed_keys = {'right': False, 'left': False, 'up': False, 'down': False,
                'shift': False, 'e': False, 'q': False, 'lctrl': False, 
                'rctrl': False, 'r': False, 'tab': False, 'z': False, 
                'alt': False,'space': False}

		self.direction_indicator = {'right': True, 'left': False, 'up': False} # Default value
		self.acceleration = 0

		# Game Level and ship fleet
		self.level = 1
		self.ship_fleet = 3

		self.game_pause = True
		# Instantiating objects
		self.ui = PausedUI(self)
		self.cannon = Cannon(self)
		self.character = Character(self)
		self.environment = Environment(self)
		self.hearts = Heart(self)

		self.explosion = None
		self.ship = None

		# Creating parallel groups

		# Our intention here is to utilize these groups in a parallel way
		# to render explosions at specified collided points.
		# The logic utilized here is very similar to of parallel arrays		
		self.explosions = Group()
		self.enemy_ships = Group()	

		self.ship_picture_level = 1
		self.ship_speed = 2

		# Generating ships
		for i in range(self.ship_fleet):
			self.ship = EnemyShip(self, 
						pygame.image.load(f'images/ships/enemy ship {self.ship_picture_level}.png').convert_alpha(), 
						self.ship_speed)

			self.ship.rect.y = random.randrange(100, 600)
			self.ship.rect.x = random.randrange(1200, 1500)
			self.enemy_ships.add(self.ship)

			

		# Background music
		self.main_music = pygame.mixer.Sound('audios/Imagine Dragons - Whatever it takes.mp3')

        #------------------------------------------------------------------------------	
		self.main_font = pygame.font.SysFont("calibri", 24)
		self.score = 0
		self.score_text = self.main_font.render(f"Score: {self.score}", 1, (0,0,0)) 
		self.level_text = self.main_font.render(f"Level: {self.level}", 1, (0,0,0)) 
		#------------------------------------------------------------------------------

		# Boolean variable to prevent the while loop from
		# infinitely re-starting the music
		self.music_start = True

		pygame.display.flip()


	def key_down_events(self, event):
		if event.key == K_ESCAPE:
			pygame.quit()
			sys.exit()

		if event.key == K_RETURN and self.game_pause:
			# We want to stop the music after pressing enter key	
			pygame.mixer.Channel(2).stop()

			self.game_pause = False		

		if event.key == K_RETURN and self.hearts.game_over:
			self.hearts.game_over = False
			self.hearts.heart_sentinel = 5
			self.level = 0
			self.ship_picture_level = 1
			self.ship_speed = 2
			self.ship_fleet = 3
			self.score = 0
			self.enemy_ships.empty()

		if not self.hearts.game_over:
			if event.key == K_RIGHT:
				self.pressed_keys['right'] = True
				self.direction_indicator['right'] = True
				self.direction_indicator['left'] = False

			elif event.key == K_LEFT:
				self.pressed_keys['left'] = True
				self.direction_indicator['left'] = True
				self.direction_indicator['right'] = False

			elif event.key == K_LSHIFT:
				self.pressed_keys['shift'] = True

			elif event.key == K_SPACE:
				self.pressed_keys['space'] = True
				self.direction_indicator['up'] = True

			elif event.key == K_e:
				self.pressed_keys['e'] = True

			elif event.key == K_q:
				self.pressed_keys['q'] = True			

	
			elif event.key == K_LCTRL:
				self.pressed_keys['lctrl'] = True	

			elif event.key == K_RCTRL:
				self.pressed_keys['rctrl'] = True	

			elif self.pressed_keys['r'] == False and event.key == K_r:
				self.pressed_keys['r'] = True

			elif self.pressed_keys['r'] and event.key == K_r:
				self.pressed_keys['r'] = False

			elif event.key == K_TAB and not self.cannon.ball_appear:
				if self.cannon.f_init_velocity > 0:
					self.pressed_keys['tab'] = True
					self.cannon.recoil_back = True

		
			elif not self.pressed_keys['alt'] and event.key == K_LALT:
				if self.character.img_rect.x > 60 and self.character.img_rect.x < 100:
					self.pressed_keys['alt'] = True
			

			elif self.pressed_keys['alt'] and event.key == K_LALT:
				self.pressed_keys['alt'] = False
				

	def key_up_events(self, event):
		if event.key == K_RIGHT:
			self.pressed_keys['right'] = False
		elif event.key == K_LEFT:					
			self.pressed_keys['left'] = False

		elif event.key == K_LSHIFT:
			self.pressed_keys['shift'] = False

		elif event.key == K_e:
			self.pressed_keys['e'] = False

		elif event.key == K_q:
			self.pressed_keys['q'] = False	
				
		elif event.key == K_LCTRL:
			self.pressed_keys['lctrl'] = False

		elif event.key == K_RCTRL:
			self.pressed_keys['rctrl'] = False
			
	def check_events(self):
			#pygame.quit()
			#sys.exit()

		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			else:
				if event.type == KEYDOWN:
					self.key_down_events(event)  
				elif event.type == KEYUP:
					self.key_up_events(event)

		self.character.character_movement(self.cannon.cannon_operator_mode,
			self.cannon.launch_character_mode)

		self.cannon.cannon_action()
	
	def update_ships(self):
		# Loop to increment/change ships positions.
		for ship in self.enemy_ships.sprites():
			ship.enemy_ship_movement()
			ship.detect_collisions(self.cannon.cannon_ball_rect)
			ship.detect_wall_hit()
			if ship.deplete_heart_sentinel:
				self.hearts.heart_sentinel -= 1
				self.enemy_ships.remove(ship)

			elif not ship.ship_appear:
				self.enemy_ships.remove(ship)

				# Updating score
				self.score += 10
				self.score_text = self.main_font.render(f"Score: {self.score}", 1, (0,0,0)) 

				# Passing rect attributes of enemy ship
				self.explosion = Explosion(self)
				self.explosion.rect.x = ship.rect.x
				self.explosion.rect.y = ship.rect.y
				self.explosions.add(self.explosion)


	def update_explosions(self):
		"""Loop to change and remove explosion pictures"""
		for explosion in self.explosions.sprites():
			explosion.blit_explosions()

			if explosion.explosion_change_picture == 0:
				self.explosions.remove(explosion)

	def level_up(self):
		# Block to level up
		if not self.enemy_ships:
			self.level += 1
			self.level_text = self.main_font.render(f"Level: {self.level}", 1, (0,0,0))

			self.ship_fleet += 1

			# If current game level is divisible by 6 and if 
			# a ship picture is available then we increment speed and picture
			# to the change ship with attributes
			if (self.level % 6) == 0 and self.ship_picture_level < 8:
				self.ship_picture_level += 1 
				self.ship_speed += 1	

			# Generating ships for new level
			for i in range(self.ship_fleet):						

				self.ship = EnemyShip(self, 
					pygame.image.load(f'images/ships/enemy ship {self.ship_picture_level}.png').convert_alpha(), 
					self.ship_speed)
				self.ship.rect.y = random.randrange(100, 550)
				self.ship.rect.x = random.randrange(1200, 1700+self.level)
				self.enemy_ships.add(self.ship)


	def run_game(self):	
		while True:				
			self.check_events()	
			if not self.game_pause:			
				if not self.hearts.game_over:	
					# The worst case time complexity of both the methods combin
					# is linear i.e O(n + n) = O(2n), which is fair enough		
					
					self.update_ships()
					self.update_explosions()

				self.environment.blit_sky()
				self.environment.blit_land()
				self.cannon.blit_cannon()
				self.character.blit_character(self.cannon.cannon_operator_mode, self.cannon.static_cannon_x, 
					self.cannon.static_cannon_y)			

				if not self.hearts.game_over:			
					self.enemy_ships.draw(self.screen)
					self.explosions.draw(self.screen)
			
				self.screen.blit(self.score_text, (10, 8))
				self.screen.blit(self.level_text, (620, 8))

				self.hearts.blit_hearts()

				# Block to level up
				self.level_up()

			else:
				if self.music_start:
					self.main_music.set_volume(0.8) # Setting music's volume
					pygame.mixer.Channel(2).play(self.main_music) # Playing music through channel selection 
					self.music_start = False # Setting music_start to false

				self.environment.blit_sky()
				self.ui.render_ui()

			if self.hearts.heart_sentinel < 0:
				self.ui.blit_game_over()

			pygame.display.update()


if __name__ == '__main__':
	clock_world = ClockWorld()
	clock_world.run_game()