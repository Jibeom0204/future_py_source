"""
pro.x : 웹 클라이언트-서버 구조 정리 보고서 (Flask)

보고서 페이지는 서버에서 Jinja2로 HTML을 완성해서 보내고(SSR),
페이지 안의 '실시간 동작 확인' 영역은 브라우저 JS가 서버와 계속 통신하며 갱신한다(CSR).

  /              보고서 페이지            → render_template: 서버에서 완성된 HTML
  /api/time      서버 시각 JSON           → 폴링, 왕복시간(RTT) 측정
  /api/echo      POST 값을 가공한 JSON     → fetch POST, 부분 갱신
  /api/slow      일부러 늦게 주는 JSON     → 동기 / 비동기 요청 비교
  /api/stream    SSE(Server-Sent Events) → 요청 없이 서버가 먼저 밀어주는(push) 통신

실행: python app.py  →  브라우저에서 http://127.0.0.1:5006
(다른 실습이 5000번 포트를 쓰고 있어도 같이 띄울 수 있게 5006번 사용)
"""
import json
import os
import platform
import queue
import threading
import time
from collections import deque
from datetime import datetime
from importlib.metadata import version

from flask import Flask, Response, g, jsonify, render_template, request

import report_data  # 보고서에 들어갈 정리 표(파이썬 리스트)

app = Flask(__name__)

START_MS = time.time() * 1000    # 서버가 켜진 시각
lock = threading.Lock()          # 여러 스레드(요청)가 동시에 건드리는 값 보호용
render_count = 0                 # 보고서 페이지가 서버에서 렌더링된 횟수
request_count = 0                # 서버가 처리한 전체 요청 수
recent_logs = deque(maxlen=30)   # 최근 요청 로그 (새로 접속한 브라우저에게 먼저 보여줌)
subscribers = []                 # SSE로 연결된 브라우저마다 Queue 하나씩


def now_ms():
    return time.time() * 1000


def timing():
    """응답 JSON에 넣는 서버쪽 시각 정보. 브라우저가 이 값으로 요청 구간을 나눠 계산한다"""
    return {
        "recv_ms": g.recv_ms,                        # 서버가 요청을 받은 시각
        "send_ms": now_ms(),                         # 서버가 응답을 내보내는 시각
        "thread": threading.current_thread().name,   # 이 요청을 처리한 서버 스레드
    }


def publish(event, data):
    """SSE로 연결된 모든 브라우저에게 이벤트 전달 (서버 → 브라우저 push)"""
    with lock:
        targets = list(subscribers)
    for q in targets:
        q.put((event, data))


def sse(event, data):
    """SSE 메시지 형식: 'event: 이름' 줄 + 'data: 내용' 줄 + 빈 줄"""
    return f"event: {event}\ndata: {json.dumps(data, ensure_ascii=False)}\n\n"


# ---------------- 모든 요청의 앞 / 뒤에서 자동 실행 ----------------
@app.before_request
def mark_recv():
    g.recv_ms = now_ms()  # g: 요청 하나 동안만 유지되는 저장소


@app.after_request
def log_request(response):
    # 서버가 처리한 요청을 기록하고, 연결된 브라우저들에게 즉시 알린다
    global request_count
    if request.path == "/favicon.ico":
        return response
    with lock:
        request_count += 1
        entry = {
            "no": request_count,
            "time": datetime.now().strftime("%H:%M:%S.%f")[:-3],
            "method": request.method,
            "path": request.full_path.rstrip("?"),
            "status": response.status_code,
            "ms": round(now_ms() - g.recv_ms, 1),
            "client": request.remote_addr,
            "poll": request.args.get("via") == "poll",
        }
        recent_logs.append(entry)
    publish("log", entry)
    return response


# ---------------- 보고서 페이지 (SSR) ----------------
@app.route("/")
def report():
    global render_count
    with lock:
        render_count += 1
        render_no = render_count

    who = request.args.get("who", "").strip()[:30]  # 폼(GET)으로 보낸 이름

    # 서버가 실제로 받은 HTTP 요청을 화면에 그대로 보여주기 위한 정리
    headers = [(k, "(생략)" if k.lower() == "cookie" else v) for k, v in request.headers.items()]
    http_request = {
        "line": f"{request.method} {request.full_path.rstrip('?')} {request.environ.get('SERVER_PROTOCOL')}",
        "headers": headers,
    }

    rendered_at = datetime.now()
    server = {
        "host": request.host,
        "port": request.environ.get("SERVER_PORT"),
        "python": platform.python_version(),
        "flask": version("flask"),
        "pid": os.getpid(),
        "uptime_s": round((now_ms() - START_MS) / 1000),
    }
    # 템플릿이 JS로 넘겨줄 값 (tojson 필터로 <script> 안에 출력)
    js_data = {
        "renderedMs": rendered_at.timestamp() * 1000,
        "renderNo": render_no,
        "myAddr": request.remote_addr,
    }
    return render_template(
        "report.html",
        d=report_data,
        who=who,
        render_no=render_no,
        rendered_at=rendered_at,
        http_request=http_request,
        server=server,
        js_data=js_data,
    )


# ---------------- JSON API (브라우저 JS가 fetch로 호출) ----------------
@app.route("/api/time")
def api_time():
    return jsonify(
        server_time=datetime.now().strftime("%H:%M:%S.%f")[:-3],
        protocol=request.environ.get("SERVER_PROTOCOL"),
        **timing(),
    )


@app.route("/api/echo", methods=["POST"])
def api_echo():
    data = request.get_json(silent=True) or request.form  # JSON 본문이든 form 본문이든 받기
    text = str(data.get("text", "")).strip()[:100]
    return jsonify(
        received=text,
        upper=text.upper(),
        length=len(text),
        reversed=text[::-1],
        server_time=datetime.now().strftime("%H:%M:%S.%f")[:-3],
        **timing(),
    )


@app.route("/api/slow")
def api_slow():
    delay = min(max(request.args.get("ms", 1500, type=int), 0), 5000)
    time.sleep(delay / 1000)  # DB 조회처럼 오래 걸리는 작업을 흉내
    return jsonify(delay=delay, mode=request.args.get("mode", "async"), **timing())


# ---------------- SSE: 서버가 먼저 보내는 통신 ----------------
@app.route("/api/stream")
def api_stream():
    q = queue.Queue()
    with lock:
        subscribers.append(q)
        backlog = list(recent_logs)
        count = len(subscribers)
    publish("clients", {"count": count})

    def generate():
        # yield 할 때마다 그 조각이 바로 브라우저로 전송되고, 응답은 끝나지 않는다
        try:
            yield sse("hello", {"logs": backlog, "boot": START_MS})  # boot: 서버 재시작 구분용
            next_tick = time.time()
            while True:
                wait = next_tick - time.time()
                if wait <= 0:  # 1초마다 서버 시각 push
                    yield sse("tick", {
                        "server_ms": now_ms(),
                        "requests": request_count,
                        "uptime_s": round((now_ms() - START_MS) / 1000),
                    })
                    next_tick = time.time() + 1.0
                    continue
                try:
                    event, data = q.get(timeout=wait)  # 다른 요청이 publish한 이벤트 대기
                    yield sse(event, data)
                except queue.Empty:
                    pass
        finally:
            # 브라우저가 연결을 끊으면(탭 닫기, 새로고침) 다음 전송에서 예외 → 여기로 옴
            with lock:
                subscribers.remove(q)
                count = len(subscribers)
            publish("clients", {"count": count})

    return Response(generate(), mimetype="text/event-stream",
                    headers={"Cache-Control": "no-cache"})


if __name__ == "__main__":
    # threaded=True: 요청마다 스레드를 따로 써서 SSE 연결이 열려 있어도 다른 요청 처리 가능
    app.run(debug=True, host="0.0.0.0", port=5006, threaded=True)
