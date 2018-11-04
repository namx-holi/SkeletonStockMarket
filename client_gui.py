
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

class Fonts:
	large = ("Helvetica 20 bold")
	medium = ("Helvetica 15 bold")



class MainApp:

	def __init__(self, master):
		self.master = master
		self.frame = tk.Frame(self.master)
		self.auth_token = None

		self.login_logout_btn = tk.Button(
			self.frame, text="Login",
			width=25, command=self.login)
		self.login_logout_btn.pack()

		self.frame.pack()


	def _send(self, data):
		sending_data = dict(
			command="", args="", auth_token=self.auth_token)
		sending_data.update(data)

		client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		client.connect((client_cfg.bind_ip, client_cfg.bind_port))

		# TODO: Try Except around this
		sending_data = json.dumps(sending_data)

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
		login_popup = LoginDialog(self.master)
		self.master.wait_window(login_popup)

		data = dict(command="login", args="bob cool")
		response = self._send(data)

		if response["error"]:
			print(response["error_text"])
			return

		self.auth_token = response["data"]
		print(response["msg"])

		# Change the login button to a logout button
		self.login_logout_btn.configure(text="Logout",
			command=self.logout)


	def logout(self):
		data = dict(command="logout")
		response = self._send(data)

		if response["error"]:
			print(response["error_text"])
			return

		self.auth_token = None
		print(response["msg"])

		# Change the logout button to a login button
		self.login_logout_btn.configure(text="Login",
			command=self.login)


class LoginDialog(tk.Toplevel):
	def __init__(self, master):
		tk.Toplevel.__init__(self, master)
		self.master = master

		self.username_label = tk.Label(self, font=Fonts.medium, text="Username")
		self.password_label = tk.Label(self, font=Fonts.medium, text="Password")

		self.username_entry = tk.Entry(self, font=Fonts.large)
		self.password_entry = tk.Entry(self, font=Fonts.large, show=u"\u2620")

		self.username_label.grid(row=0, sticky=tk.E)
		self.password_label.grid(row=1, sticky=tk.E)
		self.username_entry.grid(row=0, column=1)
		self.password_entry.grid(row=1, column=1)

		self.login_button = tk.Button(
			self, text="Login", command=self.login_button_clicked)
		self.login_button.grid(columnspan=2)

		# self.pack()


	def login_button_clicked(self):
		print("Attempting to log in")

		username = self.username_entry.get()
		password = self.password_entry.get()

		print(username, password)


	def exit(self):
		self.destroy()



if __name__ == "__main__":
	root = tk.Tk()
	app = MainApp(root)
	# app = LoginFrame(root)
	root.mainloop()
