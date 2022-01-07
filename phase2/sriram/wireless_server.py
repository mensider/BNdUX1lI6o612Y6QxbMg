import socket
import time

port =5000
ipAddress ='192.168.137.47'

s =socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((ipAddress,port))
data ='B'
dataBytes =data.encode('utf-8')
s.send(dataBytes)
time.sleep(0.000005)
# print(s.recv(1024).decode())
s.close()
