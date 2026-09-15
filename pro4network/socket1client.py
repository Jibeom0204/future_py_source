# client
from socket import *

clientsock = socket(AF_INET,SOCK_STREAM) # 소켓 객체 만듬
clientsock.connect(('192.168.0.18',8888))
clientsock.send("안녕 서버".encode())

clientsock.close()

# 서버 실행 중 - client 실행  - server가 메세지 수신