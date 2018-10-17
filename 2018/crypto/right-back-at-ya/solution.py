import socket

#create an INET, STREAMing socket
s = socket.socket(
    socket.AF_INET, socket.SOCK_STREAM)
#now connect to the web server on port 80
# - the normal http port
s.connect(("127.0.0.1", 9876))
x = s.recv(1024)
payload = (x).decode("utf-8").split("\n")[1]
print(payload)
print(payload.encode())
s.sendall(payload.encode())
print(s.recv(1024))
