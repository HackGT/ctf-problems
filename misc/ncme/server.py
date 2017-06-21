'''
    Simple socket server using threads
'''
 
import socket
import sys
from thread import *
       
def clientthread(conn):
    conn.send('Nice job! The flag is hackgt{here_kitty_kitty}\n')
    conn.close()
    
HOST = ''   # Symbolic name, meaning all available interfaces
PORT = 9000 # Arbitrary non-privileged port
 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('Socket created')
 
#Bind socket to local host and port
try:
    s.bind((HOST, PORT))
except socket.error as msg:
    print('Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
    sys.exit()
     
print('Socket bind complete')
 
#Start listening on socket
s.listen(10)
print('Socket now listening')
 
#now keep talking with the client
try: 
    while 1:
        #wait to accept a connection - blocking call
        conn, addr = s.accept()
        print('Connected with ' + addr[0] + ':' + str(addr[1]))
        start_new_thread(clientthread, (conn,))
except KeyboardInterrupt:
    s.close()
