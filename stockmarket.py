
import numpy as np
import random
import json

from settings import market_settings as cfg

# TODO: Method/class comments


class Stockmarket:

	def __init__(self, stock_types_filepath):
		with open(stock_types_filepath, "r") as stream:
			data = json.load(stream)

		stocks = []
		for stock in data:
			stock["Price"] = stock["startingPrice"]
			stock["PriceHistory"] = [stock["startingPrice"]]

			stock["AllTimeHigh"] = stock["startingPrice"]
			stock["AllTimeLow" ] = stock["startingPrice"]

			stock["Change"] = 0.0

			del stock["startingPrice"]
			stocks.append(stock)

		self._stocks = stocks
		self._stdev = cfg.stdev
		self._mean = cfg.mean

		self._price_history_len = cfg.price_history_len
		self._update_period = cfg.update_period
		self._time_elapsed = 0

		# Update the stocks a few times 
		for t in range(self._price_history_len):
			self.update()


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
			if len(stock["PriceHistory"]) >= self._price_history_len:
				del stock["PriceHistory"][0]

			next_price = self._calculate_next_price(stock["Price"])

			if next_price < stock["AllTimeLow"]:
				stock["AllTimeLow"] = next_price
			elif next_price > stock["AllTimeHigh"]:
				stock["AllTimeHigh"] = next_price

			stock["Change"] = next_price / stock["Price"]

			stock["Price"] = next_price
			stock["PriceHistory"].append(next_price)


	def update(self):
		self._time_elapsed += 1
		if self._time_elapsed % self._update_period:
			self._shuffle_params()

		self._update_stocks()


	def get_stocks(self):
		return self._stocks


if __name__ == "__main__":
	import matplotlib.pyplot as plt
	import matplotlib.animation as animation

	fig = plt.figure()
	ax1 = fig.add_subplot(1, 1, 1)

	market = Stockmarket(cfg.stock_types_filepath)

	def animate(i):
		market.update()

		ax1.clear()
		for stock in market.get_stocks():
			x = [i - market._price_history_len for i in range(market._price_history_len)]
			y = stock["PriceHistory"]
			plt.plot(x, y)

	ani = animation.FuncAnimation(fig, animate, interval=50)
	plt.show()
