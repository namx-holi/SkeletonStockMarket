
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


	def _login_check(self, data):
		if data["auth_token"]:
			for account in self._accounts:
				if account.check_auth_token(data["auth_token"]):
					return True
			return False
		return False


	def _sell(self, data):
		if len(data["args"].split(" ", 1)) == 1:
			stock_id = data["args"]
			quantity = 1
		else:
			stock_id, quantity_str = data["args"].split(" ", 1)
			try:
				quantity = int(quantity_str)
			except:
				return dict(
					response=None,
					error=True,
					error_text="Please use 'sell STOCK_ID [QUANTITY]'")

		result_stocks = self._market.get_stocks(stock_id)
		if len(result_stocks) > 1:
			return dict(
				response=None,
				error=True,
				error_text="Ambiguous stock name")
		elif len(result_stocks) == 0:
			return dict(
				response=None,
				error=True,
				error_text="No stock found by name '{}'".format(stock_id.upper()))

		for account in self._accounts:
			if account.check_auth_token(data["auth_token"]):
				did_sell = account.sell_stocks(result_stocks[0], quantity)

				if did_sell:
					return dict(
						response="Sold {} of {}".format(quantity, stock_id.upper()),
						error=False,
						error_text="")
				else:
					return dict(
						response=None,
						error=True,
						error_text="Not enough stocks of {} to sell {}".format(
							stock_id.upper(), quantity))
		return dict(
			response=None,
			error=True,
			error_text="Account not found.")


	def _buy(self, data):
		if len(data["args"].split(" ", 1)) == 1:
			stock_id = data["args"]
			quantity = 1
		else:
			stock_id, quantity_str = data["args"].split(" ", 1)
			try:
				quantity = int(quantity_str)
			except:
				return dict(
					response=None,
					error=True,
					error_text="Please use 'buy STOCK_ID [QUANTITY]'")

		result_stocks = self._market.get_stocks(stock_id)
		if len(result_stocks) > 1:
			return dict(
				reponse=None,
				error=True,
				error_text="Ambiguous stock name")
		elif len(result_stocks) == 0:
			return dict(
				response=None,
				error=True,
				error_text="No stock found by name '{}'".format(stock_id.upper()))

		for account in self._accounts:
			if account.check_auth_token(data["auth_token"]):
				did_buy = account.buy_stocks(result_stocks[0], quantity)

				if did_buy:
					return dict(
						response="Bought {} of {}".format(quantity, stock_id.upper()),
						error=False,
						error_text="")
				else:
					return dict(
						response=None,
						error=True,
						error_text="Not enough funds to buy {} of {}".format(
							quantity, stock_id.upper()))

		return dict(
			response=None,
			error=True,
			error_text="Account not found.")


	def _get(self, data):
		stocks = self._market.get_stocks(data["args"])

		if len(stocks):
			return dict(
				response=stocks,
				error=False,
				error_text="")
		else:
			return dict(
				response=[],
				error=True,
				error_text="No stocks by name '{}'".format(data["args"]))


	def _create_user(self, data):
		if len(data["args"].split(" ", 1)) > 1:
			username, password = data["args"].split(" ", 1)

			# check if username already exists
			for account in self._accounts:
				if account.get_username().lower() == username.lower():
					return dict(
						response=None,
						error=True,
						error_text="Username already exists")


			new_account = Account(username, password)
			self._accounts.append(new_account)

			return dict(
				response="Account created",
				error=False,
				error_text="")

		else:
			return dict(
				response=None,
				error=True,
				error_text="Please use 'createuser USERNAME PASSWORD'")


	def _login(self, data):
		if len(data["args"].split(" ", 1)) > 1:
			username, password = data["args"].split(" ", 1)

			# check if username exists
			for account in self._accounts:
				if account.get_username().lower() == username.lower():

					# try log in
					if account.check_password(password):
						auth_token = account.get_new_auth_token()
						return dict(
							response=dict(
								msg="Logged in as {}".format(username),
								auth_token=auth_token),
							error=False,
							error_text="")

					else:
						return dict(
							response=None,
							error=True,
							error_text="Incorrect password")

			return dict(
				response=None,
				error=True,
				error_text="Username does not exist")
		else:
			return dict(
				response=None,
				error=True,
				error_text="Please use 'login USERNAME PASSWORD'")


	def _logout(self, data):
		for account in self._accounts:
			if account.check_auth_token(data["auth_token"]):
				account.logout()
				return dict(
					response="You have been logged out.",
					error=False,
					error_text="")
		return dict(
			response="",
			error=True,
			error_text="You are not logged in.")


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
