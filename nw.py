import socket

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

port = 5000

host = socket.gethostname()

server.bind((host, port))

server.listen(1)

print("Waiting for connection...")

conn, addr = server.accept()

print("Connected by:", addr)

data = conn.recv(1024)

print("Received:", data.decode())

conn.send(b'Thank you for connecting')

conn.close()
server.close()