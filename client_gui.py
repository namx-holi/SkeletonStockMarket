
import socket
import json
import time

import matplotlib as mpl
mpl.use("TkAgg")

import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import tkinter as tk

from settings import market_settings as market_cfg
from settings import client_settings as client_cfg


class MainApp:
	def __init__(self, master):
		self.master = master
		self.frame = tk.Frame(self.master)
		self.auth_token = None


		self.login_btn = tk.Button(
			self.frame, text="Login", width=25,
			command = self.login)
		self.login_btn.pack()

		self.frame.pack()


	def _send(self, data):
		data.update(dict(auth_token=self.auth_token))

		client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		client.connect((client_cfg.bind_ip, client_cfg.bind_port))

		# TODO: Try Except around this
		sending_data = json.dumps(data)

		client.send(sending_data.encode())

		# Read in parts until read all
		BUFF_SIZE = 4096
		data = b""
		no_recv_count = 0
		while no_recv_count < 3:
			part = client.recv(BUFF_SIZE)
			data += part

			if len(part) < BUFF_SIZE:
				time.sleep(0.025)
				no_recv_count += 1
			else:
				no_recv_count = 0

		client.close()

		try:
			response = json.loads(data.decode())
		except json.decoder.JSONDecodeError:
			response = dict(error=True, error_text="RECV_ERROR: Please try again.")
		return response


	def login(self):
		data = dict(command="login", args="bob cool")
		response = self._send(data)

		if not response["error"]:
			self._auth_token = response["data"]
			print(response["msg"])



if __name__ == "__main__":
	root = tk.Tk()
	app = MainApp(root)
	root.mainloop()
