import matplotlib as mpl
mpl.use('TkAgg')

import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from tkinter import *

from settings import market_settings as market_cfg

class mclass:
	def __init__(self,  window, stocks):
		self.window = window
		# self.box = Entry(window)
		# self.button = Button (window, text="check", command=self.plot)
		# self.box.pack ()
		# self.button.pack()
		self.plot(stocks)

	def plot (self, stocks):
		fig = Figure(figsize=(6,6))
		a = fig.add_subplot(111)

		for stock in stocks:
			x = [i - market_cfg.price_history_len
				for i in range(market_cfg.price_history_len)]
			y = stock["PriceHistory"]
			a.plot(x, y, label=stock["stockID"])

		# a.scatter(v,x,color='red')
		# a.plot(p, range(2 +max(x)),color='blue')
		# a.invert_yaxis()

		a.set_title ("Stock price history", fontsize=16)
		a.set_xlabel("Days from now", fontsize=14)
		a.set_ylabel("Price", fontsize=14)

		canvas = FigureCanvasTkAgg(fig, master=self.window)
		canvas.get_tk_widget().pack()
		canvas.draw()

def show(stocks):
	window = Tk()
	start = mclass(window, stocks)
	window.mainloop()
