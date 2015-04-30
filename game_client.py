from twisted.internet.protocol import Factory
from twisted.internet.protocol import ClientFactory
from twisted.internet.protocol import Protocol
from twisted.internet import reactor
import sys

HOST = 'student02.cse.nd.edu'
try:
	PORT = int(sys.argv[1])
except IndexError:
	print 'Usage:', sys.argv[0], '[port 9082/9083]'
	sys.exit()

class ClientConnFactory(ClientFactory):
	def __init__(self):
		self.connections = {}
	def buildProtocol(self, addr):
		return ClientConnProtocol(self)

class ClientConnProtocol(Protocol):
	def __init__(self, factory):
		self.factory = factory

	def connectionMade(self):
		self.factory.connections["server"] = self
		#while 1:
		#	user_input = sys.stdin.read(1)
		#	self.factory.connections["server"].transport.write(user_input)

	def connectionLost(self, reason):
		del self.factory.connections["server"]
		print "Lost connection:", reason

	def dataReceived(self, data):
		return data

'''
if __name__ == '__main__':
	reactor.connectTCP(HOST, PORT, ClientConnFactory())
	reactor.run()
'''
