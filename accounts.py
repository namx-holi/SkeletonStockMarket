
import hashlib
import uuid

class Account:
	def __init__(self, username=None, password=None, account_dict=None):
		if account_dict:
			self._username = account_dict["username"]
			self._password = account_dict["password"]
			self._funds = account_dict["funds"]
			self._owned_stocks = account_dict["owned_stocks"]
		else:
			self._username = username
			self._password = hashlib.sha256(password.encode()).hexdigest()
			self._funds = 10000
			self._owned_stocks = {}
		self._logged_in = False
		self._auth_token = None


	def buy_stocks(self, stock, quantity=1):
		if stock["Price"] * quantity > self._funds:
			return False

		if stock["stockID"] in self._owned_stocks.keys():
			self._owned_stocks[stock["stockID"]] += quantity
		else:
			self._owned_stocks[stock["stockID"]] = quantity

		self._funds -= stock["Price"] * quantity

		return True


	def sell_stocks(self, stock, quantity=1):
		print(self._owned_stocks)
		print(stock["stockID"])

		if stock["stockID"] not in self._owned_stocks.keys():
			return False
		if self._owned_stocks[stock["stockID"]] < quantity:
			return False

		self._owned_stocks[stock["stockID"]] -= quantity
		if self._owned_stocks[stock["stockID"]] == 0:
			del self._owned_stocks[stock["stockID"]]

		self._funds += stock["Price"] * quantity

		return True


	def get_username(self):
		return self._username


	def check_password(self, password):
		password_hash = hashlib.sha256(password.encode()).hexdigest()
		return self._password == password_hash


	def get_funds(self):
		return self._funds


	def to_dict(self):
		account_dict = dict(
			username=self._username,
			password=self._password,
			funds=self._funds,
			owned_stocks=self._owned_stocks
		)

		return account_dict


	# TODO: Combine this with check_password to create login function
	def get_new_auth_token(self):
		auth_token = uuid.uuid4().hex
		self._auth_token = auth_token
		self._logged_in = True
		return auth_token


	def check_auth_token(self, auth_token):
		if not self._auth_token:
			return False
		return self._auth_token == auth_token


	def is_logged_in(self):
		return self._logged_in


	def logout(self):
		self._logged_in = False
		self._auth_token = None