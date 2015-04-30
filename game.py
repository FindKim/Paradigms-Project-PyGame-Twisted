# Kim Ngo and Kendra Bilardello
# Programming Paradigms -- CSE30332
# PyGame + Twisted final project
# April 29, 2015

#from game_client import *
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

		self.rect.centerx = randint(0+self.rect.width*2, GAME_WIDTH-self.rect.width*2)
		self.rect.centery = randint(0+self.rect.height*2, GAME_HEIGHT-self.rect.height*2)

		print self.rect.centerx, self.rect.centery

		self.eaten = 0

	def tick(self):
		if self.eaten:
			self.rect.centerx = randint(0+self.rect.width*2, GAME_WIDTH-self.rect.width*2)
			self.rect.centery = randint(0+self.rect.height*2, GAME_HEIGHT-self.rect.height*2)
			self.eaten = 0

class Snake(pygame.sprite.Sprite):
	def __init__(self,gs=None):
		pygame.sprite.Sprite.__init__(self)
		self.gs = gs
		self.image = pygame.image.load("images/snake_blue.png")
		self.rect = self.image.get_rect()
		self.rect.centerx = 960/3
		self.rect.centery = 640/2
		
		self.length = 1

class GameSpace:
	def main(self):#, factory):
		pygame.init()

		#self.factory = factory

		self.size = self.width, self.height = GAME_WIDTH, GAME_HEIGHT
		self.black = 0, 0, 0, 0
		self.screen = pygame.display.set_mode(self.size)

		self.clock = pygame.time.Clock()

		#self.player1 = Player(self)
		#self.player2 = Player(self)
		self.apple = Apple(self)
		self.player1 = Snake(self)
		#self.pos.x = self.player1.rect.centerx
		#self.pos.y = self.player1.rect.centery
		#self.player2 = Snake(self)
		#self.player2.rect.centerx *= 2

		# Game loop
		while 1:
			self.clock.tick(60)

			for event in pygame.event.get():
				if event.type == QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
					pygame.quit()
					sys.exit()

			key = pygame.key.get_pressed()
			if key[pygame.K_UP]:
				if self.player1.rect.top > 0:
					self.player1.rect.centery -= 5
				else:
					self.player1.rect.centery = self.height
			if key[pygame.K_DOWN]:
				if self.player1.rect.bottom < self.height:
					self.player1.rect.centery += 5
				else:
					self.player1.rect.centery = 0
			if key[pygame.K_LEFT]:
				if self.player1.rect.left > 0:
					self.player1.rect.centerx -= 5
				else:
					self.player1.rect.centerx = self.width
			if key[pygame.K_RIGHT]:
				if self.player1.rect.right < self.width:
					self.player1.rect.centerx += 5
				else:
					self.player1.rect.centerx = 0

			#self.pos.x = self.player1.rect.centerx
			#self.pos.y = self.player1.rect.centery

			# Check collision
				# Snake & snake
				# Snake and itself
			# Collision: snake and apple
			if pygame.sprite.collide_rect(self.apple, self.player1):
				self.apple.eaten = 1
				self.player1.length += 1
				#self.factory.connections["server"].transport.write("apple")
			
			#self.factory.connections["server"].transport.write(self.pos)
			#if (pos2 = self.factory.connections["server"].dataReceived()):
			#	self.player2.rect.centerx = pos2.x
			#	self.player2.rect.centery = pos2.y

			#self.player1.tick()
			#self.player2.tick()
			self.apple.tick()

			self.screen.fill(self.black)
			
			#self.screen.blit(self.player1.image, self.player1.rect)
			#self.screen.blit(self.player2.image, self.player2.rect)
			self.screen.blit(self.apple.image, self.apple.rect)
			self.screen.blit(self.player1.image, self.player1.rect)
			#self.screen.blit(self.player2.image, self.player2.rect)

			pygame.display.flip() # double buffer animation system

if __name__ == '__main__':
	#factory = ClientConnFactory()
	#reactor.connectTCP(HOST, PORT, factory)
	gs = GameSpace()
	gs.main()#factory)


