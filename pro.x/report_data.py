"""
보고서에 들어갈 정리 내용 (표 데이터)

템플릿(report.html)이 {% for %} 반복문으로 이 리스트들을 읽어 <table>을 만든다.
→ 정리 내용(데이터)과 화면 모양(HTML)을 분리하는 템플릿 엔진 사용 예
"""

# 1-3. 실습 흐름: 소켓에서 Flask까지
STEPS = [
    {
        "folder": "pro4network",
        "topic": "TCP 소켓",
        "tool": "socket",
        "server": "bind → listen → accept → recv / send",
        "browser": "(브라우저 없음) 파이썬 클라이언트가 connect → send",
        "point": "모든 통신의 바닥. 형식 약속 없이 bytes만 주고받음 (encode / decode)",
    },
    {
        "folder": "pro5web",
        "topic": "정적 웹 서버",
        "tool": "http.server.SimpleHTTPRequestHandler",
        "server": "요청 경로의 파일을 읽어 그대로 전송",
        "browser": "받은 HTML을 렌더링",
        "point": "소켓 위에 HTTP라는 형식 약속을 얹은 것",
    },
    {
        "folder": "pro6web2",
        "topic": "CGI",
        "tool": "CGIHTTPRequestHandler + cgi-bin/*.py",
        "server": "요청마다 파이썬 실행 → print() 출력이 곧 응답 (DB 조회 포함)",
        "browser": "form으로 GET / POST 전송, 결과 HTML 렌더링",
        "point": "동적 페이지의 시작. 파이썬 코드와 HTML 문자열이 뒤섞임",
    },
    {
        "folder": "pro7web3_basic",
        "topic": "HTML · CSS",
        "tool": "태그, 선택자, 박스 모델",
        "server": "파일 제공",
        "browser": "DOM 생성, 스타일 계산, 화면 그리기",
        "point": "브라우저가 해석하는 문서 구조와 모양",
    },
    {
        "folder": "pro8js",
        "topic": "JavaScript · AJAX",
        "tool": "XHR → fetch → async/await → axios",
        "server": "JSON · CSV 데이터 제공",
        "browser": "비동기 요청 → 받은 데이터로 DOM 부분 갱신",
        "point": "새로고침 없이 데이터만 주고받음 (CSR)",
    },
    {
        "folder": "pro9Flask",
        "topic": "Flask · Jinja2",
        "tool": "@app.route, request, render_template",
        "server": "라우팅 → 뷰 함수 → 템플릿에 값을 채워 HTML 완성",
        "browser": "완성된 HTML 수신 · 렌더링",
        "point": "WAS + 템플릿 엔진: 서버에서 HTML 완성 (SSR)",
    },
]

# 1-4. 웹 서버와 WAS
SERVER_TYPES = [
    {
        "kind": "웹 서버",
        "role": "정적 파일(HTML, CSS, 이미지)을 읽어서 그대로 전송",
        "examples": "SimpleHTTPRequestHandler, Nginx, Apache",
        "here": "pro5web/httpserver1.py",
    },
    {
        "kind": "WAS",
        "role": "요청마다 프로그램을 실행해 결과(HTML / JSON)를 만들어 전송",
        "examples": "CGI, Flask, Django, Tomcat(자바)",
        "here": "pro6web2, pro9Flask",
    },
    {
        "kind": "개발용 서버",
        "role": "app.run(debug=True). 코드 수정 시 자동 재시작, 에러 화면 제공",
        "examples": "Flask 내장 서버(Werkzeug)",
        "here": "f_pro2 ~ f_pro5, pro.x",
    },
    {
        "kind": "운영용 서버",
        "role": "많은 요청을 안정적으로 동시에 처리",
        "examples": "waitress, gunicorn (+ 앞단에 Nginx)",
        "here": "f_pro1 (waitress.serve)",
    },
]

# 2-2. GET과 POST
GET_POST = [
    ("데이터 위치", "URL 뒤 쿼리스트링 ?name=tom&age=31", "요청 본문(body)"),
    ("Flask에서 받기", "request.args.get('name')", "request.form.get('name') · request.get_json()"),
    ("CGI에서 받기", "os.environ['QUERY_STRING']", "sys.stdin.read(CONTENT_LENGTH)"),
    ("주소창 · 기록", "그대로 노출, 북마크·공유 가능", "노출 안 됨 (암호화는 아님 → HTTPS 필요)"),
    ("길이", "URL 길이 제한 있음", "큰 데이터·파일 업로드 가능"),
    ("주 용도", "조회, 검색", "로그인, 등록·수정"),
    ("XHR 코드", 'open("GET", "js18.py?name=tom") → send()',
     'open("POST", url) → setRequestHeader("Content-Type", …) → send("name=tom")'),
]

# 2-3. 자주 보는 상태 코드
STATUS_CODES = [
    ("200", "OK", "요청 성공", "xhr.status === 200, response.ok"),
    ("302", "Found", "다른 주소로 이동(리다이렉트)", "return redirect('/')"),
    ("304", "Not Modified", "바뀐 게 없으니 캐시 사용", "static 파일을 다시 요청할 때"),
    ("404", "Not Found", "없는 주소 · 파일", "@app.route에 등록 안 된 경로"),
    ("405", "Method Not Allowed", "허용하지 않은 메서드", "f_pro2: make_response('잘못된 요청', 405)"),
    ("500", "Internal Server Error", "서버 코드에서 예외 발생", "뷰 함수 안의 오류"),
]

# 2-4. 브라우저가 요청을 보내는 방법
CLIENT_REQUESTS = [
    ("주소창 입력 · <a href>", "GET", "전체 교체", "문서 이동", "pro6web2/index.html"),
    ("<form> 제출", "GET / POST", "전체 교체", "method 속성으로 선택, name 속성이 변수명", "friend.html, get_form.html"),
    ("XMLHttpRequest", "모두", "부분 갱신", "readyState 0→4, status 200 확인. open(…, true)가 비동기", "js18, js19"),
    ("fetch + then", "모두", "부분 갱신", "Promise 체인. response.ok 확인 → response.json()", "js20"),
    ("async / await fetch", "모두", "부분 갱신", "비동기를 동기 코드처럼 작성, try / catch로 오류 처리", "js20, js21"),
    ("axios", "모두", "부분 갱신", "외부 라이브러리. JSON 자동 변환, timeout 옵션", "js20, js21"),
]

# 2-5. 실시간 통신 방식
REALTIME = [
    {
        "name": "폴링 (Polling)",
        "how": "setInterval로 일정 간격마다 요청",
        "conn": "요청마다 새로",
        "dir": "브라우저 → 서버",
        "note": "가장 간단. 변화가 없어도 계속 요청(낭비), 간격만큼 늦게 알게 됨",
        "flask": "일반 라우트 + fetch — 이 페이지 ③번 시계",
    },
    {
        "name": "롱 폴링",
        "how": "새 데이터가 생길 때까지 서버가 응답을 붙잡아 둠",
        "conn": "응답 받으면 바로 재요청",
        "dir": "사실상 서버 → 브라우저",
        "note": "지연이 적음. 대기 중인 연결 관리가 필요",
        "flask": "라우트 안에서 이벤트 대기",
    },
    {
        "name": "SSE (Server-Sent Events)",
        "how": "응답을 끝내지 않고 text/event-stream으로 계속 흘려보냄",
        "conn": "1개 유지 (끊기면 자동 재연결)",
        "dir": "서버 → 브라우저 (단방향)",
        "note": "HTTP 그대로, 브라우저에 EventSource 내장. HTTP/1.1은 한 서버당 동시 연결 6개 제한",
        "flask": "제너레이터 + Response — 이 페이지 ④번 시계",
    },
    {
        "name": "WebSocket",
        "how": "HTTP로 시작해 Upgrade 후 양방향 소켓으로 전환",
        "conn": "1개 유지",
        "dir": "양방향",
        "note": "채팅·게임처럼 양쪽이 수시로 보내는 경우. 별도 서버 구성 필요",
        "flask": "flask-sock, Flask-SocketIO 확장 필요",
    },
]

# 3-1. HTML을 만드는 네 가지 방식
HTML_WAYS = [
    {
        "name": "정적 HTML",
        "where": "미리 만든 파일",
        "side": "static",
        "server": "파일을 읽어 그대로 전송",
        "browser": "받은 그대로 렌더링",
        "refresh": "링크 이동 시 전체",
        "pros": "빠르고 단순, 캐시하기 쉬움",
        "cons": "누가 언제 요청해도 내용이 같음",
        "ex": "pro5web/abc.html",
    },
    {
        "name": "CGI",
        "where": "서버 · 파이썬 print()",
        "side": "server",
        "server": "요청마다 스크립트 실행 → 표준출력이 곧 응답",
        "browser": "완성된 HTML 렌더링",
        "refresh": "전체",
        "pros": "DB 조회 결과 같은 동적 내용 가능",
        "cons": "HTML을 문자열로 print → 수정이 어려움. 요청마다 프로세스 생성. "
                "cgi 모듈은 Python 3.13에서 제거, CGIHTTPRequestHandler도 3.15 제거 예정",
        "ex": "cgi-bin/sangpum.py",
    },
    {
        "name": "SSR · 템플릿 엔진",
        "where": "서버 · Jinja2",
        "side": "server",
        "server": "render_template()이 {{ }}·{% %}를 실제 값으로 치환",
        "browser": "완성된 HTML 렌더링 (Jinja 문법은 브라우저에 도착하지 않음)",
        "refresh": "전체",
        "pros": "HTML과 로직 분리, 상속(extends)·필터, 자동 이스케이프, 검색엔진 노출 유리",
        "cons": "일부만 바뀌어도 페이지 전체를 다시 받음",
        "ex": "f_pro3 ~ f_pro5",
    },
    {
        "name": "CSR · JS + AJAX",
        "where": "브라우저 · JavaScript",
        "side": "browser",
        "server": "데이터(JSON)만 전송",
        "browser": "받은 데이터로 DOM 조작 (innerHTML, 템플릿 리터럴)",
        "refresh": "필요한 부분만",
        "pros": "새로고침 없는 빠른 반응, 전송량 적음",
        "cons": "JS가 실행돼야 내용이 보임. 사용자 입력을 innerHTML에 그대로 넣으면 XSS 위험",
        "ex": "pro8js/js21.deep_ajax.html",
    },
]

# 3-3. 브라우저가 HTML을 화면으로 만드는 과정
RENDER_STEPS = [
    ("HTML 파싱", "태그를 읽어 DOM 트리 생성"),
    ("CSS 파싱", "스타일 규칙으로 CSSOM 생성"),
    ("렌더 트리", "DOM + CSSOM → 화면에 보일 요소만"),
    ("레이아웃", "각 요소의 위치 · 크기 계산"),
    ("페인트", "실제 픽셀로 그리기"),
]

# 코드 비교용 조각 (템플릿에서 {{ }}로 출력 → Jinja2가 < > 를 자동 이스케이프)
CODE = {
    "socket": """serversock.bind(('', 7788))          # IP=건물 주소, PORT=호실 번호
serversock.listen(5)                  # 연결 대기
conn, addr = serversock.accept()      # 클라이언트 접속 수락
msg = conn.recv(1024).decode()        # bytes → str
conn.send("행운을 빌게".encode())      # str → bytes""",

    "cgi": """print("Content-Type: text/html; charset=utf-8")
print()                               # 헤더와 본문 사이 빈 줄 필수
print("<table>")
for s in datas:                       # DB에서 읽은 행
    print(f"<tr><td>{s[0]}</td><td>{s[1]}</td></tr>")
print("</table>")""",

    "jinja": """<!-- templates/sangpum.html -->
<table>
{% for s in datas %}
  <tr><td>{{ s.code }}</td><td>{{ s.sang }}</td></tr>
{% endfor %}
</table>

# app.py
return render_template("sangpum.html", datas=datas)""",

    "js": """const res  = await fetch("/api/sangpum");   // JSON만 받음
const data = await res.json();
let out = "<table>";
data.forEach(s => {
  out += `<tr><td>${s.code}</td><td>${s.sang}</td></tr>`;
});
document.querySelector("#result").innerHTML = out + "</table>";""",

    "sse_server": """@app.route("/api/stream")
def api_stream():
    def generate():
        while True:                   # 응답이 끝나지 않음
            yield f"event: tick\\ndata: {time.time()}\\n\\n"
            time.sleep(1)
    return Response(generate(), mimetype="text/event-stream")""",

    "sse_client": """const es = new EventSource("/api/stream");
es.addEventListener("tick", e => {
  console.log("서버가 보냄:", e.data);   // 요청 없이 계속 실행됨
});""",
}
