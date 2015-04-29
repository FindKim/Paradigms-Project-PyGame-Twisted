#Kendra Bilardello, pygame
#Due: May 7th, 2015

import pygame
import sys
import math
from pygame.locals import *

#Player Class
class Player(pygame.sprite.Sprite):
	def __init__(self, gs=None):
		pygame.sprite.Sprite.__init__(self)

		self.gs = gs
		self.image = pygame.image.load("ironman.png") # Player image
		self.rect = self.image.get_rect()

		# Player starting position
		self.x = 100
		self.y = 100
		
		# Keep original image to limit resize errors
		self.orig_image = self.image

	def tick(self):

		# Get the mouse x and y position on the screen
		mx, my = pygame.mouse.get_pos()




