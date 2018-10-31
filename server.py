
import socket
import threading
import json

from settings import server_settings as server_cfg
from settings import market_settings as market_cfg

import stockmarket
import accounts


class Server:
	def __init__(self, bind_ip, bind_port):
		self._bind_ip = bind_ip
		self._bind_port = bind_port
		self._server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self._server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self._server.bind((bind_ip, bind_port))
		self._accounts = []


	def bind_market(self, market):
		self._market = market


	def load_accounts(self, accounts_filepath):
		self._accounts_filepath = accounts_filepath

		try:
			with open(accounts_filepath, "r") as stream:
				data = json.load(stream)
		except FileNotFoundError:
			return

		for account in data:
			self._accounts.append(accounts.Account(account_dict=account))


	def save_accounts(self):
		if not self._accounts_filepath:
			return

		data = []
		for account in self._accounts:
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

		elif data["command"].lower() == "createuser":
			if len(data["args"].split(" ", 1)) > 1:
				username, password = data["args"].split(" ", 1)

				new_account = accounts.Account(username, password)
				self._accounts.append(new_account)

				response = dict(
					response="Account created",
					error=False,
					error_text=""
				)

			else:
				response = dict(
					response=None,
					error=True,
					error_text="Please use 'createuser USERNAME PASSWORD"
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
		self._market.start_update_thread()
		self._server.listen(5)
		self._listen_func()

		self._market.stop_update_thread()
		self.save_accounts()
		self._server.shutdown(socket.SHUT_RDWR)
		self._server.close()



if __name__ == "__main__":
	market = stockmarket.Stockmarket(market_cfg.stock_types_filepath)
	server = Server(server_cfg.bind_ip, server_cfg.bind_port)

	server.load_accounts(server_cfg.accounts_filepath)
	server.bind_market(market)

	server.start()
