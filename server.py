# Kim Ngo and Kendra Bilardello
# Programming Paradigms -- CSE30332
# PyGame + Twisted final project
# April 29, 2015

import pygame
import sys
import math
from pygame.locals import *

from random import randint

GAME_WIDTH = 960
GAME_HEIGHT = 640

class Apple(pygame.sprite.Sprite):
	def __init__(self,gs=None):
		pygame.sprite.Sprite.__init__(self)

		self.gs = gs

		self.image = pygame.image.load("images/apple.png")
		self.rect = self.image.get_rect()
		self.image_eaten = pygame.image.load("images/apple_blank.png")

		self.rect.centerx = randint(0+self.rect.width, GAME_WIDTH-self.rect.width)
		self.rect.centery = randint(0+self.rect.height, GAME_WIDTH-self.rect.height)

		print self.rect.centerx, self.rect.centery

		self.eaten = 0

	def tick(self):
		if self.eaten:
			self.rect.centerx = randint(0+self.rect.width, GAME_WIDTH-self.rect.width)
			self.rect.centery = randint(0+self.rect.height, GAME_WIDTH-self.rect.height)
			self.eaten = 0

class GameSpace:
	def main(self):
		pygame.init()

		self.size = self.width, self.height = GAME_WIDTH, GAME_HEIGHT
		self.black = 0, 0, 0, 0
		self.screen = pygame.display.set_mode(self.size)

		self.clock = pygame.time.Clock()

		#self.player1 = Player(self)
		#self.player2 = Player(self)
		self.apple = Apple(self)

		# Game loop
		while 1:
			self.clock.tick(60)

			#self.player1.tick()
			#self.player2.tick()
			self.apple.tick()

			self.screen.fill(self.black)
			
			# Check collision
				# Snake & snake
				# Snake and wall
				# Snake and apple

			#self.screen.blit(self.player1.image, self.player1.rect)
			#self.screen.blit(self.player2.image, self.player2.rect)
			self.screen.blit(self.apple.image, self.apple.rect)

			pygame.display.flip() # double buffer animation system

if __name__ == '__main__':
	gs = GameSpace()
	gs.main()


