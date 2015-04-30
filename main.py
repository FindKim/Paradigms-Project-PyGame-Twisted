import pygame
import time

class ServerMain:
	def __init__(self):
		self.server = ServerState()

	def start_from_client(self):
		self.serverstate.setup_network()

	def start_from_server(self):
		self.serverstate.setup_network()
		self.serverstate.run_network()
