import socket
import time

port1 =5000
bot1_ip ='192.168.43.238'
port2 =5000
bot2_ip ='192.168.43.220'
port3 =5000
bot3_ip ='192.168.43.242'

# try:
#     s1 =socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     s1.connect((bot1_ip,port1))
# except:
#     print("Bot 1 unavailable")

try:
    s2 =socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s2.connect((bot2_ip,port2))
except:
    print("Bot 2 unavailable")

# try:
#     s3 =socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     s3.connect((bot3_ip,port3))
# except:
#     print("Bot 3 unavailable")

while True:
    command = input("Enter 3 commands: ")
    data1 = command[0]
    if (data1 == 'X'):
        break
    data2 = command[1]
    if (data2 == 'X'):
        break
    data3 = command[2]
    if (data3 == 'X'):
        break

    # try:
    #     dataBytes = data1.encode('utf-8')
    #     s1.send(dataBytes)
    #     time.sleep(0.000005)
    #     print(s1.recv(1024).decode())
    # except:
    #     print("Bot 1 Error in transmission")

    try:
        dataBytes = data2.encode('utf-8')
        s2.send(dataBytes)
        time.sleep(0.000005)
        print(s2.recv(1024).decode())
    except:
        print("Bot 2 Error in transmission")
    #
    # try:
    #     dataBytes = data3.encode('utf-8')
    #     s3.send(dataBytes)
    #     time.sleep(0.000005)
    #     print(s3.recv(1024).decode())
    # except:
    #     print("Bot 3 Error in transmission")

    #
    # try:
    #     dataBytes = 'S'.encode('utf-8')
    #     s1.send(dataBytes)
    #     time.sleep(0.000005)
    #     print(s1.recv(1024).decode())
    # except:
    #     print("Bot 1 Error in transmission")
    #
    # try:
    #     dataBytes = 'S'.encode('utf-8')
    #     s2.send(dataBytes)
    #     time.sleep(0.000005)
    #     print(s2.recv(1024).decode())
    # except:
    #     print("Bot 2 Error in transmission")
    #
    # try:
    #     dataBytes = 'S'.encode('utf-8')
    #     s3.send(dataBytes)
    #     time.sleep(0.000005)
    #     print(s3.recv(1024).decode())
    # except:
    #     print("Bot 3 Error in transmission")

#s1.close()
s2.close()
#s3.close()