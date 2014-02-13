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
		self.config = configuration

	def init_menus(self, data):
		self._menus = dict()
		for menu in data:
			self._menus[menu['id']] = menu
			
		targetstack = list()
		targetstack.append(self._menus)
		
		for menu in targetstack[-1]:
			for subitem in 
			
	def assign_menu_subitems(self, menu):
		ids = list()
		for itemid in menu['items']:
			ids.append(itemid)

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
		self.draw_other_items(coords, above=True)
		self.draw_other_items(coords, above=False)
		
	def draw_selected_item(self):
		items = self.get_menu_items()
		item = items[self.menu_position]
		text = self.make_text_surface(item['title'], size=self.config['menu_item_font_size_selected'])
		textr = text.get_rect()
		x, y = self.get_selected_coords(textr)
		self.blit_surface(text, x, y)
		return textr
		
	def get_selected_coords(self, selrect):
		x = round((self.config['menu_percent_width']/100) * self.get_width())
		y = round(((self.config['menu_main_item_percent_height']/100) * self.get_height()) - (selrect.height / 2))
		return (x, y)
				
	def draw_other_items(self, selrect, above=True):
		dirmult = 1
		if above:
			dirmult *= -1
		items = self.get_menu_items()
		num = 1
		while True:
			pos = self.menu_position + (mult * num)
			if pos < 0 or pos >= len(items):
				break
			item = items[pos]
			text = self.make_text_surface(item['title'], size=self.config['menu_item_font_size'])
			textr = text.get_rect()
			ydiff = self.config['menu_item_vertical_spacing']
			if above or num is not 1:
				ydiff += textr.height
			else:
				ydiff += selrect.height
			x = selrect.x
			y = selrect.y + (ydiff * num)
			if y < 0 or y + textr > self.get_height():
				break
			else:
				self.blit_surface(text, x, y)
				num += 1
				
	def get_height(self):
		info = pygame.display.Info()
		return info['current_h']
		
	def get_width(self):
		info = pygame.display.Info()
		return info['current_w']

	def get_menu_items(self, selrect):
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

	def make_text_surface(self, msg, font=pygame.font.get_default_font(), color=COLOR_WHITE, size=12, aa=True):
		return pygame.font.Font(font, size).render(msg, aa, color)
		
	def blit_surface(self, surface, x, y):
		srect = surface.get_rect()
		srect.topleft = (x, y)
		self.window_surface.blit(surface, srect)

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

