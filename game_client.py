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
GAME_HEIGHT = 640
HOST = 'student02.cse.nd.edu'
try:
	PORT = int(sys.argv[1])
except IndexError:
	print 'Usage:', sys.argv[0], '[port 9082/9083]'
	sys.exit()
#The initial snake is 5 parts long
SNAKE1=[(0,0),(0,0),(0,0),(0,0),(0,0)]#[(5,5),(5,4),(5,3),(5,2),(5,1)]
SNAKE2=[(0,0),(0,0),(0,0),(0,0),(0,0)]#[(5,5),(5,4),(5,3),(5,2),(5,1)]
scale = 15


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
			SNAKE1.append(SNAKE1[-1]) #Add a part onto the snake


class Snake(pygame.sprite.Sprite):
	def __init__(self,gs=None):
		pygame.sprite.Sprite.__init__(self)
		self.gs = gs
		self.image = pygame.image.load("images/snake_blue.png")
		self.rect = self.image.get_rect()
		self.rect.centerx = 0
		self.rect.centery = 0
		self.length = 5

#Whenever the snake is moved with a button press, this function handles it
def move(pressed, player1, size):
	x=0
	y=0
	key = pygame.key.get_pressed()
	#Up button pressed
	if pressed == 1:
		x=0
		y=-1
		if player1.rect.top > 0:
			player1.rect.centery -= scale
		else:
			print "Out of bounds top" #Hit top of screen
			exit(1)
	#Down button pressed
	if pressed == 2:
		x=0
		y=1
		if player1.rect.bottom < size[1]:
			player1.rect.centery += scale
		else:
			print "Out of bounds bottom" #Hit bottom of screen
			exit(1)
	#Left button pressed
	if pressed == 3:
		x=-1
		y=0
		if player1.rect.left > 0:
			player1.rect.centerx -= scale
		else:
			print "Out of bounds left" #Hit left of screen
			exit(1)
	#Right button pressed
	if pressed == 4:
		x=1
		y=0
		if player1.rect.right < size[0]:
			player1.rect.centerx += scale
		else:
			print "Out of bounds right" #Hit right of screen
			print player1.rect.right
			exit(1)

	t=SNAKE1[0] #Head of the snake
	t=(t[0]+x,t[1]+y) #Increment parts of snake
	SNAKE1.insert(0,t) #Insert new element in front of snake
	del SNAKE1[-1] #Delete the last element of the snake

	#Check if snake has run into himself
	if SNAKE1[0] in SNAKE1[1:]:
		print "Player is dead"
		exit(1)
	
#Show the snake on the screen
def draw_snake(screen, player, snakeX):
	#Iterate through all the parts of the snake and show them on the screen
	for i in snakeX:
		rect = (i[0]*scale,i[1]*scale,scale-1,scale-1)
		screen.blit(player.image,rect)

class GameSpace:
	def __init__(self):
		pygame.init()

		self.size = self.width, self.height = GAME_WIDTH, GAME_HEIGHT
		self.black = 0, 0, 0, 0
		self.screen = pygame.display.set_mode(self.size)

		self.apple = Apple(self)
		self.player1 = Snake(self)
		self.player2 = Snake(self)
		self.k = 0
		self.pressed = 2

	# Game loop
	def mainloop(self):
		global SNAKE1, SNAKE2

		#Handle the keyboard events
		for event in pygame.event.get():
			if event.type == QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
				pygame.quit()
				sys.exit()
			elif event.type == KEYDOWN:
				if event.key == K_UP:
					self.pressed = 1
				if event.key == K_DOWN:
					self.pressed = 2
				if event.key == K_LEFT:
					self.pressed = 3
				if event.key == K_RIGHT:
					self.pressed = 4


		# Send server new head and body position to other player
		global factory
		pos_str = "position," + str(self.player1.rect.centerx) + ',' + str(self.player1.rect.centery)
		snake_str = ",".join("%s,%s" % tup for tup in SNAKE1)
		send_snake = "snake," + snake_str		
		factory.connections["server"].sendLine(pos_str)
		factory.connections["server"].sendLine(send_snake)

		# Check collision
			# Snake & snake
			# Snake and itself
			
		# Collision: snake and apple
		if pygame.sprite.collide_rect(self.apple, self.player1) and not self.apple.eaten:
			print "You ate the apple\n"
			self.apple.eaten = 1
			self.player1.length += 1
			factory.connections["server"].sendLine("apple\r\n")
			# Notify server that apple has been eaten

		
		#To check if apple needs to be respawned
		self.apple.tick()
		#Move the snake across the screen
		if self.k%5==0: 
			move(self.pressed,self.player1,self.size)


		self.k+=1
		self.screen.fill(self.black)
		self.screen.blit(self.apple.image, self.apple.rect)
		draw_snake(self.screen,self.player1, SNAKE1)
		draw_snake(self.screen,self.player2, SNAKE2)

		pygame.display.flip() # double buffer animation system


class ClientConnFactory(ClientFactory):
	def __init__(self):
		self.connections = {}
	def buildProtocol(self, addr):
		return ClientConnProtocol(self)

class ClientConnProtocol(LineReceiver):
	def __init__(self, factory):
		self.factory = factory
		self.start = 0

	def connectionMade(self):
		self.factory.connections["server"] = self
		print "Connected to server"

	def connectionLost(self, reason):
		del self.factory.connections["server"]

	# Process data received from server
	def lineReceived(self, raw_data):
		data = raw_data.strip()
		data = data.split(',')
		global gs, SNAKE1, SNAKE2
				
		# Update other snake's head position
		if data[0] == "position":
			gs.player2.rect.centerx = int(data[X])
			gs.player2.rect.centery = int(data[Y])

		# Update other snake's body position
		elif data[0] == "snake":
			i = 0
			index = 0
			if len(SNAKE2) < (len(data)-1)/2:
				SNAKE2.append(SNAKE2[-1])
			for elem in enumerate(data):
				if i%2 != 0:
					SNAKE2[index] = (int(data[i]),int(data[i+1]))
					index+=1
				i+=1

		# Update apple's new position
		elif data[0] == "apple":
			gs.apple.rect.centerx = int(data[X])
			gs.apple.rect.centery = int(data[Y])

		# Initialize player head starting positions
		# Start game loop only once body everything is initialized
		if data[0] == "start":
			global loop
			gs.player1.rect.centerx = int(data[X])
			gs.player1.rect.centery = int(data[Y])
			self.start += 1
			if self.start == 3:
				loop.start(1.0/FPS)

		# Initialize player body starting positions
		# Start game loop only once body everything is initialized
		elif data[0] == "init":
			i = 0
			index = 0
			if len(SNAKE1) < (len(data)-1)/2:
				SNAKE1.append(SNAKE1[-1])
			for elem in enumerate(data):
				if i%2 != 0:
					SNAKE1[index] = (int(data[i]),int(data[i+1]))
					index+=1
				i+=1
			self.start += 1
			if self.start == 3:
				loop.start(1.0/FPS)

		# Initialize other player body starting positions
		# Start game loop only once body everything is initialized
		elif data[0] == "init2":
			i = 0
			index = 0
			if len(SNAKE2) < (len(data)-1)/2:
				SNAKE2.append(SNAKE2[-1])
			for elem in enumerate(data):
				if i%2 != 0:
					SNAKE2[index] = (int(data[i]),int(data[i+1]))
					index+=1
				i+=1
			self.start += 1
			if self.start == 3:
				loop.start(1.0/FPS)

			
global factory, gs, loop
factory = ClientConnFactory()
gs = GameSpace()
loop = LoopingCall(gs.mainloop)

reactor.connectTCP(HOST, PORT, factory)
reactor.run()

