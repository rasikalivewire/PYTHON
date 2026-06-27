import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
port = 5000

host = socket.gethostname()

client.connect((host, port))

message = "Hello Server"

client.send(message.encode())

print(client.recv(1024).decode())

client.close()