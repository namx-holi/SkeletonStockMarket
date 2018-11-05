
import tkinter as tk

from gui.fonts import Fonts



class LoginPage(tk.Frame):

	@staticmethod
	def get_class_name():return "LoginPage"
	def set_opened_by(self, page): self.opened_by = page

	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)

		self.parent = parent
		self.controller = controller

		# Create components
		self.username_label = tk.Label(self, font=Fonts.medium, text="Username")
		self.password_label = tk.Label(self, font=Fonts.medium, text="Password")

		self.username_entry = tk.Entry(self, font=Fonts.large)
		self.password_entry = tk.Entry(self, font=Fonts.large, show=u"\u2620")

		self.username_label.grid(row=0, sticky=tk.E)
		self.password_label.grid(row=1, sticky=tk.E)
		self.username_entry.grid(row=0, column=1)
		self.password_entry.grid(row=1, column=1)

		self.error_text = tk.StringVar()
		self.error_label = tk.Label(self, font=Fonts.small,
			textvariable=self.error_text)
		self.error_label.grid(columnspan=2)

		self.login_button = tk.Button(self, text="Login",
			font=Fonts.medium, command=self.login_button_clicked)
		self.login_button.grid(columnspan=2)


	def login_button_clicked(self):
		username = self.username_entry.get()
		password = self.password_entry.get()

		resp = self.controller.send_request("login", "{} {}".format(username, password))

		if resp["error"]:
			print(resp["error_text"])
			self.error_text.set(resp["error_text"])
			return

		self.controller.auth_token = resp["data"]
		print(resp["msg"])

		# TODO: Delegate this to main menu somehow
		self.opened_by.login_button.configure(
			text="Logout", command=self.opened_by.logout)

		self.controller.show_frame("MainMenu")
