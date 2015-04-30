from twisted.internet import reactor
from twisted.internet.protocol import Factory
from twisted.internet.protocol import Protocol

CLIENTPORT1 = 9082
CLIENTPORT2 = 9083
GAME_WIDTH = 640
GAME_HEIGHT = 960
SNAKE_WIDTH = 15*2
SNAKE_HEIGHT = 15*2

'''
HOST = 'student02.cse.nd.edu'
SERVERPORT = 22

class ServiceConnFactory(Factory):
	def __init__(self):
		self.connections = {}
		self.client1 = 0
		self.client2 = 0

	def buildProtocol(self, addr):
		return ServiceConnProtocol(self)
'''

class Server():
	def __init__(self):
		self.connections = {}
		self.client1 = 0
		self.client2 = 0

	def listen(self):
		reactor.listenTCP(CLIENTPORT1, ClientConnFactory1(self.connections, self.client1))
		reactor.listenTCP(CLIENTPORT2, ClientConnFactory2(self.connections, self.client2))

class ClientConnFactory1(Factory):
	def __init__(self, connections, client1):
		self.connections = connections
		self.client1 = client1
	def buildProtocol(self, addr):
		return ClientConnProtocol1(self)


class ClientConnProtocol1(Protocol):
	def __init__(self, factory):
		self.factory = factory

	def connectionMade(self):
		self.factory.client1 = 1
		self.factory.connections["client1"] = self
		self.factory.connections[self] = "client1"
		self.factory.connections["client1"].transport.write("Player 1 has entered the game.\nWaiting for player 2...")
		
	def connectionLost(self, reason):
		del self.factory.connections["client1"]
		print "Player 1 has left the game."
		#print "Lost connection:", reason

	def dataReceived(self, data):
		if data == "apple":
			x = randint(0+SNAKE_WIDTH, GAME_WIDTH-SNAKE_WIDTH)
			y = randint(0+SNAKE_HEIGHT, GAME_HEIGHT-SNAKE_WIDTH)
			self.apple_pos.x, self.apple_pos.y = x,y
			self.factory.connections["client1"].transport.write(self.apple.pos)
			self.factory.connections["client2"].transport.write(self.apple.pos)
		else:
			# Send player2 new position of player1
			print self.factory.connections[self], data
			self.factory.connections["client2"].transport.write(data)


class ClientConnFactory2(Factory):
	def __init__(self, connections, client2):
		self.connections = connections
		self.client2 = client2
	def buildProtocol(self, addr):
		return ClientConnProtocol2(self)

class ClientConnProtocol2(Protocol):
	def __init__(self, factory):
		self.factory = factory

	def connectionMade(self):
		self.factory.client2 = 1
		self.factory.connections["client2"] = self
		self.factory.connections[self] = "client2"
		self.factory.connections["client2"].transport.write("Player 2 has entered the game.")
		self.factory.connections["client1"].transport.write("Player 2 has entered the game.")
		
	def connectionLost(self, reason):
		del self.factory.connections["client2"]
		print "Player 2 has left the game."
		#print "Lost connection:", reason

	def dataReceived(self, data):
		if data == "apple":
			x = randint(0+SNAKE_WIDTH, GAME_WIDTH-SNAKE_WIDTH)
			y = randint(0+SNAKE_HEIGHT, GAME_HEIGHT-SNAKE_WIDTH)
			self.apple_pos.x, self.apple_pos.y = x,y
			self.factory.connections["client1"].transport.write(self.apple.pos)
			self.factory.connections["client2"].transport.write(self.apple.pos)
		else:
			# Send player1 new position of player2	
			print self.factory.connections[self], data
			self.factory.connections["client1"].transport.write(data)


if __name__ == '__main__':
	server = Server()
	server.listen()
	reactor.run()
