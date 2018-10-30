
import numpy as np
import random
import json

import stock_settings as cfg

# TODO: Import these from JSON
# stock_types = [
# 	dict(stockID="BNS", name="Bones", Price=100),
# 	dict(stockID="BBN", name="Baby Bones", Price=350),
# 	dict(stockID="BIG", name="Big Bones", Price=550),
# 	dict(stockID="DBN", name="Dry Bones", Price=275)
# ]


class Stockmarket:

	def __init__(self, stock_types_filepath):
		with open(stock_types_filepath, "r") as stream:
			data = json.load(stream)

		stocks = []
		for stock in data:
			stock["Price"] = stock["StartingPrice"]
			stock["PriceHistory"] = [stock["StartingPrice"]]

			stock["AllTimeHigh"] = stock["StartingPrice"]
			stock["AllTimeLow" ] = stock["StartingPrice"]

			stock["Change"] = 0.0

			del stock["StartingPrice"]
			stocks.append(stock)

		self._stocks = stocks
		self._stdev = cfg.stdev
		self._mean = cfg.mean

		self._time_ticks = 0
		self._update_period = cfg.update_period


	def _shuffle_params(self):
		# TODO: Do something to stdev and mean
		pass


	def _calculate_next_price(self, price):
		r = np.random.normal(0, 1, 1)
		next_price = price * (
			1 +
			self._mean/255 +
			r * self._stdev / np.sqrt(225))
		return next_price


	def _update_stocks(self):
		for stock in self._stocks:
			next_price = self._calculate_next_price(stock["Price"])

			if next_price < stock["AllTimeLow"]:
				stock["AllTimeLow"] = next_price
			elif next_price > stock["AllTimeHigh"]:
				stock["AllTimeHigh"] = next_price

			stock["Change"] = next_price / stock["Price"]

			stock["Price"] = next_price

	def update(self):
		self._time_ticks += 1
		if self._time_ticks % self._update_period:
			self._shuffle_params()

		self._update_stocks()
