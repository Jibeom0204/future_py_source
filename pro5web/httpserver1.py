#web server : html 서비스가 가능한 서버

#단순한 https서버 구축. 기본적인 소켓 연결
from http.server import SimpleHTTPRequestHandler,HTTPServer
PORT=7777

#get 요청에 대해 문서를 읽어 클라이언트로 전송하는 역할
handler = SimpleHTTPRequestHandler


#HTTPS server 객체 생성
serv = HTTPServer(('192.168.0.18', PORT), handler)
print('웹 서비스 시작')

serv.serve_forever() # 무한 웹서비스 진행 

