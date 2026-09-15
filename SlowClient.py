import socket
import time

s = socket.socket()
s.connect(("127.0.0.1", 45123))

s.sendall(b"BIG glenn\n") 

s.recv(4096).decode()

print("Sent BIG glenn. Not reading response.")
