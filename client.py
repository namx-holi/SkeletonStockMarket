import socket
import json

from settings import client_settings as client_cfg
from visualisation.stocks import visualise_stocks


class Client:
	def __init__(self, bind_ip, bind_port):
		self._bind_ip = bind_ip
		self._bind_port = bind_port


	def _send(self, data):
		self._client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self._client.connect((self._bind_ip, self._bind_port))
		self._client.send(json.dumps(data).encode())

		# Read in parts until read all
		BUFF_SIZE = 4096
		data = b""
		while True:
			part = self._client.recv(BUFF_SIZE)
			data += part
			if len(part) < BUFF_SIZE:
				break

		self._client.close()

		return json.loads(data.decode())


	def start(self):
		input_line = ""
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
				args = None
			data = dict(command=command, args=args)

			response = self._send(data)

			if not response["error"]:
				visualise_stocks(response["response"])
			else:
				print("ERROR: {}".format(response["error_text"]))


if __name__ == "__main__":
	client = Client(client_cfg.bind_ip, client_cfg.bind_port)
	client.start()
