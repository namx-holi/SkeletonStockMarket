import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random


# TODO: Get these from json file
stock_types = [
	dict(stockID="BNS", name="Bones", Price=1.23),
	dict(stockID="BBN", name="Baby Bones", Price=3.45)
]

price_history_len = 100

mean = 0.1
stdev = 0.3


def calculate_next_price(current_price, mean, stdev):
	r = np.random.normal(0, 1, 1)
	next_price = current_price * (1 + mean/255 + r*stdev/np.sqrt(225))
	return next_price


def PROTOTYPE_UPDATE_PARAMS():
	global mean, stdev
	next_mean = calculate_next_price(mean, mean, stdev)
	next_stdev = calculate_next_price(stdev, mean, stdev)
	mean = next_mean
	stdev = next_stdev



def init_stocks(stock_types):
	stocks = []
	for stock in stock_types:
		stock_copy = stock.copy()
		stock_copy.update(dict(
			PriceHistory=[stock_copy["Price"]]))
		stocks.append(stock_copy)
	return stocks


def update_stocks(stocks):
	for stock in stocks:
		if len(stock["PriceHistory"]) >= price_history_len:
			del stock["PriceHistory"][0]

		next_price = calculate_next_price(
			stock["Price"], mean, stdev)

		stock["Price"] = next_price
		stock["PriceHistory"].append(next_price)

	# MAYBE NOT DO THIS
	# PROTOTYPE_UPDATE_PARAMS()


def simulate_stocks(stocks):
	fig = plt.figure()
	ax1 = fig.add_subplot(1, 1, 1)

	def animate(i):
		update_stocks(stocks)

		ax1.clear()
		for stock in stocks:
			x = [i for i in range(len(stock["PriceHistory"]))]
			y = stock["PriceHistory"]
			plt.plot(x, y)
	
	ani = animation.FuncAnimation(fig, animate, interval=1)
	plt.show()

stocks = init_stocks(stock_types)
simulate_stocks(stocks)
