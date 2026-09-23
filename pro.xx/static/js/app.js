// static/js/app.js
// 버튼마다 클라이언트(이 파일)와 서버(app.py)가 한 일을 순서대로 모아 알림창(dialog)으로 보여준다.
// 서버 단계는 서버가 응답에 담아 보낸 기록(server.trace)을 그대로 쓴다.

const $ = (sel) => document.querySelector(sel);
const PAGE = window.PAGE; // 서버(Jinja2)가 렌더링할 때 넣어 준 값

// ===================== 공통 도구 =====================
const STATUS_KO = { 200: "성공", 201: "생성됨", 302: "다른 주소로 이동", 400: "잘못된 요청", 401: "인증 실패", 404: "찾을 수 없음", 500: "서버 오류" };
const SIDE = { client: "클라이언트", net: "통신", server: "서버" };
const KIND = { ok: "처리 완료", error: "예외 발생", local: "브라우저에서만 처리" };

function fmtMs(ms) {
    if (ms < 10) return ms.toFixed(1) + "ms";
    if (ms < 1000) return Math.round(ms) + "ms";
    return (ms / 1000).toFixed(2) + "초";
}

// 알림창 단계 만들기: 누가 한 일인지 + 제목 + 설명
const C = (title, detail = "") => ({ side: "client", title, detail });
const N = (title, detail = "") => ({ side: "net", title, detail });
const S = (title, detail = "") => ({ side: "server", title, detail });
const clicked = (name, detail = "") => C(`[${name}] 클릭 → click 이벤트 처리 함수 실행`, detail);

// 알림창에는 비밀번호를 가려서 보여준다
const hidePw = (obj) => (obj && "pw" in obj ? { ...obj, pw: "•".repeat(String(obj.pw).length) } : obj);
// 응답 JSON 중 서버 기록(server)은 서버 단계로 따로 보여주므로 뺀다
function bodyOnly(data) {
    if (!data) return data;
    const { server, ...rest } = data;
    return rest;
}

function make(tag, text = "", cls = "") {
    const el = document.createElement(tag);
    el.textContent = text; // 사용자 입력이 섞여도 태그로 해석되지 않도록 textContent 사용
    if (cls) el.className = cls;
    return el;
}

// ===================== 서버 요청 =====================
// call(): fetch()를 보내고 응답 JSON까지 받아 온다. 통신 실패도 여기서 잡아 결과로 돌려준다.
async function call(method, url, body, timeoutMs = 0) {
    const ctrl = new AbortController();
    const timer = timeoutMs ? setTimeout(() => ctrl.abort(), timeoutMs) : null;
    const opt = { method, signal: ctrl.signal };
    if (body !== undefined) {
        opt.headers = { "Content-Type": "application/json" };
        opt.body = JSON.stringify(body);
    }
    const t0 = performance.now();
    try {
        const res = await fetch(url, opt);              // 비동기: 기다리는 동안에도 화면은 멈추지 않음
        const data = await res.json().catch(() => null);
        return { method, url, body, res, data, ms: performance.now() - t0 };
    } catch (err) {                                     // 서버 꺼짐, 시간 초과(abort) 등 → 응답 자체가 없음
        return { method, url, body, err, ms: performance.now() - t0 };
    } finally {
        clearTimeout(timer);
    }
}

function sendStep(c) {
    const how = c.body !== undefined
        ? `본문 ${JSON.stringify(hidePw(c.body))} (Content-Type: application/json)`
        : "본문 없음";
    return N(`${c.method} ${c.url} 요청 보냄`, `fetch()가 비동기로 전송 · ${how}. 응답을 기다리는 동안에도 페이지는 그대로 동작함`);
}

function serverSteps(c) {
    const s = c.data?.server;
    if (!s) return [S("서버 기록 없음", "응답이 JSON이 아니어서 서버가 한 일을 읽지 못함")];
    return s.trace.map((t) => S(t));
}

function responseStep(c) {
    const st = c.res.status;
    return N(`응답 받음: ${st} ${c.res.statusText}${STATUS_KO[st] ? ` (${STATUS_KO[st]})` : ""}`,
        `JSON 본문: ${JSON.stringify(bodyOnly(c.data))}`);
}

function facts(c) {
    const f = [["요청", `${c.method} ${c.url}`]];
    if (c.body !== undefined) f.push(["보낸 데이터", JSON.stringify(hidePw(c.body))]);
    if (c.res) f.push(["응답 상태", `${c.res.status} ${c.res.statusText}`]);
    const s = c.data?.server;
    if (s) {
        f.push(["처리한 서버 함수", `${s.view}()`]);
        f.push(["서버 처리 시간", fmtMs(s.send_ms - s.recv_ms)]);
        f.push(["서버 스레드", s.thread]);
    }
    f.push(["클릭 → 응답까지", fmtMs(c.ms)]);
    return f;
}

// 서버와 통신한 버튼의 알림창: [클릭·입력] → 요청 → 서버 기록 → 응답 → [화면 처리]
function apiReport({ button, c, before, ok, fail, code }) {
    if (c.err) return report(commErrorReport(button, c, before, code));
    const good = c.res.ok;
    const r = good ? ok(c.data) : fail(c.data?.error ?? `${c.res.status} ${c.res.statusText}`);
    report({
        kind: good ? "ok" : "error",
        button,
        summary: r.summary,
        steps: [...before, sendStep(c), ...serverSteps(c), responseStep(c), ...r.after],
        facts: facts(c),
        code,
    });
}

// 응답 자체를 못 받은 경우 (서버가 꺼져 있음 등)
function commErrorReport(button, c, before, code) {
    return {
        kind: "error",
        kindLabel: "예외 발생 · 통신 실패",
        button,
        summary: "서버에 연결하지 못했습니다. 서버가 꺼져 있거나 주소가 잘못됐을 수 있습니다.",
        steps: [
            ...before,
            N(`${c.method} ${c.url} 요청 보냄`),
            N("연결 실패: 응답 자체가 오지 않음", `fetch()가 ${c.err.name}: ${c.err.message} 로 실패. 상태 코드도 없음`),
            C("catch 블록에서 오류를 잡아 이 예외창 표시", "서버 기록이 없음 → 서버까지 요청이 닿지 않았음"),
        ],
        facts: [["요청", `${c.method} ${c.url}`], ["결과", c.err.name], ["클릭 → 실패까지", fmtMs(c.ms)]],
        code,
    };
}

// ===================== 알림창 (dialog) =====================
const records = []; // 처리 기록 (최근 것이 앞)

function report(r, remember = true) {
    const dlg = $("#report");
    dlg.dataset.kind = r.kind;
    $("#report-kind").textContent = r.kindLabel ?? KIND[r.kind];
    $("#report-title").textContent = `[${r.button}] 버튼을 눌렀을 때`;
    $("#report-summary").textContent = r.summary;
    $("#report-steps").replaceChildren(...r.steps.map(stepItem));
    $("#report-facts").replaceChildren(...(r.facts ?? []).flatMap(([k, v]) => [make("dt", k), make("dd", v)]));
    const code = $("#report-code");
    code.hidden = !r.code;
    code.open = false;
    if (r.code) {
        $("#code-client").textContent = r.code.client;
        $("#code-server").textContent = r.code.server;
    }
    if (remember) addHistory(r);
    if (dlg.open) dlg.close();
    dlg.showModal();                                   // 같은 창 위에 뜨는 모달 (새 창 아님)
    $(".report-body").scrollTop = 0;
}

function stepItem(s) {
    const li = make("li", "", `step ${s.side}`);
    const what = make("div", "", "what");
    what.append(make("b", s.title));
    if (s.detail) what.append(make("p", s.detail));
    li.append(make("span", SIDE[s.side], "who"), what);
    return li;
}

function addHistory(r) {
    records.unshift({ r, at: new Date() });
    $("#history").replaceChildren(...records.map(({ r: item, at }) => {
        const btn = make("button", "", `hist ${item.kind}`);
        btn.type = "button";
        btn.append(
            make("span", at.toLocaleTimeString("ko-KR", { hour12: false }), "t"),
            make("b", item.button),
            make("span", item.kindLabel ?? KIND[item.kind], "k"),
            make("span", item.summary, "s"),
        );
        btn.addEventListener("click", () => report(item, false));
        const li = make("li");
        li.append(btn);
        return li;
    }));
}

// 요청 중에는 버튼을 잠깐 막아 두 번 눌리지 않게
function onClick(sel, handler) {
    const btn = $(sel);
    btn.addEventListener("click", async () => {
        btn.disabled = true;
        try { await handler(); } finally { btn.disabled = false; }
    });
}

// ===================== 화면 갱신 함수 =====================
function setLoginState(user) {
    const el = $("#login-state");
    el.textContent = user ? `로그인: ${user}` : "로그인 안 됨";
    el.classList.toggle("on", Boolean(user));
}

function memoItem(m) {
    const li = make("li");
    const text = make("div", "", "memo");
    text.append(make("b", m.text), make("span", `${m.no}번 · ${m.user} · ${m.time}`, "meta"));
    const del = make("button", "삭제", "btn small danger");
    del.type = "button";
    del.dataset.no = m.no;
    li.append(text, del);
    return li;
}

function renderMemos(list) {
    const ul = $("#memo-list");
    ul.replaceChildren(...list.map(memoItem));
    if (!list.length) ul.append(make("li", "저장된 메모가 없습니다.", "empty"));
}

function renderProducts(items) {
    const tbody = $("#search-result");
    tbody.replaceChildren(...items.map((p) => {
        const tr = make("tr");
        tr.append(make("td", p.code), make("td", p.sang), make("td", p.su), make("td", p.dan.toLocaleString() + "원"));
        return tr;
    }));
    if (!items.length) {
        const td = make("td", "검색 결과가 없습니다.", "empty");
        td.colSpan = 4;
        const tr = make("tr");
        tr.append(td);
        tbody.append(tr);
    }
}

// ===================== ① 로그인 =====================
function readLogin() {
    const uid = $("#uid").value.trim();
    const pw = $("#upw").value;
    return { uid, pw, step: C("JS가 입력란 값 읽음", `아이디 '${uid}', 비밀번호 ${pw.length}자리 (알림창에는 •로 가려 표시)`) };
}

// 빈 칸이면 서버에 보내지 않고 브라우저에서 바로 예외창
function emptyLoginReport(button, first, v, code) {
    const missing = [!v.uid && "아이디", !v.pw && "비밀번호"].filter(Boolean).join(", ");
    return {
        kind: "error",
        kindLabel: "예외 발생 · 브라우저에서 차단",
        button,
        summary: `${missing}가 비어 있어 브라우저가 서버에 보내기 전에 멈췄습니다.`,
        steps: [
            first,
            v.step,
            C(`빈 칸 발견: ${missing}`, "if (!uid || !pw) 검사에 걸림"),
            C("서버로 요청을 보내지 않고 여기서 중단", "서버는 버튼이 눌린 것조차 모릅니다. 서버까지 갈 필요 없는 검사라 브라우저에서 먼저 합니다 (서버에도 같은 검사가 있음)."),
            C("이 예외창 표시"),
        ],
        facts: [["요청", "보내지 않음"], ["검사한 곳", "브라우저 (JS)"]],
        code,
    };
}

// 제출 (form): 값이 있으면 막지 않음 → 브라우저가 폼을 전송하고 페이지를 떠남
$("#login-form").addEventListener("submit", (e) => {
    const v = readLogin();
    if (!v.uid || !v.pw) {
        e.preventDefault(); // 폼 전송(페이지 이동)을 막음
        report(emptyLoginReport("제출 (form)", C("[제출 (form)] 클릭 → form의 submit 이벤트 발생"), v, CODE.formEmpty));
    }
});

// 폼 제출 → 302 → 다시 그려진 페이지에서 보여줄 알림창
function formLoginReport(last, index) {
    const nav = performance.getEntriesByType("navigation")[0];
    const redirects = nav ? nav.redirectCount : 1;
    const s = last.server;
    return {
        kind: last.ok ? "ok" : "error",
        button: "제출 (form)",
        summary: last.ok
            ? `브라우저가 폼을 서버로 보내며 페이지를 떠났고, 서버가 '${last.uid}' 로그인을 처리한 뒤 302로 첫 화면에 돌려보냈습니다. 새로 그려진 페이지에 로그인 상태가 반영됐습니다.`
            : `서버가 아이디·비밀번호를 확인했지만 로그인을 거절했습니다: ${last.error} 페이지는 새로고침됐고 로그인 상태는 바뀌지 않았습니다.`,
        steps: [
            C("[제출 (form)] 클릭 → 입력값이 있어 JS가 막지 않음"),
            C("브라우저 기본 동작으로 폼 전송, 지금 보던 페이지를 떠남",
                "JS의 fetch가 아니라 브라우저가 <form method=\"post\" action=\"/login\">의 입력값을 id=…&pw=… 형태(application/x-www-form-urlencoded)로 만들어 보냄"),
            N("POST /login 요청 보냄", `본문: id=${encodeURIComponent(last.uid)}&pw=(가림)`),
            ...s.trace.map((t) => S(t)),
            N("응답 받음: 302 FOUND (다른 주소로 이동)", "본문 없이 Location: / 헤더만 옴"),
            C(`브라우저가 Location을 보고 GET / 을 자동으로 다시 요청 (리다이렉트 ${redirects}회)`, "JS 코드 없이 브라우저가 알아서 함"),
            ...index.trace.map((t) => S(t)),
            N("응답 받음: 200 OK", "서버에서 완성된 HTML 문서 전체"),
            C("새 HTML을 처음부터 파싱·렌더링 → 페이지 전체가 새로 그려짐",
                "입력란은 기본값으로 돌아가고, 불러온 메모·검색 결과·처리 기록은 사라짐"),
            C("JS가 서버가 넣어 둔 window.PAGE.last를 읽어 이 알림창을 띄움",
                "이 상태에서 새로고침(F5)해도 폼이 다시 전송되지 않음 (POST 후 리다이렉트하는 PRG 방식의 장점)"),
        ],
        facts: [
            ["요청 흐름", "POST /login → 302 → GET / → 200"],
            ["처리한 서버 함수", `${s.view}() → ${index.view}()`],
            ["서버 처리 시간", `/login ${fmtMs(s.send_ms - s.recv_ms)} · / ${fmtMs(index.send_ms - index.recv_ms)}`],
            ["리다이렉트 횟수", `${redirects}회`],
            ["폼 전송 → 이 알림창까지", fmtMs(performance.now())],
        ],
        code: CODE.form,
    };
}

// 로그인 (fetch): 새로고침 없이 JSON으로 주고받음
onClick("#btn-login", async () => {
    const first = clicked("로그인 (fetch)", "type=\"button\"이라 폼 전송(페이지 이동)은 일어나지 않음");
    const v = readLogin();
    if (!v.uid || !v.pw) return report(emptyLoginReport("로그인 (fetch)", first, v, CODE.fetchEmpty));
    const c = await call("POST", "/api/login", { id: v.uid, pw: v.pw });
    if (c.res?.ok) setLoginState(c.data.user);
    apiReport({
        button: "로그인 (fetch)", c, before: [first, v.step], code: CODE.login,
        ok: (d) => ({
            summary: `브라우저가 입력값을 JSON으로 보내고, 서버가 확인해 '${d.user}' 로그인을 허용했습니다. 페이지는 새로고침되지 않았습니다.`,
            after: [C(`response.ok 확인 → 상단 표시를 '로그인: ${d.user}'로 변경`,
                "DOM의 글자만 바꾼 부분 갱신. 이후 요청마다 브라우저가 session 쿠키를 자동으로 붙여 보냄")],
        }),
        fail: (msg) => ({
            summary: `서버가 아이디·비밀번호를 확인했지만 로그인을 거절했습니다: ${msg}`,
            after: [C("response.ok가 false → 예외 처리로 넘어감", "로그인 상태 표시는 바꾸지 않고 이 예외창을 띄움")],
        }),
    });
});

onClick("#btn-me", async () => {
    const c = await call("GET", "/api/me");
    if (c.res) setLoginState(c.res.ok ? c.data?.user : null);
    apiReport({
        button: "로그인 상태 확인", c, code: CODE.me,
        before: [clicked("로그인 상태 확인"),
            C("보낼 데이터 없음", "로그인 정보는 브라우저가 가진 session 쿠키가 요청에 자동으로 실려 감. JS는 이 쿠키를 직접 읽지 않음")],
        ok: (d) => ({
            summary: `서버가 요청에 실려 온 session 쿠키를 확인해 '${d.user}'로 로그인된 상태라고 답했습니다.`,
            after: [C(`상단 표시를 '로그인: ${d.user}'로 맞춤`)],
        }),
        fail: (msg) => ({
            summary: `서버가 session에서 로그인 정보를 찾지 못해 401로 답했습니다: ${msg}`,
            after: [C("401 응답 → 상단 표시를 '로그인 안 됨'으로 맞추고 이 예외창 표시")],
        }),
    });
});

onClick("#btn-logout", async () => {
    const c = await call("POST", "/api/logout");
    if (c.res?.ok) setLoginState(null);
    apiReport({
        button: "로그아웃", c, code: CODE.logout,
        before: [clicked("로그아웃"), C("보낼 데이터 없음", "지울 대상은 요청에 자동으로 실려 가는 session 쿠키로 서버가 알아냄")],
        ok: (d) => ({
            summary: d.was
                ? `서버가 session에서 '${d.was}' 로그인 정보를 지웠습니다.`
                : "원래 로그인 상태가 아니어서 서버가 지울 정보가 없었습니다 (응답은 성공).",
            after: [C("상단 표시를 '로그인 안 됨'으로 변경")],
        }),
        fail: (msg) => ({ summary: `로그아웃하지 못했습니다: ${msg}`, after: [C("이 예외창 표시")] }),
    });
});

$("#btn-reset").addEventListener("click", () => {
    const t0 = performance.now();
    $("#uid").value = "id";
    $("#upw").value = "1";
    report({
        kind: "local",
        button: "기본값으로 되돌리기",
        summary: "서버와 통신하지 않고, 브라우저 JS가 입력란 값만 기본값으로 바꿨습니다.",
        steps: [
            clicked("기본값으로 되돌리기"),
            C("JS가 아이디 입력란 value를 'id', 비밀번호 입력란 value를 '1'로 바꿈"),
            C("서버로는 아무 요청도 보내지 않음", "서버는 이 버튼이 눌린 것을 모릅니다. 서버 터미널 로그에도 찍히지 않습니다."),
        ],
        facts: [["요청", "없음"], ["처리한 곳", "브라우저 JS"], ["걸린 시간", fmtMs(performance.now() - t0)]],
        code: CODE.reset,
    });
});

// ===================== ② 메모 =====================
onClick("#btn-memo-add", async () => {
    const first = clicked("저장");
    const text = $("#memo-text").value.trim();
    const read = C("JS가 입력란 값 읽음", `메모 '${text}'`);
    if (!text) {
        return report({
            kind: "error", kindLabel: "예외 발생 · 브라우저에서 차단", button: "저장",
            summary: "메모 내용이 비어 있어 브라우저가 서버에 보내기 전에 멈췄습니다.",
            steps: [first, read, C("빈 값 발견 → 서버로 요청을 보내지 않고 중단"), C("이 예외창 표시")],
            facts: [["요청", "보내지 않음"], ["검사한 곳", "브라우저 (JS)"]],
            code: CODE.memoAdd,
        });
    }
    const c = await call("POST", "/api/memos", { text });
    if (c.res?.ok) {
        $("#memo-list .empty")?.remove();
        $("#memo-list").append(memoItem(c.data.memo));
    }
    apiReport({
        button: "저장", c, before: [first, read], code: CODE.memoAdd,
        ok: (d) => ({
            summary: `서버가 ${d.memo.no}번 메모로 저장했고(201 Created), 브라우저가 목록에 한 줄을 추가했습니다.`,
            after: [C("응답의 memo로 <li>를 하나 만들어 목록 끝에 추가",
                "전체 새로고침 없이 그 줄만 추가. 사용자 입력은 textContent로 넣어 태그로 해석되지 않음")],
        }),
        fail: (msg) => ({
            summary: `서버가 저장을 거절했습니다: ${msg}`,
            after: [C("response.ok가 false → 목록은 그대로 두고 이 예외창 표시",
                c.res.status === 401 ? "먼저 ① 로그인을 하세요." : "")],
        }),
    });
});

onClick("#btn-memo-list", async () => {
    const c = await call("GET", "/api/memos");
    if (c.res?.ok) renderMemos(c.data.memos);
    apiReport({
        button: "목록 불러오기", c, code: CODE.memoList,
        before: [clicked("목록 불러오기"), C("보낼 데이터 없음 (GET)")],
        ok: (d) => ({
            summary: `서버가 메모 ${d.memos.length}개를 JSON 배열로 보냈고, 브라우저가 그것으로 목록을 다시 그렸습니다.`,
            after: [C(`받은 배열 ${d.memos.length}개로 <li>를 만들어 목록을 통째로 다시 그림`,
                d.memos.length ? "" : "0개라 '저장된 메모가 없습니다'를 표시")],
        }),
        fail: (msg) => ({ summary: `목록을 받지 못했습니다: ${msg}`, after: [C("이 예외창 표시")] }),
    });
});

// 삭제 버튼은 나중에 생기므로 목록(ul)에 이벤트를 걸어 둠 (이벤트 위임)
$("#memo-list").addEventListener("click", async (e) => {
    const btn = e.target.closest("button[data-no]");
    if (!btn) return;
    const no = Number(btn.dataset.no);
    btn.disabled = true;
    const c = await call("DELETE", `/api/memos/${no}`);
    if (c.res?.ok) {
        btn.closest("li").remove();
        if (!$("#memo-list li")) renderMemos([]);
    } else {
        btn.disabled = false;
    }
    apiReport({
        button: `삭제 (${no}번 메모)`, c, code: CODE.memoDelete,
        before: [clicked(`삭제 (${no}번 메모)`),
            C(`버튼의 data-no 속성에서 메모 번호 ${no} 읽음`, `주소 /api/memos/${no}에 번호를 넣어 DELETE 메서드로 요청`)],
        ok: () => ({
            summary: `서버가 ${no}번 메모를 지웠고, 브라우저가 목록에서 그 줄만 뺐습니다.`,
            after: [C("해당 <li>만 목록에서 제거")],
        }),
        fail: (msg) => ({
            summary: `서버가 삭제를 거절했습니다: ${msg}`,
            after: [C("목록은 그대로 두고 이 예외창 표시", c.res.status === 401 ? "먼저 ① 로그인을 하세요." : "")],
        }),
    });
});

// ===================== ③ 검색 =====================
onClick("#btn-search", async () => {
    const q = $("#q").value.trim();
    const enc = encodeURIComponent(q);
    const c = await call("GET", `/api/products?q=${enc}`);
    if (c.res?.ok) renderProducts(c.data.items);
    apiReport({
        button: "검색", c, code: CODE.search,
        before: [clicked("검색"),
            C(`검색어 '${q}'를 주소 뒤에 ?q=${enc} 로 붙임`,
                "GET은 본문이 없고 데이터가 주소(쿼리스트링)에 실림. 한글은 encodeURIComponent로 %EA… 형태로 바꿔서 보냄")],
        ok: (d) => ({
            summary: q
                ? `서버가 상품명에 검색어('${q}')가 들어간 상품 ${d.items.length}개를 골라 보냈고, 브라우저가 표를 다시 그렸습니다.`
                : `검색어가 없어 서버가 전체 상품 ${d.items.length}개를 보냈고, 브라우저가 표를 다시 그렸습니다.`,
            after: [C(`받은 ${d.items.length}개로 표의 <tr>을 다시 만듦`,
                d.items.length ? "단가는 toLocaleString()으로 세 자리마다 쉼표" : "0개라 '검색 결과가 없습니다'를 표시")],
        }),
        fail: (msg) => ({ summary: `검색하지 못했습니다: ${msg}`, after: [C("이 예외창 표시")] }),
    });
});

// ===================== ④ 예외 상황 =====================
onClick("#btn-404", async () => {
    const c = await call("GET", "/api/nothing");
    apiReport({
        button: "없는 주소 요청 (404)", c, code: CODE.e404,
        before: [clicked("없는 주소 요청 (404)"), C("일부러 서버에 없는 주소 /api/nothing 으로 요청을 만듦")],
        ok: () => ({ summary: "예상과 달리 성공했습니다.", after: [] }),
        fail: (msg) => ({
            summary: `서버에 그런 주소(라우트)가 없어서 404 Not Found로 답했습니다: ${msg}`,
            after: [C("response.ok가 false(404) → 이 예외창 표시",
                "fetch는 404·500 응답도 '도착'으로 보고 catch로 보내지 않음 → response.ok나 status를 직접 확인해야 함")],
        }),
    });
});

onClick("#btn-500", async () => {
    const c = await call("GET", "/api/error");
    apiReport({
        button: "서버 코드 오류 (500)", c, code: CODE.e500,
        before: [clicked("서버 코드 오류 (500)"), C("오류가 나도록 만들어 둔 주소 /api/error 로 요청")],
        ok: () => ({ summary: "예상과 달리 성공했습니다.", after: [] }),
        fail: (msg) => ({
            summary: `서버 함수가 실행 도중 오류로 멈췄고, 서버의 오류 처리 함수가 500 Internal Server Error로 답했습니다: ${msg}`,
            after: [C("response.ok가 false(500) → 이 예외창 표시", "브라우저 쪽 코드는 문제없음. 원인은 서버 코드")],
        }),
    });
});

onClick("#btn-timeout", async () => {
    const LIMIT = 1500;   // 브라우저가 기다려 줄 시간
    const WORK = 3000;    // 서버 작업 시간
    const before = [
        clicked("응답 지연 → 시간 초과"),
        C(`AbortController로 ${LIMIT / 1000}초 타이머 설정`, "시간 안에 응답이 없으면 controller.abort()로 요청을 취소하도록 준비"),
    ];
    const c = await call("GET", `/api/slow?ms=${WORK}`, undefined, LIMIT);
    if (c.err?.name !== "AbortError") {
        // 시간 안에 응답이 왔거나(서버가 빨랐음) 다른 통신 오류
        return apiReport({
            button: "응답 지연 → 시간 초과", c, before, code: CODE.timeout,
            ok: () => ({ summary: "제한 시간 안에 응답이 와서 시간 초과가 일어나지 않았습니다.", after: [] }),
            fail: (msg) => ({ summary: msg, after: [] }),
        });
    }
    report({
        kind: "error",
        kindLabel: "예외 발생 · 시간 초과",
        button: "응답 지연 → 시간 초과",
        summary: `서버가 ${LIMIT / 1000}초 안에 답하지 않아 브라우저가 기다리기를 포기했습니다 (시간 초과).`,
        steps: [
            ...before,
            N(`GET /api/slow?ms=${WORK} 요청 보냄`, "fetch()가 비동기로 전송"),
            S(`서버가 요청을 받아 slow() 실행 → time.sleep(${WORK / 1000})으로 ${WORK / 1000}초 걸리는 작업 시작`,
                "응답을 받지 못해서 서버 기록 대신 서버 코드를 기준으로 설명한 단계"),
            C(`${LIMIT / 1000}초가 지나도 응답이 없어 controller.abort() 실행 → fetch가 AbortError로 실패`),
            C("catch에서 AbortError를 잡아 이 예외창 표시", "기다리는 동안에도 화면은 멈추지 않았음 (비동기)"),
            S(`서버는 작업을 끝까지 마치고 약 ${WORK / 1000}초 뒤 응답을 보내지만, 브라우저가 이미 요청을 취소해 그 응답은 버려짐`,
                "서버 코드를 기준으로 설명한 단계"),
        ],
        facts: [
            ["요청", `GET /api/slow?ms=${WORK}`],
            ["브라우저 제한 시간", `${LIMIT / 1000}초`],
            ["서버 작업 시간", `${WORK / 1000}초`],
            ["결과", `${c.err.name} (응답 없음)`],
            ["클릭 → 포기까지", fmtMs(c.ms)],
        ],
        code: CODE.timeout,
    });
});

// Enter 키로도 누르기
$("#memo-text").addEventListener("keydown", (e) => { if (e.key === "Enter") $("#btn-memo-add").click(); });
$("#q").addEventListener("keydown", (e) => { if (e.key === "Enter") $("#btn-search").click(); });

// ===================== 버튼별 핵심 코드 (알림창의 '코드 보기') =====================
const CODE = {
    form: {
        client: `<!-- templates/index.html -->
<form method="post" action="/login">
  <input name="id" value="id">
  <input name="pw" type="password" value="1">
  <button type="submit">제출 (form)</button>
</form>

// app.js: 빈 칸이 아니면 막지 않음 → 브라우저가 전송
form.addEventListener("submit", (e) => {
  if (!uid || !pw) e.preventDefault();
});
// 다시 그려진 페이지에서 서버가 넣어 준 결과로 알림창
if (PAGE.last) report(formLoginReport(PAGE.last, PAGE.index));`,
        server: `@app.route("/login", methods=["POST"])
def login_form():
    uid = request.form.get("id", "").strip()
    pw = request.form.get("pw", "")
    ok, why = check_login(uid, pw)
    if ok:
        session["user"] = uid
    token = secrets.token_hex(8)
    pending[token] = {"ok": ok, "uid": uid, ...}  # 결과 보관
    session["last_action"] = token
    return redirect(url_for("index"))             # 302

@app.route("/")
def index():
    last = pending.pop(session.pop("last_action", None), None)
    return render_template("index.html", user=..., page=...)`,
    },
    formEmpty: {
        client: `form.addEventListener("submit", (e) => {
  const uid = $("#uid").value.trim();
  const pw = $("#upw").value;
  if (!uid || !pw) {
    e.preventDefault();   // 폼 전송(페이지 이동)을 막음
    report(emptyLoginReport(...));
  }
});`,
        server: `# 서버까지 요청이 가지 않음

# 서버에도 같은 검사가 있음 (check_login)
if not uid or not pw:
    return False, "아이디와 비밀번호를 모두 입력하세요."`,
    },
    fetchEmpty: {
        client: `const uid = $("#uid").value.trim();
const pw = $("#upw").value;
if (!uid || !pw)
  return report(emptyLoginReport(...));  // fetch 전에 중단`,
        server: `# 서버까지 요청이 가지 않음

# 서버에도 같은 검사가 있음 (check_login)
if not uid or not pw:
    return False, "아이디와 비밀번호를 모두 입력하세요."`,
    },
    login: {
        client: `// call(): fetch()를 보내고 JSON까지 받아 오는 공통 함수
const c = await call("POST", "/api/login", { id: uid, pw });
//   = fetch("/api/login", {
//       method: "POST",
//       headers: { "Content-Type": "application/json" },
//       body: JSON.stringify({ id: uid, pw }) })
if (c.res.ok) setLoginState(c.data.user);  // 상단 글자만 바꿈
else report(...);                          // 예외창`,
        server: `@app.route("/api/login", methods=["POST"])
def api_login():
    data = request.get_json(silent=True) or {}
    uid = str(data.get("id", "")).strip()
    pw = str(data.get("pw", ""))
    ok, why = check_login(uid, pw)
    if not ok:
        return reply(401 if uid and pw else 400, ok=False, error=why)
    session["user"] = uid        # 로그인 상태 저장 (쿠키)
    return reply(ok=True, user=uid)

def check_login(uid, pw):
    if not uid or not pw: return False, "...모두 입력하세요."
    if uid not in USERS:  return False, "...틀렸습니다."
    if USERS[uid] != pw:  return False, "...틀렸습니다."
    return True, ""`,
    },
    me: {
        client: `const c = await call("GET", "/api/me");
// session 쿠키는 브라우저가 자동으로 붙여 보냄
setLoginState(c.res.ok ? c.data.user : null);`,
        server: `@app.route("/api/me")
def api_me():
    user = session.get("user")
    if not user:
        return reply(401, ok=False, error="로그인하지 않은 상태입니다.")
    return reply(ok=True, user=user)`,
    },
    logout: {
        client: `const c = await call("POST", "/api/logout");
if (c.res.ok) setLoginState(null);`,
        server: `@app.route("/api/logout", methods=["POST"])
def api_logout():
    user = session.pop("user", None)   # 로그인 정보 삭제
    return reply(ok=True, was=user)`,
    },
    reset: {
        client: `$("#uid").value = "id";
$("#upw").value = "1";
// fetch 없음 → 서버와 통신하지 않음`,
        server: `# 서버 코드 없음 (서버와 통신하지 않는 버튼)`,
    },
    memoAdd: {
        client: `const text = $("#memo-text").value.trim();
if (!text) return report(...);              // 빈 값이면 중단
const c = await call("POST", "/api/memos", { text });
if (c.res.ok) $("#memo-list").append(memoItem(c.data.memo));`,
        server: `@app.route("/api/memos", methods=["POST"])
def memo_add():
    user = session.get("user")
    if not user:
        return reply(401, ok=False, error="로그인해야 ...")
    text = str((request.get_json(silent=True) or {}).get("text", "")).strip()
    if not text:
        return reply(400, ok=False, error="메모 내용이 비어 있습니다.")
    memo = {"no": memo_seq, "text": text, "user": user, ...}
    memos.append(memo)                  # DB라면 INSERT
    return reply(201, ok=True, memo=memo)`,
    },
    memoList: {
        client: `const c = await call("GET", "/api/memos");
if (c.res.ok) renderMemos(c.data.memos);  // 목록 통째로 다시 그림`,
        server: `@app.route("/api/memos")
def memo_list():
    items = list(memos)                 # DB라면 SELECT
    return reply(ok=True, memos=items)`,
    },
    memoDelete: {
        client: `// 삭제 버튼은 나중에 생기므로 ul에 이벤트를 걸어 둠 (이벤트 위임)
$("#memo-list").addEventListener("click", async (e) => {
  const btn = e.target.closest("button[data-no]");
  const c = await call("DELETE", \`/api/memos/\${btn.dataset.no}\`);
  if (c.res.ok) btn.closest("li").remove();
});`,
        server: `@app.route("/api/memos/<int:no>", methods=["DELETE"])
def memo_delete(no):
    if not session.get("user"):
        return reply(401, ok=False, error="로그인해야 ...")
    found = next((m for m in memos if m["no"] == no), None)
    if not found:
        return reply(404, ok=False, error=f"{no}번 메모를 찾을 수 없습니다.")
    memos.remove(found)                 # DB라면 DELETE
    return reply(ok=True, no=no)`,
    },
    search: {
        client: `const q = $("#q").value.trim();
const c = await call("GET", \`/api/products?q=\${encodeURIComponent(q)}\`);
if (c.res.ok) renderProducts(c.data.items);`,
        server: `@app.route("/api/products")
def products():
    q = request.args.get("q", "").strip()   # 쿼리스트링 읽기
    found = [p for p in PRODUCTS if q in p["sang"]]
    return reply(ok=True, q=q, items=found)`,
    },
    e404: {
        client: `const c = await call("GET", "/api/nothing");
// fetch는 404도 '도착'으로 처리 → 직접 확인
if (!c.res.ok) report(...);   // 예외창`,
        server: `# /api/nothing 에 해당하는 @app.route가 없음

@app.errorhandler(404)
def not_found(e):
    return reply(404, "not_found", ok=False,
                 error=f"'{request.path}' 주소가 서버에 없습니다.")`,
    },
    e500: {
        client: `const c = await call("GET", "/api/error");
if (!c.res.ok) report(...);   // 예외창`,
        server: `@app.route("/api/error")
def error_demo():
    total, count = 100, 0
    return reply(ok=True, avg=total / count)  # ZeroDivisionError

@app.errorhandler(ZeroDivisionError)
def on_zero_division(e):
    return reply(500, "error_demo", ok=False,
                 error="서버 코드에서 오류가 발생했습니다 (0으로 나누기).")`,
    },
    timeout: {
        client: `// call() 안: 제한 시간이 지나면 요청 취소
const ctrl = new AbortController();
setTimeout(() => ctrl.abort(), 1500);
try {
  await fetch("/api/slow?ms=3000", { signal: ctrl.signal });
} catch (err) {
  // err.name === "AbortError" → 시간 초과 예외창
}`,
        server: `@app.route("/api/slow")
def slow():
    ms = min(max(request.args.get("ms", 3000, type=int), 0), 5000)
    time.sleep(ms / 1000)        # 오래 걸리는 작업 흉내
    return reply(ok=True, ms=ms)`,
    },
};

// ===================== 시작: 폼 제출 뒤 다시 그려진 페이지라면 결과 알림창 =====================
if (PAGE.last) report(formLoginReport(PAGE.last, PAGE.index));
