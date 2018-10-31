
import socket
import threading
import json

from settings import server_settings as server_cfg
from settings import market_settings as market_cfg

import stockmarket


class Server:
	def __init__(self, bind_ip, bind_port):
		self._bind_ip = bind_ip
		self._bind_port = bind_port
		self._server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self._server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
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
		request = client_socket.recv(1024).decode()
		print("Received {} command".format(request))

		data = json.loads(request)

		if data["command"].lower() == "get":
			stocks = self._market.get_stocks(data["args"])

			if len(stocks):
				response = dict(
					response=stocks,
					error=False,
					error_text=""
				)
			else:
				response = dict(
					response=[],
					error=True,
					error_text="No stocks by name '{}'".format(data["args"])
				)

		else:
			response = dict(
				response=None,
				error=True,
				error_text="No command for {}".format(data["command"])
			)

		client_socket.send(json.dumps(response).encode())
		client_socket.close()


	def start(self):
		self._server.listen(5)
		self._listen_func()
		self._server.shutdown(socket.SHUT_RDWR)
		self._server.close()



if __name__ == "__main__":
	market = stockmarket.Stockmarket(market_cfg.stock_types_filepath)
	server = Server(server_cfg.bind_ip, server_cfg.bind_port)

	server.bind_market(market)

	server.start()
