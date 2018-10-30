import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client.connect(("0.0.0.0", 9999))

client.send("Hello, world!\n".encode())

response = client.recv(4096)
print(response)
