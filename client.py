import socket
import json

from settings import client_settings as cfg


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

send_text = input("> ")
if len(send_text.split(" ", 1)) > 1:
	command, args = send_text.split(" ", 1)
else:
	command = send_text
	args = None
data = dict(command=command, args=args)

client.connect((cfg.bind_ip, cfg.bind_port))
client.send(json.dumps(data).encode())
response = client.recv(4096).decode()

print(json.loads(response))
