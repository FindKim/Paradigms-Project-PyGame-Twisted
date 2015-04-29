from twisted.internet import reactor
from twisted.internet.protocol import Factory
from twisted.internet.protocol import Protocol

CLIENTPORT1 = 9082
CLIENTPORT2 = 9083

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
		reactor.listenTCP(CLIENTPORT1, ClientConnFactory(self.factory.connections, self.client1, self.client2))
		reactor.listenTCP(CLIENTPORT2, ClientConnFactory(self.factory.connections, self.client1, self.client2))



class ClientConnFactory(Factory):
	def __init__(self, connections, client1, client2):
		self.connections = connections
		self.client1 = client1
		self.client2 = client2
	def buildProtocol(self, addr):
		return ClientConnProtocol(self)

class ClientConnProtocol(Protocol):
	def __init__(self, factory):
		self.factory = factory

	def connectionMade(self):
		if not self.client1:
			self.client1 = 1
			self.factory.connections["client1"] = self
		else:
			self.client2 = 1
			self.factory.connections["client2"] = self
		self.factory.connections["command"].transport.write("Connected to server")
		
	def connectionLost(self, reason):
		if self == self.factory.connections["client1"]:
			del self.factory.connections["client1"]
		else:
			del self.factory.connections["client2"]
		print "Lost connection:", reason

	#def dataReceived(self, data):
	# send user key strokes to game server	


if __name__ == '__main__':
	self.server = Server()
	self.server.listen()
	reactor.run()
