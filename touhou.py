import pygame, sys
from pygame.locals import *

RESOLUTION = (640, 480)

MODE_CONTROL = 0
MODE_VIDEO = 1

IDLE_TIMEOUT = 5000

MOVIECOMPLETE = USEREVENT + 1

class Touhou(object):
	def __init__(self):
		pygame.init()
		self.clock = pygame.time.Clock()
		self.window_surface = pygame.display.set_mode(RESOLUTION, pygame.FULLSCREEN)
		self.game_mode = MODE_CONTROL
		self.idle_timer = 0
		self.gui_movie = None
		self.running = True
		self.msgfont = pygame.font.Font(pygame.font.get_default_font(), 12)

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
				if event.key == K_ESCAPE:
					pygame.event.post(pygame.event.Event(QUIT))
			elif event.type == QUIT:
			# check quit last so exit is not followed by pygame calls
				self.exit()

	def update(self):
		if self.game_mode == MODE_CONTROL:
			pygame.display.update()
			self.clock.tick(30)
			if pygame.time.get_ticks() - self.idle_timer >= IDLE_TIMEOUT:
				self.start_movie()
				self.game_mode = MODE_VIDEO
			else:
				self.write_idle_message()

		elif self.game_mode == MODE_VIDEO:
			if not self.gui_movie.get_busy():
				pygame.event.post(pygame.event.Event(MOVIECOMPLETE))

	def start_movie(self):
		pygame.mixer.quit()
		self.gui_movie = pygame.movie.Movie('neko_miko.mpg')
		self.gui_movie.set_display(self.window_surface, self.window_surface.get_rect())
		self.gui_movie.play()

	def stop_movie(self):
		self.gui_movie.set_display(None)
		pygame.mixer.init()

	def exit(self):
		if self.game_mode == MODE_VIDEO:
			self.stop_movie()
		pygame.quit()
		self.running = False

	def exit_movie_mode(self):
		self.game_mode = MODE_CONTROL
		self.idle_timer = pygame.time.get_ticks()
		self.stop_movie()

	def write_idle_message(self):
		diff = round((pygame.time.get_ticks() - self.idle_timer) / 1000)
		remain = diff - round(IDLE_TIMEOUT / 1000)
		msg = str(remain) + " seconds until video..."
		self.write_message(msg)

	def write_message(self, msg):
		msgSurface = self.msgfont.render(msg, False, pygame.Color(255, 255, 255))
		msgrect = msgSurface.get_rect()
		msgrect.topleft = (10, 20)
		self.window_surface.blit(msgSurface, msgrect)

game = Touhou()
game.start()

