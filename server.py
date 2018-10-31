
import socket
import threading

from settings import server_settings as cfg

# import stockmarket



# server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# server.bind((cfg.bind_ip, cfg.bind_port))
# server.listen(5)

# print("Listening on {}:{}".format(cfg.bind_ip, cfg.bind_port))


# def handle_client_connection(client_socket):
# 	request = client_socket.recv(1024)
# 	print("Received {}".format(request))
# 	client_socket.send("ACK!".encode())
# 	client_socket.close()

# while True:
# 	client_sock, address = server.accept()
# 	print("Accepted connection from {}:{}".format(address[0], address[1]))
# 	client_handler = threading.Thread(
# 		target=handle_client_connection,
# 		args=[client_sock]
# 	)
# 	client_handler.start()




class Server:
	def __init__(self, bind_ip, bind_port):
		self._bind_ip = bind_ip
		self._bind_port = bind_port
		self._server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self._server.bind((bind_ip, bind_port))


	def _listen_func(self):
		print("Listening on {}:{}".format(self._bind_ip, self._bind_port))
		while True:
			try:
				client_sock, address = self._server.accept()
			except KeyboardInterrupt:
				print("\rEnding server...")
				return

			print("Accepted connection from {}:{}".format(address[0], address[1]))
			client_handler = threading.Thread(
				target=self._handle_func,
				args=[client_sock]
			)
			client_handler.start()


	def _handle_func(self, client_socket):
		request = client_socket.recv(1024)
		print("Received {} command".format(request))

		# TODO: Handle things here!
		client_socket.send("TODO: Handle {}".format(request).encode())

		client_socket.close()


	def start(self):
		self._server.listen(5)
		self._listen_func()
		self._server.close()

if __name__ == "__main__":
	server = Server(cfg.bind_ip, cfg.bind_port)
	server.start()
