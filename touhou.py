#import os
#os.environ['SDL_VIDEODRIVER'] = 'windib'

import pygame, sys
from pygame.locals import *

import dekarrin.file.lines

import json
import os

CONFIG_FILE = 'launcher.cfg'

MODE_CONTROL = 0
MODE_VIDEO = 1

MOVIECOMPLETE = USEREVENT + 1

COLOR_WHITE = pygame.Color(255, 255, 255)
COLOR_BLACK = pygame.Color(0, 0, 0)

class TouhouLauncher(object):

	def __init__(self, configuration, video_list, menu_data):
		pygame.init()
		resolution = (configuration['resolution_width'], configuration['resolution_height']);
		self.clock = pygame.time.Clock()
		self.window_surface = pygame.display.set_mode(resolution)
		self.game_mode = MODE_CONTROL
		self.idle_timer = 0
		self.gui_movie = None
		self.running = True
		self.msgfont = pygame.font.Font(pygame.font.get_default_font(), 12)
		self.videos = video_list
		self.videos_position = 0
		self.idle_timeout = configuration['idle_timeout']
		self.menu_position = 0
		self.init_menus(menu_data)
		self.set_menu("main")

	def init_menus(self, data):
		self._menus = dict()
		for menu in data:
			self._menus[menu['id']] = menu

	def set_menu(self, id):
		self._current_menu = self._menus[id]

	def start(self):
		while self.running:
			self.update()
			# poll after update so quit causes exit before next update
			self.poll_events()

	def poll_events(self):
		for event in pygame.event.get():
			if event.type == MOVIECOMPLETE:
				self.exit_movie_mode()
			elif event.type == KEYDOWN:
				self.idle_timer = pygame.time.get_ticks()
				self.exit_movie_mode()
				if event.key == K_ESCAPE:
					pygame.event.post(pygame.event.Event(QUIT))
			elif event.type == QUIT:
			# check quit last so exit is not followed by pygame calls
				self.exit()

	def update(self):
		if self.game_mode == MODE_CONTROL:
			self.show_menu()
			pygame.display.update()
			self.clock.tick(30)
			if pygame.time.get_ticks() - self.idle_timer >= self.idle_timeout:
				self.start_movie()
				self.game_mode = MODE_VIDEO
			else:
				self.write_idle_message()

		elif self.game_mode == MODE_VIDEO:
			if not self.gui_movie.get_busy():
				pygame.event.post(pygame.event.Event(MOVIECOMPLETE))

	def show_menu(self):
		self.draw_background()
		self.draw_preview()
		self.draw_items()

	def draw_background(self):
		pass

	def draw_preview(self):
		pass

	def draw_items(self):
		coords = self.draw_selected_item()
		self.draw_upper_items(coords)
		self.draw_lower_items(coords)
		
	def draw_selected_item(self):
		items = self.get_menu_items()
		item = items[self.menu_position]
		self.blit_text(

	def draw_upper_items(self):
		items = self.get_menu_items()
		pass

	def get_menu_items(self):
		return self._current_menu['items']

	def start_movie(self):
		pygame.mixer.quit()
		self.gui_movie = pygame.movie.Movie(self.get_next_movie())
		self.gui_movie.set_display(self.window_surface, self.window_surface.get_rect())
		self.gui_movie.play()

	def stop_movie(self):
		self.gui_movie.stop()
		self.gui_movie.set_display(None)
		self.gui_movie = None
		pygame.mixer.init()

	def exit(self):
		if self.game_mode == MODE_VIDEO:
			self.stop_movie()
		pygame.quit()
		self.running = False

	def exit_movie_mode(self):
		if self.game_mode == MODE_VIDEO:
			self.game_mode = MODE_CONTROL
			self.idle_timer = pygame.time.get_ticks()
			self.stop_movie()
			self.window_surface.fill(COLOR_BLACK)

	def write_idle_message(self):
		diff = round((pygame.time.get_ticks() - self.idle_timer) / 1000)
		remain = int(round(self.idle_timeout / 1000) - diff)
		msg = str(remain) + " seconds until video..."
		self.write_message(msg)

	def blit_text(self, msg, x, y, font=pygame.font.get_default_font(), color=COLOR_WHITE, size=12, aa=True):
		surface = pygame.font.Font(font, size).render(msg, aa, color)
		msgrect = msgSurface.get_rect()
		msgrect.topleft = (x, y)
		self.window_surface.blit(surface, msgrect)

	def write_message(self, msg):
		msgSurface = self.msgfont.render(msg, False, COLOR_WHITE)
		msgrect = msgSurface.get_rect()
		msgrect.topleft = (10, 20)
		self.window_surface.fill(COLOR_BLACK, msgrect)
		self.window_surface.blit(msgSurface, msgrect)
		
	def get_next_movie(self):
		next = self.videos[self.videos_position]
		self.videos_position += 1
		if self.videos_position == len(self.videos):
			self.videos_position = 0
		return next

config_reader = dekarrin.file.lines.ConfigReader(CONFIG_FILE)
config = config_reader.read()

vid_reader = dekarrin.file.lines.ListReader(config['video_list'])
vids = vid_reader.read()

menu_data = []
for menu_item in os.listdir(config['menus_dir']):
	jfile = open(menu_item)
	menu_data.extend(json.load(jfile))

game = TouhouLauncher(config, vids, menu_data)
game.start()

