
class Account:
	def __init__(self, username=None, password=None, account_dict=None):
		if account_dict:
			self._username = account_dict["username"]
			self._password = account_dict["password"]
			self._funds = account_dict["funds"]
			self._owned_stocks = account_dict["owned_stocks"]
		else:
			self._username = username
			self._password = hash(password) # TODO: Better this
			self._funds = 0
			self._owned_stocks = []


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
		if stock["stockID"] not in self._owned_stocks.keys():
			return False
		if self._owned_stocks[stock["stockID"]] < quantity:
			return False

		self._owned_stocks[stock["stockID"]] -= quantity
		if self._owned_stocks[stock["stockID"]] == 0:
			del self._owned_stocks[stock["stockID"]]

		self._funds += stock["Price"] * quantity


	def get_username(self):
		return self._username


	def check_password(self, password_hash):
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
