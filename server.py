
import socket
import threading
import json

from settings import server_settings as server_cfg
from settings import market_settings as market_cfg

import stockmarket

from accounts import Account
from request_handler import requestHandler


class Server:
	def __init__(self, bind_ip, bind_port):
		self._bind_ip = bind_ip
		self._bind_port = bind_port
		self._server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self._server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self._server.bind((bind_ip, bind_port))
		self._handler = requestHandler()


	def bind_market(self, market):
		self._handler.bind_market(market)


	def load_accounts(self, accounts_filepath):
		self._accounts_filepath = accounts_filepath

		try:
			with open(accounts_filepath, "r") as stream:
				data = json.load(stream)
		except FileNotFoundError:
			return

		account_list = []
		for account in data:
			account_list.append(Account(account_dict=account))
		self._handler.bind_accounts(account_list)


	def save_accounts(self):
		if not self._accounts_filepath:
			return

		data = []
		account_list = self._handler.get_accounts()
		for account in account_list:
			data.append(account.to_dict())

		with open(self._accounts_filepath, "w") as stream:
			json.dump(data, stream, indent=4, sort_keys=True)


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
				target=self._handle_request,
				args=[client_sock]
			)
			client_handler.start()


	def _handle_request(self, client_socket):
		request = client_socket.recv(1024).decode()
		print("Received {} command".format(request))

		data = json.loads(request)

		response = self._handler.handle_data(data)

		client_socket.send(json.dumps(response).encode())
		client_socket.close()


	def start(self):
		self._handler.get_market().start_update_thread()
		self._server.listen(5)
		self._listen_func()

		self._handler.get_market().stop_update_thread()
		self.save_accounts()
		self._server.shutdown(socket.SHUT_RDWR)
		self._server.close()



if __name__ == "__main__":
	market = stockmarket.Stockmarket(market_cfg.stock_types_filepath)
	server = Server(server_cfg.bind_ip, server_cfg.bind_port)

	server.load_accounts(server_cfg.accounts_filepath)
	server.bind_market(market)

	server.start()
