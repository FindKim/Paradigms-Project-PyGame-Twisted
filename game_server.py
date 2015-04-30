from twisted.internet import reactor
from twisted.protocols.basic import LineReceiver
from twisted.internet.protocol import Factory
from twisted.internet.protocol import Protocol

from random import randint

CLIENTPORT1 = 9082
CLIENTPORT2 = 9083
GAME_WIDTH = 640
GAME_HEIGHT = 960
SNAKE_WIDTH = 15
SNAKE_HEIGHT = 15

CLIENT1 = 0
CLIENT2 = 0
APPLE = ["apple", 0, 0]
POS1 = ["position", GAME_WIDTH/3, GAME_HEIGHT/2]
POS2 = ["position", GAME_WIDTH*2/3, GAME_HEIGHT/2]
X = 1
Y = 2

class Server():
	def __init__(self):
		self.connections = {}

	def listen(self):
		reactor.listenTCP(CLIENTPORT1, ClientConnFactory1(self.connections))
		reactor.listenTCP(CLIENTPORT2, ClientConnFactory2(self.connections))

class ClientConnFactory1(Factory):
	def __init__(self, connections):
		self.connections = connections
	def buildProtocol(self, addr):
		self.protocol = ClientConnProtocol1(self)
		return self.protocol


class ClientConnProtocol1(LineReceiver):
	def __init__(self, factory):
		self.factory = factory
	
	def concat_list(self, data):
		return data[0] + ',' + str(data[X]) + ',' + str(data[Y]) + '\r\n'

	def connectionMade(self):
		global CLIENT1, CLIENT2
		CLIENT1 = 1
		print "Player 1 has entered the game."
		self.factory.connections["client1"] = self
		self.factory.connections[self] = "client1"
		
		# Start game when both players are connected
		if CLIENT1 and CLIENT2:
		
			# Initialize player starting positions
			init_pos1 = "start," + str(POS1[X]) + ',' + str(POS1[Y]) + '\r\n'
			init_pos2 = self.concat_list(POS2)
			self.factory.connections["client1"].sendLine(init_pos1)
			self.factory.connections["client1"].sendLine(init_pos2)
			init_pos1 = self.concat_list(POS1)
			init_pos2 = "start," + str(POS2[X]) + ',' + str(POS2[Y]) + '\r\n'
			self.factory.connections["client1"].sendLine(init_pos1)
			self.factory.connections["client2"].sendLine(init_pos2)
			
			# Initialize randomized apple position
			global APPLE
			x = randint(0+SNAKE_WIDTH*2, GAME_WIDTH-SNAKE_WIDTH*2)
			y = randint(0+SNAKE_HEIGHT*2, GAME_HEIGHT-SNAKE_HEIGHT*2)
			APPLE[X] = x
			APPLE[Y] = y
			apple_pos = self.concat_list(APPLE)
			print apple_pos
			self.factory.connections["client1"].sendLine(apple_pos)
			self.factory.connections["client2"].sendLine(apple_pos)
		
	def connectionLost(self, reason):
		del self.factory.connections["client1"]
		CLIENT1 = 0
		print "Player 1 has left the game."
		#print "Lost connection:", reason

	def lineReceived(self, raw_data):
		data = raw_data.strip()
		data = data.split(',')

		# Apple was eaten, spawn new apple and send to clients pos
		if "apple" in raw_data:
			global APPLE
			x = randint(0+SNAKE_WIDTH*2, GAME_WIDTH-SNAKE_WIDTH*2)
			y = randint(0+SNAKE_HEIGHT*2, GAME_HEIGHT-SNAKE_HEIGHT*2)
			APPLE[X] = x
			APPLE[Y] = y
			apple_pos = self.concat_list(APPLE)
			print apple_pos
			self.factory.connections["client1"].sendLine(apple_pos)
			self.factory.connections["client2"].sendLine(apple_pos)

		# Send Player 2 new position of Player 1
		elif data[0] == "position":
			pos = self.concat_list(data)
			self.factory.connections["client2"].sendLine(pos)




class ClientConnFactory2(Factory):
	def __init__(self, connections):
		self.connections = connections
	def buildProtocol(self, addr):
		return ClientConnProtocol2(self)

class ClientConnProtocol2(LineReceiver):
	def __init__(self, factory):
		self.factory = factory
	
	def concat_list(self, data):
		return data[0] + ',' + str(data[X]) + ',' + str(data[Y]) + '\r\n'

	def connectionMade(self):
		global CLIENT1, CLIENT2
		CLIENT2 = 1
		print "Player 2 has entered the game."
		self.factory.connections["client2"] = self
		self.factory.connections[self] = "client2"
		
		# Start game when both players are connected
		if CLIENT1 and CLIENT2:
		
			# Initialize player starting positions
			init_pos1 = "start," + str(POS1[X]) + ',' + str(POS1[Y]) + '\r\n'
			init_pos2 = self.concat_list(POS2)
			self.factory.connections["client1"].sendLine(init_pos1)
			self.factory.connections["client1"].sendLine(init_pos2)
			init_pos1 = self.concat_list(POS1)
			init_pos2 = "start," + str(POS2[X]) + ',' + str(POS2[Y]) + '\r\n'
			self.factory.connections["client1"].sendLine(init_pos1)
			self.factory.connections["client2"].sendLine(init_pos2)
			
			# Initialize randomized apple position
			global APPLE
			x = randint(0+SNAKE_WIDTH*2, GAME_WIDTH-SNAKE_WIDTH*2)
			y = randint(0+SNAKE_HEIGHT*2, GAME_HEIGHT-SNAKE_HEIGHT*2)
			APPLE[X] = x
			APPLE[Y] = y
			apple_pos = self.concat_list(APPLE)
			print apple_pos
			self.factory.connections["client1"].sendLine(apple_pos)
			self.factory.connections["client2"].sendLine(apple_pos)
		
	def connectionLost(self, reason):
		del self.factory.connections["client2"]
		CLIENT2 = 0
		print "Player 2 has left the game."
		#print "Lost connection:", reason

	def lineReceived(self, raw_data):
		data = raw_data.strip()
		data = data.split(',')

		# Apple was eaten, spawn new apple and send to clients pos
		if "apple" in raw_data:
			global APPLE
			x = randint(0+SNAKE_WIDTH*2, GAME_WIDTH-SNAKE_WIDTH*2)
			y = randint(0+SNAKE_HEIGHT*2, GAME_HEIGHT-SNAKE_HEIGHT*2)
			APPLE[X] = x
			APPLE[Y] = y
			apple_pos = self.concat_list(APPLE)
			print apple_pos
			self.factory.connections["client1"].sendLine(apple_pos)
			self.factory.connections["client2"].sendLine(apple_pos)

		# Send Player 1 new position of Player 2
		elif data[0] == "position":
			pos = self.concat_list(data)
			self.factory.connections["client1"].sendLine(pos)


if __name__ == '__main__':
	server = Server()
	server.listen()
	reactor.run()
