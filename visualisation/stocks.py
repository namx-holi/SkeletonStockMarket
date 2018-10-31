import matplotlib.pyplot as plt
from settings import market_settings as cfg


def visualise_stocks(stocks):
	fig = plt.figure()
	ax1 = fig.add_subplot(1, 1, 1)

	for stock in stocks:
		x = [i - cfg.price_history_len for i in range(cfg.price_history_len)]
		y = stock["PriceHistory"]
		plt.plot(x, y, label=stock["stockID"])

	plt.title("Stock price history")
	plt.xlabel("Days from now")
	plt.ylabel("Price")
	plt.legend()
	plt.show()
