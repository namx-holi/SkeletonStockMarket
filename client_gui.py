
import socket
import json
import time

# import matplotlib as mpl
# mpl.use("TkAgg")

# import numpy as np
# from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
# from matplotlib.figure import Figure
import tkinter as tk


from gui.fonts import Fonts
from gui.main_menu import MainMenu
from gui.login_page import LoginPage


# from settings import market_settings as market_cfg
from settings import client_settings as client_cfg



# TODO: Dynamically resize container every time a frame changes

class App(tk.Tk):

	def __init__(self, *args, **kwargs):
		tk.Tk.__init__(self, *args, **kwargs)
		container = tk.Frame(self)

		container.pack(side="top", fill="both", expand=True)
		container.grid_rowconfigure(0, weight=1)
		container.grid_columnconfigure(0, weight=1)

		self.auth_token = None

		self.frames = {}
		for F in (MainMenu,LoginPage):
			frame = F(container, self)
			self.frames[F.get_class_name()] = frame
			frame.grid(row=0, column=0, sticky="nsew")

		print(self.frames)

		# Open the main menu
		self.show_frame("MainMenu")


	# TODO: Find a way to send prev window to the frame?
	def show_frame(self, cont, opened_by=None):
		frame = self.frames[cont]
		if opened_by:
			frame.set_opened_by(opened_by)
		frame.tkraise()


	def send_request(self, command=None, args=None):
		data = dict(
			command=command,
			args=args,
			auth_token=self.auth_token)

		client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		client.connect((client_cfg.bind_ip, client_cfg.bind_port))

		req = json.dumps(data)
		client.send(req.encode())

		# Read in parts until read all
		BUFF_SIZE = 4096
		no_recv_count = 0
		data = b""
		while no_recv_count < 3:
			part = client.recv(BUFF_SIZE)
			data += part

			if len(part) < BUFF_SIZE:
				time.sleep(0.05)
				no_recv_count += 1
			else:
				no_recv_count = 0
		client.close()

		try:
			resp = json.loads(data.decode())
		except json.decoder.JSONDecodeError:
			resp = dict(error=True, error_text="RECV_ERROR: Please try again.")
		return resp



if __name__ == "__main__":
	app = App()
	app.mainloop()
