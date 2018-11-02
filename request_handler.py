
class requestHandler:
	
	def __init__(self, accounts):
		self._accounts = accounts


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


	def login(self, data):

		# Log out user trying to sign in if they are logged in already
		current_user = self.get_user(data)
		if current_user:
			current_user.logout()

		if len(data["args"].split(" ", 1)) != 2:
			return self._err("Please use 'login USERNAME PASSWORD'")

		username, password = data["args"].split(" ", 1)

		for account in self._accounts:
			if account.get_username().lower() == username.lower():
				if account.check_password(password):
					auth_token = account.get_new_auth_token()
					return self._msg("Logged in as {}".format(username), auth_token)
				else:
					return self._err("Incorrect password")

		return self._err("Username does not exist")


	def logout(self, data):
		current_user = self.get_user(data)
		if current_user:
			current_user.logout()
			return self._msg("You have been logged out")
		else:
			return self._err("You are not logged in")