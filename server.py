
import socket
import threading

from settings import server_settings as cfg

# import stockmarket



server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((cfg.bind_ip, cfg.bind_port))
server.listen(5)

print("Listening on {}:{}".format(cfg.bind_ip, cfg.bind_port))


def handle_client_connection(client_socket):
	request = client_socket.recv(1024)
	print("Received {}".format(request))
	client_socket.send("ACK!".encode())
	client_socket.close()

while True:
	client_sock, address = server.accept()
	print("Accepted connection from {}:{}".format(address[0], address[1]))
	client_handler = threading.Thread(
		target=handle_client_connection,
		args=[client_sock]
	)
	client_handler.start()












