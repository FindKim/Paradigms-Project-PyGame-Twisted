from twisted.internet.protocol import Factory
from twisted.internet.protocol import ClientFactory
from twisted.internet.protocol import Protocol
from twisted.protocols.basic import LineReceiver
from twisted.internet import reactor
from twisted.internet.task import LoopingCall
import sys

import pygame
import sys
import math
from pygame.locals import *

FPS = 30
X = 1
Y = 2
GAME_WIDTH = 640
GAME_HEIGHT = 960
HOST = 'student02.cse.nd.edu'
try:
	PORT = int(sys.argv[1])
except IndexError:
	print 'Usage:', sys.argv[0], '[port 9082/9083]'
	sys.exit()



class Apple(pygame.sprite.Sprite):
	def __init__(self,gs=None):
		pygame.sprite.Sprite.__init__(self)

		self.gs = gs
		self.image = pygame.image.load("images/apple.png")
		self.rect = self.image.get_rect()
		self.image_eaten = pygame.image.load("images/apple_blank.png")
		self.rect.centerx = 0
		self.rect.centery = 0
		self.eaten = 0

	def tick(self):
		if self.eaten:
			self.eaten = 0


class Snake(pygame.sprite.Sprite):
	def __init__(self,gs=None):
		pygame.sprite.Sprite.__init__(self)
		self.gs = gs
		self.image = pygame.image.load("images/snake_blue.png")
		self.rect = self.image.get_rect()
		self.rect.centerx = 0
		self.rect.centery = 0
		self.length = 1

class GameSpace:
	def __init__(self):
		pygame.init()

		self.size = self.width, self.height = GAME_WIDTH, GAME_HEIGHT
		self.black = 0, 0, 0, 0
		self.screen = pygame.display.set_mode(self.size)

		self.apple = Apple(self)
		self.player1 = Snake(self)
		self.player2 = Snake(self)

	# Game loop
	def mainloop(self):

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

		# Send server new position to other player
		global factory
		pos_str = "position," + str(self.player1.rect.centerx) + ',' + str(self.player1.rect.centery)
		factory.connections["server"].sendLine(pos_str)

		# Check collision
			# Snake & snake
			# Snake and itself
		# Collision: snake and apple
		if pygame.sprite.collide_rect(self.apple, self.player1):
			self.apple.eaten = 1
			self.player1.length += 1
			factory.connections["server"].sendLine("apple\r\n")
			# Notify server that apple has been eaten

		self.apple.tick()
		self.screen.fill(self.black)
		self.screen.blit(self.apple.image, self.apple.rect)
		self.screen.blit(self.player1.image, self.player1.rect)
		self.screen.blit(self.player2.image, self.player2.rect)

		pygame.display.flip() # double buffer animation system




class ClientConnFactory(ClientFactory):
	def __init__(self):
		self.connections = {}
	def buildProtocol(self, addr):
		return ClientConnProtocol(self)

class ClientConnProtocol(LineReceiver):
	def __init__(self, factory):
		self.factory = factory

	def connectionMade(self):
		self.factory.connections["server"] = self

	def connectionLost(self, reason):
		del self.factory.connections["server"]

	def lineReceived(self, raw_data):
		data = raw_data.strip()
		data = data.split(',')
		global gs
		
		if data[0] == "start":
			global loop
			loop.start(1.0/FPS)
			gs.player1.rect.centerx = int(data[X])
			gs.player1.rect.centery = int(data[Y])
		
		elif data[0] == "position":
			gs.player2.rect.centerx = int(data[X])
			gs.player2.rect.centery = int(data[Y])
			
		elif data[0] == "apple":
			gs.apple.rect.centerx = int(data[X])
			gs.apple.rect.centery = int(data[Y])
			
global factory, gs, loop
factory = ClientConnFactory()
gs = GameSpace()
loop = LoopingCall(gs.mainloop)

reactor.connectTCP(HOST, PORT, factory)
reactor.run()

