import socket
import json
import time

from settings import client_settings as client_cfg
from visualisation.stocks import visualise_stocks


class Client:
	def __init__(self, bind_ip, bind_port):
		self._bind_ip = bind_ip
		self._bind_port = bind_port
		self._auth_token = None


	def _send(self, data):
		self._client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self._client.connect((self._bind_ip, self._bind_port))
		self._client.send(json.dumps(data).encode())

		# Read in parts until read all
		BUFF_SIZE = 4096
		data = b""
		recv_no_bytes_count = 0
		while True:
			part = self._client.recv(BUFF_SIZE)
			data += part
			if len(part) < BUFF_SIZE:
				# If we didn't recieve anything, try again as long
				# as we havent already tried 3 times in a row
				if recv_no_bytes_count >= 3:
					time.sleep(0.025)
					recv_no_bytes_count += 1
				else:
					break
			else:
				recv_no_bytes_count = 0

		self._client.close()
		try:
			response = json.loads(data.decode())
		except json.decoder.JSONDecodeError:
			response = dict(error=True, error_text="RECV_ERROR: Please try again.")

		return response


	def start(self):
		while True:
			try:
				input_line = input("> ").lower()
			except KeyboardInterrupt:
				print()
				break

			if input_line == "exit":
				break
			elif input_line == "":
				continue

			if len(input_line.split(" ", 1)) > 1:
				command, args = input_line.split(" ", 1)
			else:
				command = input_line
				args = ""

			data = dict(command=command, args=args, auth_token=self._auth_token)

			response = self._send(data)

			if not response["error"]:
				if command == "get":
					visualise_stocks(response["data"])
				elif command == "login":
					self._auth_token = response["data"]
					print(response["msg"])
				elif command == "logout":
					self._auth_token = None
					print(response["msg"])
				else:
					print(response["msg"])
			else:
				print("ERROR: {}".format(response["error_text"]))


if __name__ == "__main__":
	client = Client(client_cfg.bind_ip, client_cfg.bind_port)
	client.start()
