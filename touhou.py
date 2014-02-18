#os.environ['SDL_VIDEODRIVER'] = 'windib'

import pygame, sys
from pygame.locals import *

import dekarrin.file.lines

import json
import os

CONFIG_FILE = 'launcher.cfg'

M_CONTROL = 0
M_VIDEO = 1

E_MOVIECOMPLETE = 1

COLOR_WHITE = pygame.Color(255, 255, 255)
COLOR_BLACK = pygame.Color(0, 0, 0)

class TouhouLauncher(object):

	def __init__(self, configuration, video_list, wheel_data, key_bindings):
		self.binder = KeyBinder()
		self.binder.bind_all(key_bindings)
		self.config = configuration
		pygame.init()
		resolution = (configuration['resolution_width'], configuration['resolution_height']);
		self.clock = pygame.time.Clock()
		self.window_surface = pygame.display.set_mode(resolution)
		self.game_mode = M_CONTROL
		self.idle_timer = 0
		self.gui_movie = None
		self.running = True
		self.msgfont = pygame.font.Font(pygame.font.get_default_font(), 12)
		self.videos = video_list
		self.videos_position = 0
		self.idle_timeout = configuration['idle_timeout']
		self._wheel = WheelManager(wheel_data, config['root_wheel_id'])
		self.background_surf = pygame.image.load(config['background'])
		self._wheel_y_offset = 0
		self._anim = Animator()

	def start(self):
		while self.running:
			self.update()
			# poll after update so quit causes exit before next update
			self.poll_events()

	def poll_events(self):
		for event in pygame.event.get():
			if event.type == USEREVENT:
				self._handle_user_event(event)
			elif event.type == KEYDOWN:
				self.idle_timer = pygame.time.get_ticks()
				self.exit_movie_mode()
				if event.key == self.binder.key_for('LAUNCHER_EXIT'):
					pygame.event.post(pygame.event.Event(QUIT))
				elif event.key == self.binder.key_for('WHEEL_PREV'):
					self._wheel.prev()
					self._wheel_y_offset = self.get_wheel_offset(above=True)
					self._anim.add_animation(300, self, '_wheel_y_offset', 0)
				elif event.key == self.binder.key_for('WHEEL_NEXT'):
					self._wheel.next()
					self._wheel_y_offset = self.get_wheel_offset(above=False)
					self._anim.add_animation(300, self, '_wheel_y_offset', 0)
				elif event.key == self.binder.key_for('WHEEL_ADVANCE'):
					self._wheel.advance()
				elif event.key == self.binder.key_for('WHEEL_BACK'):
					self._wheel.backtrack()
			elif event.type == QUIT:
			# check quit last so exit is not followed by pygame calls
				self.exit()
				
	def _handle_user_event(self, event):
		if event.code == E_MOVIECOMPLETE:
			self.exit_movie_mode()

	def update(self):
		if self.game_mode == M_CONTROL:
			self._anim.pulse()
			self.draw_screen()
			if pygame.time.get_ticks() - self.idle_timer >= self.idle_timeout:
				self.start_movie()
				self.game_mode = M_VIDEO
			else:
				self.draw_idle_message()
			pygame.display.flip()
			self.clock.tick(30)
		elif self.game_mode == M_VIDEO:
			if not self.gui_movie.get_busy():
				pygame.event.post(pygame.event.Event(USEREVENT, code=E_MOVIECOMPLETE))

	def draw_screen(self):
		self.draw_background()
		self.draw_preview()
		if self._wheel.subitems_count() > 0:
			self.draw_items()

	def draw_background(self):
		self.window_surface.blit(self.background_surf, self.background_surf.get_rect())

	def draw_preview(self):
		pass

	def draw_items(self):
		coords = self.draw_selected_item()
		self.draw_other_items(coords, above=True)
		self.draw_other_items(coords, above=False)
		
	def get_wheel_offset(self, above=False):
		if above:
			txt = self.make_text_surface(" ", size=self.config['menu_item_font_size'])
			return -(txt.get_rect().height + config['menu_item_vertical_spacing'])
		else:
			txt = self.make_text_surface(" ", size=self.config['menu_item_font_size_selected'])
			return txt.get_rect().height + config['menu_item_vertical_spacing']
		
	def draw_selected_item(self):
		text = self.make_text_surface(self._wheel.get_item_title(), size=self.config['menu_item_font_size_selected'])
		textr = text.get_rect()
		x, y = self.get_selected_coords(textr)
		y += self._wheel_y_offset
		self.blit_surface(text, x, y)
		return pygame.Rect((x, y), textr.size)
	
	def get_selected_coords(self, selrect):
		x = round((self.config['menu_percent_width']/100.0) * self.get_width())
		y = round(((self.config['menu_main_item_percent_height']/100.0) * self.get_height()) - (selrect.height / 2.0))
		return (x, y)
				
	def draw_other_items(self, selrect, above=True):
		direction_mult = 1
		if above:
			direction_mult *= -1
		num = 1
		while True:
			title = self._wheel.get_item_title(num * direction_mult)
			text = self.make_text_surface(title, size=self.config['menu_item_font_size'])
			textr = text.get_rect()
			ydiff = self.config['menu_item_vertical_spacing'] + textr.height
			if above:
				offset = ydiff
			else:
				offset = selrect.height + self.config['menu_item_vertical_spacing']
			x = selrect.x
			y = selrect.y + (offset + (ydiff * (num-1))) * direction_mult
			if y + textr.height - 1 < 0 or y > self.get_height():
				break
			else:
				self.blit_surface(text, x, y)
				num += 1
				
	def get_height(self):
		return pygame.display.Info().current_h
		
	def get_width(self):
		return pygame.display.Info().current_w

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
		if self.game_mode == M_VIDEO:
			self.stop_movie()
		pygame.quit()
		self.running = False

	def exit_movie_mode(self):
		if self.game_mode == M_VIDEO:
			self.game_mode = M_CONTROL
			self.idle_timer = pygame.time.get_ticks()
			self.stop_movie()
			self.window_surface.fill(COLOR_BLACK)

	def draw_idle_message(self):
		diff = round((pygame.time.get_ticks() - self.idle_timer) / 1000)
		remain = int(round(self.idle_timeout / 1000) - diff)
		msg = str(remain) + " seconds until video..."
		self.draw_message(msg)

	def make_text_surface(self, msg, font=pygame.font.get_default_font(), color=COLOR_WHITE, size=12, aa=True):
		return pygame.font.Font(font, size).render(msg, aa, color)
		
	def blit_surface(self, surface, x, y):
		srect = surface.get_rect()
		srect.topleft = (x, y)
		self.window_surface.blit(surface, srect)

	def draw_message(self, msg):
		msgSurface = self.msgfont.render(msg, True, COLOR_WHITE)
		msgrect = msgSurface.get_rect()
		msgrect.topleft = (10, 20)
		self.window_surface.blit(msgSurface, msgrect)
		
	def get_next_movie(self):
		next = self.videos[self.videos_position]
		self.videos_position += 1
		if self.videos_position == len(self.videos):
			self.videos_position = 0
		return next

class KeyBinder(object):
	"""Provide automatic binding to pygame key constants."""

	def __init__(self):
		self._bindings = dict()
	
	def bind_all(self, text_bindings):
		for action, binding in text_bindings.items():
			self.bind(action, binding)

	def bind(self, action_index, key_name):
		try:
			self._bindings[action_index] = eval(key_name)
		except NameError as e:
			print "'%s' is not a valid key code!" % key_name
			raise e

	def key_for(self, action_index):
		return self._bindings[action_index]

class Animator(object):
	"""Lets us add tweening to properties."""
	def __init__(self):
		self._animations = []
		
	def add_animation(self, time, target, prop, end, delta_hook=None, end_hook=None):
		"""Start animating a property of an object.

		
		time - amount of time in milliseconds that the animation should take.

		target - the object that has a property to be animated.

		prop - the name of the property to animate.

		end - the ending value of the property; when it is equal to this
		value, the animation is ended.

		delta_hook - Function to change the prop. Must accept start_val,
		current_val, end_val, and percent_complete (will be float from 0 to 1)
		and return the new value of the property. It is assumed to be complete
		if comparing the new value to end_value yields True. Leave as None to
		assume numeric value for prop and end and let Animator do the math.

		end_hook - Function to call when animation is complete. Leave as None to
		call no function on completion.
		"""
		start = pygame.time.get_ticks()
		startval = getattr(target, prop)
		if delta_hook is None:
			delta_hook = self._numeric_linear_tween
		anim = {'start_time': start, 'duration': time, 'target': target,
				'prop': prop, 'start': startval, 'end': end,
				'delta_hook': delta_hook, 'end_hook': end_hook}
		self._animations.append(anim)
		
	def pulse(self):
		"""Execute all animations."""
		active_anims = []
		for anim in self._animations:
			time = pygame.time.get_ticks() - anim['start_time']
			progress = time / float(anim['duration'])
			start_val = anim['start']
			current_val = getattr(anim['target'], anim['prop'])
			end_val = anim['end']
			new_val = anim['delta_hook'](start_val, current_val, end_val, progress)
			setattr(anim['target'], anim['prop'], new_val)
			if new_val == end_val:
				if anim['end_hook'] is not None:
					anim['end_hook']()
			else:
				active_anims.append(anim)
		self._animations = active_anims
		
	def _numeric_linear_tween(self, startval, curval, endval, progress):
		d = endval - startval
		newval = startval + (d * progress)
		if (d > 0 and newval > endval) or (d < 0 and newval < endval) or d == 0:
			newval = endval
		return newval


config_reader = dekarrin.file.lines.ConfigReader(CONFIG_FILE)
config = config_reader.read()

vid_reader = dekarrin.file.lines.ListReader(config['video_list'])
vids = vid_reader.read()

wheel_data = []
for wheel_item in os.listdir(config['wheels_dir']):
	jfile = open(os.path.join(config['wheels_dir'], wheel_item))
	wheel_data.extend(json.load(jfile))
	jfile.close()

bindings_reader = dekarrin.file.lines.ConfigReader(config['key_bindings'])
key_bindings = bindings_reader.read()

game = TouhouLauncher(config, vids, wheel_data, key_bindings)
game.start()
