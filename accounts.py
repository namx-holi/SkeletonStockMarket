
class Account:
	def __init__(self, username, password):
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


	def get_funds(self):
		return self._funds
