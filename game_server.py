from twisted.internet import reactor
from twisted.protocols.basic import LineReceiver
from twisted.internet.protocol import Factory
from twisted.internet.protocol import Protocol

from random import randint

CLIENTPORT1 = 9082
CLIENTPORT2 = 9083
GAME_WIDTH = 640
GAME_HEIGHT = 640
SNAKE_WIDTH = 15
SNAKE_HEIGHT = 15
SCALE = 15

CLIENT1 = 0
CLIENT2 = 0
APPLE = ["apple", 0, 0]
POS1 = ["position", 5*SCALE, 5*SCALE]
POS2 = ["position", 5*SCALE, 5*SCALE]
X = 1
Y = 2

SNAKE1 = [(5,5),(5,4),(5,3),(5,2),(5,1)]
SNAKE2=[(5,5),(5,4),(5,3),(5,2),(5,1)]

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
		string = str()
		for item in data:
			string = string + str(item) + ','
		string = string.strip(',')
		return string + '\r\n'

	def concat_tup(self, header, list_tup):
		string = header + ','
		for tup in list_tup:
			for item in tup:
				string = string + str(item) + ','
		string = string.strip(',')
		return string + '\r\n'

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
			print "player 1:", init_pos1, ",", init_pos2
			init_pos1 = self.concat_list(POS1)
			init_pos2 = "start," + str(POS2[X]) + ',' + str(POS2[Y]) + '\r\n'
			self.factory.connections["client2"].sendLine(init_pos1)
			self.factory.connections["client2"].sendLine(init_pos2)
			print "player 2:", init_pos1, ",", init_pos2

			
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
		global SNAKE1
		data = raw_data.strip()
		data = data.split(',')

		# Apple was eaten, spawn new apple and send to clients pos
		if "apple" in raw_data:
			global APPLE
			print "Player 1 has eaten the apple"
			x = randint(0+SNAKE_WIDTH*2, GAME_WIDTH-SNAKE_WIDTH*2)
			y = randint(0+SNAKE_HEIGHT*2, GAME_HEIGHT-SNAKE_HEIGHT*2)
			APPLE[X] = x
			APPLE[Y] = y
			apple_pos = self.concat_list(APPLE)
			print apple_pos
			self.factory.connections["client1"].sendLine(apple_pos)
			self.factory.connections["client2"].sendLine(apple_pos)
			SNAKE1.append(SNAKE1[-1])
			snake_str1 = ",".join("%s,%s" % tup for tup in SNAKE1)
			my_snake = "my_snake," + snake_str1
			other_snake = "other_snake," + snake_str1
			self.factory.connections["client1"].sendLine(my_snake)
			self.factory.connections["client2"].sendLine(other_snake)

		# Send Player 2 new position of Player 1
		elif data[0] == "position":
			pos = self.concat_list(data)
			self.factory.connections["client2"].sendLine(pos)
		elif data[0] == "snake":
			self.factory.connections["client2"].sendLine(raw_data)



class ClientConnFactory2(Factory):
	def __init__(self, connections):
		self.connections = connections
	def buildProtocol(self, addr):
		return ClientConnProtocol2(self)

class ClientConnProtocol2(LineReceiver):
	def __init__(self, factory):
		self.factory = factory
	
	def concat_list(self, data):
		string = str()
		for item in data:
			string = string + str(item) + ','
		string = string.strip(',')
		return string + '\r\n'
		#return data[0] + ',' + str(data[X]) + ',' + str(data[Y]) + '\r\n'

	def concat_tup(self, header, list_tup):
		string = header + ','
		for tup in list_tup:
			for item in tup:
				string = string + str(item) + ','
		string = string.strip(',')
		return string + '\r\n'

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
			self.factory.connections["client2"].sendLine(init_pos1)
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
		global SNAKE2
		data = raw_data.strip()
		data = data.split(',')

		# Apple was eaten, spawn new apple and send to clients pos
		if "apple" in raw_data:
			global APPLE
			print "Player 2 has eaten the apple"
			x = randint(0+SNAKE_WIDTH*2, GAME_WIDTH-SNAKE_WIDTH*2)
			y = randint(0+SNAKE_HEIGHT*2, GAME_HEIGHT-SNAKE_HEIGHT*2)
			APPLE[X] = x
			APPLE[Y] = y
			apple_pos = self.concat_list(APPLE)
			print apple_pos
			self.factory.connections["client1"].sendLine(apple_pos)
			self.factory.connections["client2"].sendLine(apple_pos)
			SNAKE2.append(SNAKE2[-1])
			snake_str2 = ",".join("%s,%s" % tup for tup in SNAKE2)
			my_snake = "my_snake," + snake_str2
			other_snake = "other_snake," + snake_str2
			self.factory.connections["client1"].sendLine(other_snake)
			self.factory.connections["client2"].sendLine(my_snake)

		# Send Player 1 new position of Player 2
		elif data[0] == "position":
			pos = self.concat_list(data)
			print pos
			self.factory.connections["client1"].sendLine(pos)
		elif data[0] == "snake":
			self.factory.connections["client1"].sendLine(raw_data)
			



if __name__ == '__main__':
	server = Server()
	server.listen()
	reactor.run()
