import pygame, sys
from pygame.locals import *

pygame.init()
clock = pygame.time.Clock()
window_surface = pygame.display.set_mode((640, 480), pygame.FULLSCREEN)

neko = pygame.movie.Movie('neko_miko.mp4')

neko.set_display(window_surface)

while True:
	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			sys.exit()
		elif event.type == KEYDOWN and event.key == K_ESCAPE:
			pygame.event.post(pygame.event.Event(QUIT))
	pygame.display.update()
	clock.tick(30)
