from twisted.internet.protocol import Factory
from twisted.internet.protocol import ClientFactory
from twisted.internet.protocol import Protocol
from twisted.protocols.basic import LineReceiver
from twisted.internet import reactor
from twisted.internet.task import LoopingCall
import sys
import time
import os

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
START = 1
CHOOSE = 1
OFFSET = 50
DEAD = 0


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

class Other_Snake(pygame.sprite.Sprite):
	def __init__(self,gs=None):
		pygame.sprite.Sprite.__init__(self)
		self.gs = gs
		self.image = pygame.image.load("images/snake_green.png")
		self.rect = self.image.get_rect()
		self.rect.centerx = 0
		self.rect.centery = 0
		self.length = 5

class GameSpace:
	def __init__(self):
		pygame.init()

		self.size = self.width, self.height = GAME_WIDTH, GAME_HEIGHT
		self.black = 0, 0, 0, 0
		self.screen = pygame.display.set_mode(self.size)

		# Images for the start screen
		self.background = pygame.image.load("images/start_screen.png")
		self.start_button = pygame.image.load("images/start_button.png")

		# Images for choosing a custom background
		self.text_back = pygame.image.load("images/text_choose.png")
		self.blue_back = pygame.image.load("images/blue_small.png")
		self.brown_back = pygame.image.load("images/brown_small.png")
		self.green_back = pygame.image.load("images/green_small.png")
		self.pattern_back = pygame.image.load("images/pattern_small.png")
		self.snake_back = pygame.image.load("images/snake_small.png")

		# Waiting for other player to choose background
		self.waiting_other = pygame.image.load("images/waiting.png")

		# Images to show the full background
		self.full_blue = pygame.image.load("images/background_blue_scale.png")
		self.full_brown = pygame.image.load("images/background_brown_scale.png")
		self.full_green = pygame.image.load("images/background_green.png")
		self.full_green = pygame.transform.scale(self.full_green, (GAME_WIDTH, GAME_HEIGHT))
		self.full_pattern = pygame.image.load("images/background_pattern.png")
		self.full_snake = pygame.image.load("images/background_snake.png")

		#  Define players
		self.apple = Apple(self)
		self.player1 = Snake(self)
		self.player2 = Other_Snake(self)
		self.k = 0
		self.pressed = 2

	# If the start button has been pressed 
	# Checks if the mouse click collides with the image rect
	def button_pressed(self,button):
		#Handle the keyboard events
		for event in pygame.event.get():
			if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
				pos = pygame.mouse.get_pos()
				if button.collidepoint(pos):
					return 0
		return 1
	
	# For the backgound choices, click on a small image of the background
	def choose_button_pressed(self, blue, brown, green, pattern, s_snake):
		#Handle the keyboard events
		for event in pygame.event.get():
			if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
				pos = pygame.mouse.get_pos()
				# Check if the clicked mouse chose any of the correct locations
				if blue.collidepoint(pos):
					return -1 # Blue
				elif brown.collidepoint(pos):
					return -2 # Brown
				elif green.collidepoint(pos):
					return -3 # Green
				elif pattern.collidepoint(pos):
					return -4 # Patterned
				elif s_snake.collidepoint(pos):
					return -5 # Snake
		return 1

	# Blits the small choices of backgrounds to the screen and checks if any have been clicked
	def choose_background(self):
		self.screen.fill(self.black)

		# Choose background text
		self.screen.blit(self.text_back, [100, 1*GAME_HEIGHT/8])

		# Background choice options
		blue = self.screen.blit(self.blue_back, [GAME_WIDTH/6-OFFSET, 3*GAME_HEIGHT/8])
		brown = self.screen.blit(self.brown_back, [2*GAME_WIDTH/6-OFFSET, 3*GAME_HEIGHT/8])
		green = self.screen.blit(self.green_back, [3*GAME_WIDTH/6-OFFSET, 3*GAME_HEIGHT/8])
		pattern = self.screen.blit(self.pattern_back, [ 4*GAME_WIDTH/6-OFFSET, 3*GAME_HEIGHT/8])
		s_snake = self.screen.blit(self.snake_back, [5*GAME_WIDTH/6-OFFSET, 3*GAME_HEIGHT/8])
		
		pygame.display.flip() # double buffer animation system

		# Determine which background was chosen
		which_pressed = self.choose_button_pressed(blue,brown,green,pattern,s_snake)
		return which_pressed

	# Sets the background to the one the user chose
	def display_background(self):
		global CHOOSE
		if CHOOSE == -1:
			self.background = self.full_blue
		elif CHOOSE == -2:
			self.background = self.full_brown
		elif CHOOSE == -3:
			self.background = self.full_green
		elif CHOOSE == -4:
			self.background = self.full_pattern
		elif CHOOSE == -5:
			self.background = self.full_snake

	# Displays a start  screen
	# Gives background options
	# All before the server is connected to
	def start_players(self):
		global SNAKE1, SNAKE2, START, CHOOSE

		# Deal with the start screen
		while START:
			self.screen.blit(self.background, [-1000, -400])
			b = self.screen.blit(self.start_button, [75,400]) # Start button
			var = self.button_pressed(b) # If button was pressed
			START = var
			pygame.display.flip() # double buffer animation system
		
		# Wait for user to chose a background
		while CHOOSE > 0:
			CHOOSE = self.choose_background()

		# Blit background to the screen
		self.screen.blit(self.waiting_other, [130, 5*GAME_HEIGHT/8])
		pygame.display.flip() # double buffer animation system
		self.display_background() # Display the background once the server is connected

	#Whenever the snake is moved with a button press, this function handles it
	def move(self, pressed, player1, size):
		x=0
		y=0
		key = pygame.key.get_pressed()
		#Up button pressed
		if self.pressed == 1:
			x=0
			y=-1
			if self.player1.rect.top > 0:
				self.player1.rect.centery -= scale
			else:
				print "Out of bounds top" #Hit top of screen
				self.dead()
		#Down button pressed
		if self.pressed == 2:
			x=0
			y=1
			if self.player1.rect.bottom < size[1]:
				self.player1.rect.centery += scale
			else:
				print "Out of bounds bottom" #Hit bottom of screen
				self.dead()
		#Left button pressed
		if self.pressed == 3:
			x=-1
			y=0
			if self.player1.rect.left > 0:
				self.player1.rect.centerx -= scale
			else:
				print "Out of bounds left" #Hit left of screen
				self.dead()
		#Right button pressed
		if self.pressed == 4:
			x=1
			y=0
			if self.player1.rect.right < size[0]:
				self.player1.rect.centerx += scale
			else:
				print "Out of bounds right" #Hit right of screen
				print self.player1.rect.right
				self.dead()

		global SNAKE1
		t=SNAKE1[0] #Head of the snake
		t=(t[0]+x,t[1]+y) #Increment parts of snake
		SNAKE1.insert(0,t) #Insert new element in front of snake
		del SNAKE1[-1] #Delete the last element of the snake

		#Check if snake has run into himself
		if SNAKE1[0] in SNAKE1[1:]:
			print "Player is dead"
			self.dead()

	# The player has ran into themselves, the wall, or the other snake
	def dead(self):
		factory.connections["server"].sendLine("dead\r\n") # Send dead message

		# Load end screen images
		game_over = pygame.image.load("images/game_over.png")
		loser = pygame.image.load("images/loser.png")

		# Blit the images to the screen
		self.screen.fill(self.black)
		self.screen.blit(game_over, [120, 2*GAME_HEIGHT/8])
		self.screen.blit(loser, [GAME_WIDTH/2-OFFSET, 5*GAME_HEIGHT/8])
		pygame.display.flip() # double buffer animation system

		# Update variable to show dead
		global DEAD
		DEAD = 1

	# The other player has ran into themselves, the wall, or you
	def killed(self):
		# Load end screen images
		game_over = pygame.image.load("images/game_over.png")
		winner = pygame.image.load("images/winner.png")

		# Blit the images to the screen
		self.screen.fill(self.black)
		self.screen.blit(game_over, [120, 2*GAME_HEIGHT/8])
		self.screen.blit(winner, [GAME_WIDTH/2-OFFSET, 5*GAME_HEIGHT/8])
		pygame.display.flip() # double buffer animation system

		# Update the variable to show dead
		global DEAD
		DEAD = 1

	#Show the snake on the screen
	def draw_snake(self, player, snakeX):
		#Iterate through all the parts of the snake and show them on the screen
		for i in snakeX:
			rect = (i[0]*scale,i[1]*scale,scale-1,scale-1)
			self.screen.blit(player.image,rect)

	# Game loop
	def mainloop(self):

		#Handle the keyboard events
		for event in pygame.event.get():
			if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
				pygame.quit()
				os._exit(1)
			elif event.type == KEYDOWN:
				if event.key == K_UP:
					self.pressed = 1
				if event.key == K_DOWN:
					self.pressed = 2
				if event.key == K_LEFT:
					self.pressed = 3
				if event.key == K_RIGHT:
					self.pressed = 4

		global DEAD, SNAKE2
		if not DEAD:
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

			#Check you have run into the other snake
			if SNAKE1[0] in SNAKE2[0:]:
				print "You ran into the other snake"
				self.dead()

			#Check if the other snake has run into you
			if SNAKE2[0] in SNAKE1[0:]:
				print "The other snake ran into you"
				self.killed()
		
			#To check if apple needs to be respawned
			self.apple.tick()
			#Move the snake across the screen
			if self.k%5==0: 
				self.move(self.pressed,self.player1,self.size)
			if not DEAD:
				self.k+=1
				self.screen.blit(self.background, [0, 0])
				self.screen.blit(self.apple.image, self.apple.rect)
				self.draw_snake(self.player1, SNAKE1)
				self.draw_snake(self.player2, SNAKE2)

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
		elif "dead" in raw_data:
			print "OTHER PLAYER HAS DIED"
			gs.killed()

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
gs.start_players()
loop = LoopingCall(gs.mainloop)

reactor.connectTCP(HOST, PORT, factory)
reactor.run()

