
import accounts


class requestHandler:
	
	def __init__(self, accounts, market):
		self._accounts = accounts
		self._market = market


	def get_accounts:
		return self._accounts


	def get_market:
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
