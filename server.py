
import socket
import threading

from settings import server_settings as server_cfg
from settings import market_settings as market_cfg

import stockmarket


class Server:
	def __init__(self, bind_ip, bind_port):
		self._bind_ip = bind_ip
		self._bind_port = bind_port
		self._server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self._server.bind((bind_ip, bind_port))


	def bind_market(self, market):
		self._market = market


	def _listen_func(self):
		print("Listening on {}:{}".format(self._bind_ip, self._bind_port))
		while True:
			try:
				client_sock, address = self._server.accept()
			except KeyboardInterrupt:
				print("\rEnding server...")
				return

			print("Accepted connection from {}:{}".format(address[0], address[1]))
			client_handler = threading.Thread(
				target=self._handle_func,
				args=[client_sock]
			)
			client_handler.start()


	def _handle_func(self, client_socket):
		request = client_socket.recv(1024)
		print("Received {} command".format(request))

		# TODO: Handle things here!
		client_socket.send("TODO: Handle {}".format(request).encode())

		client_socket.close()


	def start(self):
		self._server.listen(5)
		self._listen_func()
		self._server.close()



if __name__ == "__main__":
	market = stockmarket.Stockmarket(market_cfg.stock_types_filepath)
	server = Server(server_cfg.bind_ip, server_cfg.bind_port)

	server.bind_market(market)

	server.start()
