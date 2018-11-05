
import tkinter as tk

from gui.fonts import Fonts



class MainMenu(tk.Frame):

	@staticmethod
	def get_class_name():return "MainMenu"
	def set_opened_by(self, page): self.opened_by = page

	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)

		self.parent = parent
		self.controller = controller

		# Create components
		self.login_button = tk.Button(
			self, text="Login", font=Fonts.large,
			width=25, command=self.login)
		self.login_button.pack()

		self.assets_button = tk.Button(
			self, text="Assets", font=Fonts.large,
			width=25, command=None)
		self.assets_button.pack()

		self.trading_button = tk.Button(
			self, text="Trading", font=Fonts.large,
			width=25, command=None)
		self.trading_button.pack()

		self.exit_button = tk.Button(
			self, text="Exit", font=Fonts.large,
			width=25, command=self.exit)
		self.exit_button.pack()


	def login(self):
		self.controller.show_frame("LoginPage", opened_by=self)


	def logout(self):
		resp = self.controller.send_request("logout")

		if resp["error"]:
			print(resp["error_text"])
			return

		self.controller.auth_token = None
		print(resp["msg"])

		# Change the logout button to a login button
		self.login_button.configure(text="Login",
			command=self.login)


	def exit(self):
		# Try to logout before exiting
		resp = self.controller.send_request("logout")
		print(resp)

		# TODO: Error message confirming exit if logout failed?

		self.controller.destroy()
