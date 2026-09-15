# client
from socket import *

clientsock = socket(AF_INET,SOCK_STREAM) # 소켓 객체 만듬
clientsock.connect(('192.168.0.18',7788))
clientsock.send("안녕 서버".encode())
print('수신자료도 있음', clientsock.recv(1024).decode())
clientsock.close()

# 서버 실행 중 - client 실행  - server가 메세지 수신