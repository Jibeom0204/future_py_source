"""
버튼별 클라이언트·서버 처리 과정 보고서 (Flask)

버튼을 누르면 브라우저(클라이언트)와 Flask 서버가 한 일을 순서대로 모아
같은 창 안의 알림창으로 보여준다.
서버가 한 일은 서버 코드가 실행되면서 trace()로 직접 기록해 응답에 담아 보낸다.

  GET    /                  보고서 페이지 (render_template)
  POST   /login             폼 제출 로그인 → 302 리다이렉트 (페이지 새로고침)
  POST   /api/login         fetch 로그인 → JSON (새로고침 없음)
  GET    /api/me            로그인 상태 확인
  POST   /api/logout        로그아웃
  GET    /api/memos         메모 목록
  POST   /api/memos         메모 저장 (로그인 필요)
  DELETE /api/memos/<no>    메모 삭제 (로그인 필요)
  GET    /api/products?q=   상품 검색 (GET 쿼리스트링)
  GET    /api/slow          일부러 늦게 응답 (시간 초과 예외용)
  GET    /api/error         일부러 서버 오류 발생 (500 예외용)

실행: python app.py  →  브라우저에서 http://127.0.0.1:5007
로그인 계정: 아이디 id / 비밀번호 1
"""
import secrets
import threading
import time
from datetime import datetime

from flask import Flask, g, jsonify, redirect, render_template, request, session, url_for

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)  # session 쿠키 서명용. 실행할 때마다 새로 만듦 → 서버를 다시 켜면 로그아웃됨

USERS = {"id": "1"}  # 실습용 계정: 아이디 → 비밀번호
PRODUCTS = [
    {"code": 1, "sang": "안경", "su": 5, "dan": 85000},
    {"code": 2, "sang": "모자", "su": 3, "dan": 35000},
    {"code": 3, "sang": "장갑", "su": 0, "dan": 5000},
    {"code": 4, "sang": "손가방", "su": 7, "dan": 35000},
    {"code": 10, "sang": "핸드크림", "su": 12, "dan": 8000},
    {"code": 20, "sang": "칫솔", "su": 30, "dan": 2000},
]
memos = []        # DB 대신 서버 메모리에 저장 (서버를 끄면 사라짐)
memo_seq = 0
pending = {}      # 폼 제출 결과를 리다이렉트 뒤 페이지에 넘겨주기 위한 임시 보관함
lock = threading.Lock()


def now_ms():
    return time.time() * 1000


def trace(msg):
    """서버가 지금 한 일을 기록한다 → 응답에 담겨 알림창의 '서버' 단계로 표시됨"""
    g.trace.append(msg)


def server_info(view=None):
    return {
        "view": view or request.endpoint,
        "trace": g.trace,
        "recv_ms": g.recv_ms,                       # 서버가 요청을 받은 시각
        "send_ms": now_ms(),                        # 서버가 응답을 내보내는 시각
        "thread": threading.current_thread().name,  # 이 요청을 처리한 서버 스레드
    }


def reply(status=200, view=None, **data):
    """JSON 응답 + 서버 처리 기록"""
    trace(f"jsonify()로 JSON을 만들어 {status} 상태 코드로 응답")
    return jsonify({**data, "server": server_info(view)}), status


# ---------------- 모든 요청 앞에서 자동 실행 ----------------
@app.before_request
def start():
    g.recv_ms = now_ms()
    g.trace = []
    user = session.get("user")
    trace(f"{request.method} {request.full_path.rstrip('?')} 요청 받음 · "
          + (f"session 쿠키에 로그인 정보 있음 (user='{user}')" if user else "session 쿠키에 로그인 정보 없음"))
    if request.url_rule:
        trace(f"@app.route('{request.url_rule.rule}')에 연결된 {request.endpoint}() 함수 실행")


def check_login(uid, pw):
    """아이디·비밀번호 검사 (폼 로그인과 fetch 로그인이 같이 사용)"""
    if not uid or not pw:
        trace("빈 값 발견 → 서버도 한 번 더 막음 (브라우저 검사는 우회할 수 있으므로)")
        return False, "아이디와 비밀번호를 모두 입력하세요."
    if uid not in USERS:
        trace(f"USERS에 '{uid}' 계정이 없음 → 로그인 거절")
        return False, "아이디 또는 비밀번호가 틀렸습니다."
    if USERS[uid] != pw:
        trace(f"'{uid}' 계정은 있지만 비밀번호가 다름 → 로그인 거절")
        return False, "아이디 또는 비밀번호가 틀렸습니다."
    trace(f"USERS['{uid}']의 비밀번호와 일치 → 로그인 허용")
    return True, ""


# ---------------- 페이지 ----------------
@app.route("/")
def index():
    last = pending.pop(session.pop("last_action", None), None)
    if last:
        trace("session에 남겨 둔 번호(token)로 직전 폼 제출 결과를 꺼냄 (한 번 꺼내면 삭제)")
    user = session.get("user")
    trace("로그인 상태를 템플릿에 넘김: " + (f"user='{user}' → 상단에 '로그인: {user}' 표시" if user else "로그인 안 됨"))
    trace("render_template('index.html')로 HTML을 완성해 200으로 응답")
    page = {"user": user, "last": last, "index": server_info()}
    return render_template("index.html", user=user, page=page)


@app.route("/login", methods=["POST"])
def login_form():
    uid = request.form.get("id", "").strip()
    pw = request.form.get("pw", "")
    trace(f"request.form으로 폼 데이터 읽음: 아이디='{uid}', 비밀번호 {len(pw)}자리")
    ok, why = check_login(uid, pw)
    if ok:
        session["user"] = uid
        trace(f"session['user'] = '{uid}' 저장 → 응답에 Set-Cookie(session) 헤더가 붙음")
    trace("결과를 서버에 잠깐 보관(session에는 번호만 저장)하고 redirect('/') → 302 응답 (본문 없이 Location: / 만 보냄)")
    token = secrets.token_hex(8)
    pending[token] = {"ok": ok, "uid": uid, "error": why, "server": server_info()}
    session["last_action"] = token
    return redirect(url_for("index"))


# ---------------- 로그인 API ----------------
@app.route("/api/login", methods=["POST"])
def api_login():
    data = request.get_json(silent=True) or {}
    uid = str(data.get("id", "")).strip()
    pw = str(data.get("pw", ""))
    trace(f"request.get_json()으로 본문 읽음: 아이디='{uid}', 비밀번호 {len(pw)}자리")
    ok, why = check_login(uid, pw)
    if not ok:
        return reply(401 if uid and pw else 400, ok=False, error=why)
    session["user"] = uid
    trace(f"session['user'] = '{uid}' 저장 → 응답에 Set-Cookie(session) 헤더가 붙음")
    return reply(ok=True, user=uid)


@app.route("/api/me")
def api_me():
    user = session.get("user")
    if not user:
        trace("session에 'user'가 없음 → 로그인하지 않은 요청")
        return reply(401, ok=False, error="로그인하지 않은 상태입니다.")
    trace(f"session['user'] = '{user}' 확인")
    return reply(ok=True, user=user)


@app.route("/api/logout", methods=["POST"])
def api_logout():
    user = session.pop("user", None)
    if user:
        trace(f"session에서 'user'('{user}') 삭제 → 응답의 Set-Cookie로 쿠키 내용이 바뀜")
    else:
        trace("원래 로그인 상태가 아니어서 지울 정보가 없음")
    return reply(ok=True, was=user)


# ---------------- 메모 API ----------------
@app.route("/api/memos")
def memo_list():
    with lock:
        items = list(memos)
    trace(f"서버 메모리의 memos 리스트에서 {len(items)}개 읽음 (실제 서비스라면 DB에 SELECT)")
    return reply(ok=True, memos=items)


@app.route("/api/memos", methods=["POST"])
def memo_add():
    global memo_seq
    user = session.get("user")
    if not user:
        trace("메모 저장은 로그인이 필요한데 session에 'user'가 없음 → 거절")
        return reply(401, ok=False, error="로그인해야 메모를 저장할 수 있습니다.")
    text = str((request.get_json(silent=True) or {}).get("text", "")).strip()[:100]
    trace(f"request.get_json()으로 메모 내용 받음: '{text}'")
    if not text:
        trace("내용이 비어 있음 → 저장하지 않음")
        return reply(400, ok=False, error="메모 내용이 비어 있습니다.")
    with lock:
        memo_seq += 1
        memo = {"no": memo_seq, "text": text, "user": user, "time": datetime.now().strftime("%H:%M:%S")}
        memos.append(memo)
    trace(f"memos 리스트에 {memo['no']}번 메모 추가 (실제 서비스라면 DB에 INSERT)")
    return reply(201, ok=True, memo=memo)


@app.route("/api/memos/<int:no>", methods=["DELETE"])
def memo_delete(no):
    user = session.get("user")
    if not user:
        trace("메모 삭제는 로그인이 필요한데 session에 'user'가 없음 → 거절")
        return reply(401, ok=False, error="로그인해야 메모를 삭제할 수 있습니다.")
    with lock:
        found = next((m for m in memos if m["no"] == no), None)
        if found:
            memos.remove(found)
    if not found:
        trace(f"{no}번 메모가 memos 리스트에 없음 (이미 삭제됨)")
        return reply(404, ok=False, error=f"{no}번 메모를 찾을 수 없습니다.")
    trace(f"memos 리스트에서 {no}번 메모 삭제 (실제 서비스라면 DB에 DELETE)")
    return reply(ok=True, no=no)


# ---------------- 상품 검색 API (GET 쿼리스트링) ----------------
@app.route("/api/products")
def products():
    q = request.args.get("q", "").strip()
    trace(f"request.args.get('q')로 쿼리스트링 읽음: q='{q}'")
    found = [p for p in PRODUCTS if q in p["sang"]]
    if q:
        trace(f"상품 {len(PRODUCTS)}개 중 상품명에 검색어('{q}')가 들어간 {len(found)}개 선택")
    else:
        trace(f"검색어가 없어 전체 {len(found)}개 선택")
    return reply(ok=True, q=q, items=found)


# ---------------- 예외 실험용 ----------------
@app.route("/api/slow")
def slow():
    ms = min(max(request.args.get("ms", 3000, type=int), 0), 5000)
    trace(f"time.sleep({ms / 1000})으로 오래 걸리는 작업 흉내")
    time.sleep(ms / 1000)
    return reply(ok=True, ms=ms)


@app.route("/api/error")
def error_demo():
    trace("합계 ÷ 개수로 평균을 구하는 코드 실행 (개수가 0)")
    total, count = 100, 0
    return reply(ok=True, avg=total / count)  # 여기서 ZeroDivisionError 발생


@app.errorhandler(ZeroDivisionError)
def on_zero_division(e):
    trace(f"ZeroDivisionError('{e}') 발생 → error_demo() 함수가 중간에 멈춤")
    trace("@app.errorhandler(ZeroDivisionError)가 예외를 잡아 500 응답으로 바꿈")
    return reply(500, "error_demo", ok=False, error="서버 코드에서 오류가 발생했습니다 (0으로 나누기).")


@app.errorhandler(404)
def not_found(e):
    if not request.path.startswith("/api/"):
        return e  # 일반 페이지는 Flask 기본 404 화면
    trace(f"@app.route에 등록된 주소 중 '{request.path}' 주소와 일치하는 것이 없음")
    trace("@app.errorhandler(404)가 실행됨")
    return reply(404, "not_found", ok=False, error=f"'{request.path}' 주소가 서버에 없습니다.")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5007)
