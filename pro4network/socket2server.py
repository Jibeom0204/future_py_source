# 서버 서비스는 계속 유지
import socket
import sys
# HOST = '192.168.0.18' # == 127.0.0.1 or localhost
HOST ='' #이렇게 써도 됨. 사용가능한 모든 주소 가능
PORT = 7788

serversock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
# import socket로 받아서 socket.으로 실행해야함. 객체 이름 클래스 이름?
# 그전에는 from 으로 받음

try:
    serversock.bind((HOST,PORT))
    serversock.listen(5)
    print('서버 무한 루핑 서비스 중')

    while True:
        conn,addr = serversock.accept()
        # serversock이 클라이언트의 연결 요청을 대기하다가, 요청이 들어오면 이를 accept하는 역할
        # 연결이 성립되면 두 개의 값을 튜플 형태로 반환하고 conn과 addr 변수에 할당
        print("client info: ", addr[0], '',addr[1])
        #튜플 addr의 0번째 인덱스(addr[0])는 클라이언트의 IP 주소(문자열)
        #1번째 인덱스(addr[1])는 클라이언트의 포트 번호
        #serversock = socket.socket(socket.AF_INET,socket.SOCK_STREAM) 이 형식과 인자에 대응됨

        print(conn.recv(1024).decode()) # 수신 메세지 출력? 무슨 뜻이지
        #클라이언트에서 보내는 값을 수신하고 decode해서 값을 처리
        #1024는 recv() 함수 호출로 읽어 들일 최대 버퍼 크기(바이트 단위)

        # 메세지 송신 to client
        conn.send(('from server : '+str(addr[1])+'행운을 빌게').encode('utf_8'))
        #서버에서 해당 클라이언트로 텍스트 응답 메시지를 전송.
        #네트워크를 통해 데이터를 전송할 때는 반드시 Byte 형태로 변환해야 함.
        #조립된 문자열을 encode('utf_8')을 통해 UTF-8 형식의 바이트 스트림으로 인코딩

except Exception as e:
    print('err :',e)
    sys.exit()
finally:
    conn.close()
    serversock.close()