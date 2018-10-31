import socket

from settings import client_settings as cfg


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client.connect((cfg.bind_ip, cfg.bind_port))
client.send("Hello, world!\n".encode())
response = client.recv(4096)

print(response)
