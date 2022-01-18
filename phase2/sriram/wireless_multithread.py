import time
import threading
import socket

port1 = 5000
bot1_ip = '192.168.43.242'
port2 = 5000
bot2_ip = '192.168.43.220'
port3 = 5000
bot3_ip = '192.168.43.24'


def commandToBot(botNumber, s, data):
    try:
        dataBytes = data.encode('utf-8')
        s.send(dataBytes)
        time.sleep(0.000005)
        print(s.recv(1024).decode())
    except:
        print(f"Bot {botNumber} Error in transmission")


try:
    s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s1.connect((bot1_ip, port1))
except:
    print("Bot 1 unavailable")

try:
    s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s2.connect((bot2_ip, port2))
except:
    print("Bot 2 unavailable")

try:
    s3 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s3.connect((bot3_ip, port3))
except:
    print("Bot 3 unavailable")

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

    t1 = threading.Thread(target=commandToBot, args=(1, s1, data1))
    t2 = threading.Thread(target=commandToBot, args=(2, s2, data2))
    t3 = threading.Thread(target=commandToBot, args=(3, s3, data3))

    t1.start()
    t2.start()
    t3.start()