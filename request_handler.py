
import accounts


class requestHandler:
	
	def __init__(self, accounts=None, market=None):
		self._accounts = accounts if accounts else None
		self._market = market if accounts else None


	def bind_accounts(self, accounts):
		self._accounts = accounts


	def bind_market(self, market):
		self._market = market


	def get_accounts(self):
		return self._accounts


	def get_market(self):
		return self._market


	def _err(self, error_text):
		return dict(
			msg=None,
			data=None,
			error=True,
			error_text=error_text)


	def _msg(self, msg, data=None):
		return dict(
			msg=msg,
			data=data,
			error=False,
			error_text=None)


	def handle_data(self, data):
		if "command" not in data.keys():
			return self._err("Missing command in request")
		elif "args" not in data.keys():
			return self._err("Missing args in request")

		command = data["command"].lower()
		if command == "createuser":
			return self.create_user(data)
		elif command == "login":
			return self.login(data)
		elif command == "logout":
			return self.logout(data)
		elif command == "get":
			return self.get_stocks(data)
		elif command == "buy":
			return self.buy_stocks(data)
		elif command == "sell":
			return self.sell_stocks(data)

		else:
			return self._err("No command for {}".format(command))


	def get_user(self, data):
		if not data["auth_token"]:
			return None

		for account in self._accounts:
			if account.check_auth_token(data["auth_token"]):
				return account

		return None


	def get_user_by_username(self, username):
		for account in self._accounts:
			if account.get_username().lower() == username.lower():
				return account
		return None


	def create_user(self, data):
		if len(data["args"].split(" ", 1)) != 2:
			return self._err("Please use 'createuser USERNAME PASSWORD'")

		if self.get_user_by_username:
			return self._err("User alread exists")

		new_account = accounts.Account(username, password)
		self._accounts.append(new_account)

		return self._msg("Account created")


	def login(self, data):
		current_user = self.get_user(data)
		if current_user:
			current_user.logout()

		if len(data["args"].split(" ", 1)) != 2:
			return self._err("Please use 'login USERNAME PASSWORD'")

		username, password = data["args"].split(" ", 1)
		account = self.get_user_by_username(username)

		if not account:
			return self._err("Username does not exist")

		if account.check_password(password):
			auth_token = account.get_new_auth_token()
			return self._msg("Logged in as {}".format(username), auth_token)
		else:
			return self._err("Incorrect password")


	def logout(self, data):
		current_user = self.get_user(data)
		if current_user:
			current_user.logout()
			return self._msg("You have been logged out")
		else:
			return self._err("You are not logged in")


	def get_stocks(self, data):
		current_user = self.get_user(data)
		if not current_user:
			return self._err("You must be logged in to view stocks")

		stocks = self._market.get_stocks(data["args"])

		if len(stocks):
			return self._msg("", data=stocks)
		else:
			return self._err("No stocks by name '{}'".format(data["args"].upper()))


	def buy_stocks(self, data):
		current_user = self.get_user(data)
		if not current_user:
			return self._err("You must be logged in to buy stocks")

		if len(data["args"].split(" ", 1)) == 1:
			stock_id = data["args"]
			quantity = 1
		else:
			stock_id, quantity_str = data["args"].split(" ", 1)
			try:
				quantity = int(quantity_str)
			except ValueError:
				return self._err("Please use 'buy STOCK_ID [QUANTITY]'")

		stocks = self._market.get_stocks(stock_id)
		if len(stocks) == 0:
			return self._err("No stock by name '{}'".format(data["args"].upper()))
		elif len(stocks) > 1:
			return self._err("Ambiguous stock name")

		did_buy = current_user.buy_stocks(stocks[0], quantity)
		if did_buy:
			return self._msg("Bought {} of {}".format(quantity, stock_id.upper()))
		else:
			return self._err("Not enough funds to buy {} of {}".format(
				quantity, stock_id.upper()))


	def sell_stocks(self, data):
		current_user = self.get_user(data)
		if not current_user:
			return self._err("You must be logged in to sell stocks")

		if len(data["args"].split(" ", 1)) == 1:
			stock_id = data["args"]
			quantity = 1
		else:
			stock_id, quantity_str = data["args"].split(" ", 1)
			try:
				quantity = int(quantity_str)
			except ValueError:
				return self._err("Please use 'sell STOCK_ID [QUANTITY]'")

		stocks = self._market.get_stocks(stock_id)
		if len(stocks) == 0:
			return self._err("No stock by name '{}'".format(data["args"].upper()))
		elif len(stocks) > 1:
			return self._err("Ambiguous stock name")

		did_sell = current_user.sell_stocks(stocks[0], quantity)
		if did_sell:
			return self._msg("Sold {} of {}".format(quantity, stock_id.upper()))
		else:
			return self._err("Not enough of stock {} to sell {}".format(
				stock_id.upper(), quantity))
