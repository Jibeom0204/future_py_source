# CGIHTTPSRequestHandler: SimpleHTTPRequestHandler의 확장 클래스
# HTML,CSS 같은 정적 파일도 서비스 하면서
# /cgi-bin 아래의 파이선 프로그램 같은 cgi 스크립토도 실행할 수 있게 해주는 클래스
# get,post 모두 지원 가능

# CGI(Common Gateway Interface)
#     : 웹 서버와 외부 프로그램 사이에서 정보를 주고받는 방법이나 규약

#
from http.server import CGIHTTPRequestHandler,HTTPServer
#CGIHTTPRequestHandle 현재 파이썬 버전에서 못씀

PORT = 9999
class Handler(CGIHTTPRequestHandler):
    cgi_directories = ['/cgi-bin']
    #서버에게 "클라이언트가 /cgi-bin 경로에 있는 파일을 요청할 경우,
    #단순 텍스트로 보내지 말고 해당 스크립트를 실행하라"고 지시
    
    #어떻게든 상속 받아서 쓰는 방법
    # 듀플리케이트 됨

def runFunc():
    serv = HTTPServer(('127.0.0.1',PORT),Handler)
    print("웹서비스 실행중")

    try:
        serv.serve_forever()
    except Exception as e:
        print('서버종료',e)
    finally:
        serv.server_close

if __name__=="__main__":
    runFunc()
