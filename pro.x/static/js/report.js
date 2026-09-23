// pro.x/static/js/report.js
// 브라우저단 코드. 서버는 이 파일을 "정적 파일"로 그대로 보내고, 실행은 브라우저에서만 일어난다.

const R = window.REPORT;                        // 서버(Jinja2)가 tojson으로 넘겨준 값
const $ = (sel) => document.querySelector(sel);

// ===================== 공통 도구 =====================
const pad = (n, w = 2) => String(n).padStart(w, "0");

function fmtTime(ms) {
    const d = new Date(ms);
    return `${pad(d.getHours())}:${pad(d.getMinutes())}:${pad(d.getSeconds())}.${pad(d.getMilliseconds(), 3)}`;
}

function fmtMs(ms) {
    if (ms == null || Number.isNaN(ms)) return "-";
    const a = Math.abs(ms);
    if (a < 10) return ms.toFixed(1) + "ms";
    if (a < 1000) return Math.round(ms) + "ms";
    if (a < 60000) return (ms / 1000).toFixed(2) + "초";
    return `${Math.floor(ms / 60000)}분 ${Math.floor((ms % 60000) / 1000)}초`;
}

// 사용자 입력을 innerHTML에 넣기 전에 태그 문자를 바꿔 XSS를 막는다
function escapeHtml(s) {
    return String(s).replace(/[&<>"']/g, (c) =>
        ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
}

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
// 화면이 한 번 그려진 뒤 진행 (탭이 가려져 rAF가 멈춰도 0.1초 뒤에는 진행)
const nextPaint = () => new Promise((r) => {
    requestAnimationFrame(() => setTimeout(r, 0));
    setTimeout(r, 100);
});
const clamp = (v, lo, hi) => Math.min(Math.max(v, lo), hi);
const jsonPost = (obj) => ({
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(obj),
});

// 매 프레임 쓰는 요소는 미리 찾아 둔다
const els = {
    clkBrowser: $("#clk-browser"),
    clkPoll: $("#clk-poll"),
    clkSse: $("#clk-sse"),
    hbDot: $("#hb-dot"),
    hbMax: $("#hb-max"),
    waterfall: $("#waterfall"),
    logBody: $("#log-body"),
    showPoll: $("#show-poll"),
};

// ===================== 시계 상태 =====================
const clock = {
    best: { net: Infinity, offset: 0 }, // 가장 빠른 왕복에서 구한 시계 차이(서버 − 브라우저)
    poll: null,                         // 폴링으로 받은 서버 시각
    sse: null,                          // SSE로 받은 서버 시각
};
let pollCount = 0;
let sseCount = 0;

// 요청 1번의 시각 4개로 왕복시간과 시계 차이를 계산한다
//   t0: 브라우저가 보냄 → recv: 서버가 받음 → send: 서버가 보냄 → t3: 브라우저가 받음
function measure({ t0, t3, rtt }, data) {
    const offset = ((data.recv_ms - t0) + (data.send_ms - t3)) / 2; // NTP 방식: 가는 길 = 오는 길 가정
    const net = rtt - (data.send_ms - data.recv_ms);                // 서버 처리 시간을 뺀 순수 왕복
    if (net <= clock.best.net) clock.best = { net, offset };
    $("#m-rtt").textContent = fmtMs(rtt);
    $("#m-offset").textContent = (clock.best.offset >= 0 ? "+" : "") + fmtMs(clock.best.offset);
    $("#sum-rtt").textContent = fmtMs(Math.max(0, clock.best.net));
}

// ===================== 4-A 흐름 그림: 점 애니메이션 =====================
const SVGNS = "http://www.w3.org/2000/svg";
const LANES = { req: [170, 548, 52], res: [550, 172, 102], sse: [550, 172, 158] }; // [시작x, 끝x, y]
let inFlight = 0;

function shootDot(lane) {
    const layer = $("#flow-dots");
    if (!layer || document.hidden || layer.childElementCount > 40) return Promise.resolve();
    const [x1, x2, y] = LANES[lane];
    const dot = document.createElementNS(SVGNS, "circle");
    dot.setAttribute("r", 6);
    dot.setAttribute("cx", 0);
    dot.setAttribute("cy", y);
    dot.setAttribute("class", `dot ${lane}`);
    layer.appendChild(dot);
    const anim = dot.animate(
        [{ transform: `translateX(${x1}px)` }, { transform: `translateX(${x2}px)` }],
        { duration: 480, easing: "ease-in-out", fill: "forwards" },
    );
    return anim.finished.then(() => dot.remove(), () => dot.remove());
}

function setBusy(delta) {
    inFlight += delta;
    const busy = inFlight > 0;
    $("#flow-server").classList.toggle("busy", busy);
    const label = $("#flow-busy");
    label.textContent = busy ? `처리 중 ${inFlight}건` : "대기 중";
    label.classList.toggle("busy", busy);
}

// 요청 점이 서버에 닿으면 '처리 중', 응답이 오면 응답 점을 돌려보낸다
async function track(send) {
    const arrived = shootDot("req").then(() => setBusy(+1));
    try {
        return await send();
    } finally {
        arrived.then(() => { setBusy(-1); shootDot("res"); });
    }
}

// ===================== 시간을 재는 요청 함수 =====================
function timedFetch(url, options = {}) {
    return track(async () => {
        const t0 = Date.now();
        const p0 = performance.now();
        const res = await fetch(url, options);          // 비동기: 기다리는 동안 브라우저는 다른 일을 한다
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        const data = await res.json();
        const rtt = performance.now() - p0;
        return { data, t: { t0, t3: t0 + rtt, rtt } };
    });
}

function syncXhr(url) {
    return track(async () => {
        await nextPaint();                              // 요청 점이 한 번은 그려진 뒤 멈추도록
        const t0 = Date.now();
        const p0 = performance.now();
        const xhr = new XMLHttpRequest();
        xhr.open("GET", url, false);                    // 세 번째 인자 false = 동기: 응답이 올 때까지 여기서 멈춤
        xhr.send();
        const rtt = performance.now() - p0;
        if (xhr.status !== 200) throw new Error(`HTTP ${xhr.status}`);
        // send()에서 기다린 시간 = 메인 스레드가 통째로 멈춰 있던 시간
        return { data: JSON.parse(xhr.responseText), t: { t0, t3: t0 + rtt, rtt }, blocked: rtt };
    });
}

// ===================== ③ 폴링 =====================
let pollGen = 0; // 간격을 바꾸면 이전 반복을 멈추기 위한 번호

async function pollLoop(gen) {
    const interval = Number($("#poll-interval").value);
    if (!interval || gen !== pollGen) return;
    try {
        const { data, t } = await timedFetch("/api/time?via=poll");
        measure(t, data);
        clock.poll = { serverMs: data.send_ms };
        els.clkPoll.textContent = fmtTime(data.send_ms);
        pollCount++;
        $("#m-polls").textContent = pollCount;
        $("#sum-polls").textContent = pollCount;
    } catch (err) {
        els.clkPoll.textContent = "연결 실패";
    }
    if (gen === pollGen) setTimeout(() => pollLoop(gen), interval);
}

$("#poll-interval").addEventListener("change", () => {
    pollGen++;
    pollLoop(pollGen);
});

// ===================== ④ SSE + 4-C 서버 로그 =====================
const logs = [];        // 받은 로그 (최신이 앞)
const seen = new Set(); // 중복 방지용 요청 번호
let pollLogCount = 0;
let bootId = null;      // 서버가 재시작되면 요청 번호가 1부터 다시 시작하므로 구분용

function connectSSE() {
    const es = new EventSource("/api/stream"); // 연결 1개를 열어 두고, 서버가 보낼 때마다 이벤트가 온다
    const pill = $("#sse-status");
    es.onopen = () => { pill.textContent = "SSE 연결됨"; pill.className = "pill on"; };
    es.onerror = () => { pill.textContent = "SSE 재연결 중…"; pill.className = "pill off"; }; // 자동 재연결

    const received = () => {
        sseCount++;
        $("#m-sse").textContent = sseCount;
        $("#sum-sse").textContent = sseCount;
        shootDot("sse");
    };

    es.addEventListener("tick", (e) => {
        received();
        const d = JSON.parse(e.data);
        clock.sse = { serverMs: d.server_ms };
        els.clkSse.textContent = fmtTime(d.server_ms);
        $("#sse-raw").textContent = `event: tick\ndata: ${e.data}`;
        $("#m-uptime").textContent = fmtMs(d.uptime_s * 1000);
        $("#log-total").textContent = d.requests;
    });
    es.addEventListener("log", (e) => { received(); addLog(JSON.parse(e.data), true); });
    es.addEventListener("clients", (e) => { received(); $("#m-clients").textContent = JSON.parse(e.data).count; });
    es.addEventListener("hello", (e) => {
        received();
        const d = JSON.parse(e.data);
        if (bootId !== null && bootId !== d.boot) { logs.length = 0; seen.clear(); pollLogCount = 0; }
        bootId = d.boot;
        d.logs.forEach((l) => addLog(l, false));
        renderLogs();
    });
}

function logRow(l, flash) {
    const other = l.client !== R.myAddr;
    const tr = document.createElement("tr");
    tr.className = [l.poll ? "poll" : "", flash ? "new" : ""].join(" ").trim();
    tr.innerHTML = `
        <td>${l.no}</td>
        <td>${escapeHtml(l.time)}</td>
        <td class="m-${escapeHtml(l.method)}">${escapeHtml(l.method)}</td>
        <td class="path">${escapeHtml(l.path)}</td>
        <td><span class="sc sc${String(l.status)[0]}">${l.status}</span></td>
        <td>${fmtMs(l.ms)}</td>
        <td class="${other ? "other" : ""}">${escapeHtml(l.client)}${other ? " · 다른 기기" : ""}</td>`;
    return tr;
}

function updateLogCounters() {
    $("#hidden-polls").textContent = els.showPoll.checked ? 0 : pollLogCount;
}

function renderLogs() {
    const rows = logs.filter((l) => els.showPoll.checked || !l.poll).slice(0, 60);
    els.logBody.replaceChildren(...rows.map((l) => logRow(l, false)));
    if (!rows.length) {
        els.logBody.innerHTML = `<tr><td colspan="7" class="empty">아직 표시할 요청이 없다.</td></tr>`;
    }
    updateLogCounters();
}

function addLog(entry, live) {
    if (seen.has(entry.no)) return;
    seen.add(entry.no);
    if (entry.poll) pollLogCount++;
    logs.unshift(entry);
    if (logs.length > 200) seen.delete(logs.pop().no);
    updateLogCounters();
    if (!live) return;                                  // 처음 받은 지난 로그는 renderLogs()로 한 번에 그림
    if (entry.poll && !els.showPoll.checked) return;
    els.logBody.querySelector("td.empty")?.parentElement.remove();
    els.logBody.prepend(logRow(entry, true));           // 새 로그만 맨 위에 추가 (깜빡임 효과)
    while (els.logBody.rows.length > 60) els.logBody.lastElementChild.remove();
}

els.showPoll.addEventListener("change", renderLogs);

// ===================== 메인 스레드 멈춤 측정 =====================
// 50ms마다 도는 타이머가 늦게 실행된 만큼 = 메인 스레드가 다른 일(예: 동기 요청)에 붙잡혀 있던 시간
const BEAT = 50;
let lastBeat = performance.now();
let maxLag = 0;
setInterval(() => {
    const now = performance.now();
    const lag = now - lastBeat - BEAT;
    lastBeat = now;
    if (!document.hidden && lag > maxLag) maxLag = lag;
}, BEAT);
document.addEventListener("visibilitychange", () => { lastBeat = performance.now(); });

// ===================== 4-B 요청 실험 =====================
const EXPERIMENTS = {
    get: async () => [{ label: "GET /api/time", ...(await timedFetch("/api/time")) }],
    post: async () => [{ label: "POST /api/echo", ...(await timedFetch("/api/echo", jsonPost({ text: "hello flask" }))) }],
    async: async () => [{ label: "비동기 fetch · 서버 1.5초", ...(await timedFetch("/api/slow?ms=1500&mode=async")) }],
    sync: async () => [{ label: "동기 XHR · 서버 1.5초", ...(await syncXhr("/api/slow?ms=1500&mode=sync")) }],
    parallel: () => Promise.all([1, 2, 3].map(async (i) => ({
        label: `동시 요청 ${i}/3 · 1초`,
        ...(await timedFetch(`/api/slow?ms=1000&n=${i}`)),
    }))),
};
const rows = []; // 타임라인에 그릴 요청들 (최신이 앞)

// 서버가 알려준 recv/send 시각으로 한 요청을 요청 · 서버 처리 · 응답 세 구간으로 나눈다
function toRow(r, lag) {
    const { t0, rtt } = r.t;
    const server = clamp(r.data.send_ms - r.data.recv_ms, 0, rtt);
    const recvLocal = r.data.recv_ms - clock.best.offset; // 서버 시각 → 브라우저 시각으로 환산
    const up = clamp(recvLocal - t0, 0, rtt - server);
    return { label: r.label, t0, total: rtt, up, server, down: rtt - server - up, thread: r.data.thread, lag };
}

function renderWaterfall() {
    const max = Math.max(...rows.map((r) => r.total));
    const pct = (v) => (v / max) * 100 + "%";
    els.waterfall.innerHTML = rows.map((r) => `
        <div class="wf-row">
            <div class="wf-label"><b>${escapeHtml(r.label)}</b><span>${fmtTime(r.t0)} · ${escapeHtml(r.thread)}</span></div>
            <div class="wf-track">
                <span class="seg up" style="width:${pct(r.up)}"></span><span class="seg server" style="width:${pct(r.server)}"></span><span class="seg down" style="width:${pct(r.down)}"></span>
            </div>
            <div class="wf-total">${fmtMs(r.total)}</div>
            <div class="wf-detail">요청 ${fmtMs(r.up)} · 서버 처리 ${fmtMs(r.server)} · 응답 ${fmtMs(r.down)}
                · 메인 스레드 최대 멈춤 <b class="${r.lag > 200 ? "bad" : "ok"}">${fmtMs(r.lag)}</b></div>
        </div>`).join("");
}

document.querySelectorAll("[data-exp]").forEach((btn) => {
    btn.addEventListener("click", async () => {
        btn.disabled = true;
        await nextPaint();              // 버튼이 눌린 모습이 먼저 그려지도록
        maxLag = 0;                     // 이 실험 동안의 메인 스레드 멈춤 측정 시작
        lastBeat = performance.now();
        let results = [];
        try {
            results = await EXPERIMENTS[btn.dataset.exp]();
        } catch (err) {
            els.waterfall.insertAdjacentHTML("afterbegin", `<p class="empty">요청 실패: ${escapeHtml(err.message)}</p>`);
        }
        await sleep(120);               // 멈춰 있던 타이머가 한 번 더 돌아 멈춘 시간을 기록하도록
        const lag = Math.max(0, maxLag, ...results.map((r) => r.blocked ?? 0));
        results.forEach((r) => measure(r.t, r.data));
        rows.unshift(...results.map((r) => toRow(r, lag)));
        rows.splice(10);
        if (rows.length) renderWaterfall();
        els.hbMax.textContent = fmtMs(lag);
        els.hbMax.className = lag > 200 ? "bad" : "ok";
        btn.disabled = false;
    });
});

// ===================== 2-1 HTTP 응답 보기 =====================
$("#btn-response").addEventListener("click", async () => {
    const out = $("#http-response");
    try {
        const res = await fetch("/api/time");
        const body = await res.json();
        const lines = [`${body.protocol} ${res.status} ${res.statusText}`];
        res.headers.forEach((v, k) => lines.push(`${k}: ${v}`));
        lines.push("", JSON.stringify(body, null, 2));
        out.textContent = lines.join("\n");
    } catch (err) {
        out.textContent = "요청 실패: " + err.message;
    }
});

// ===================== 4-D CSR: fetch POST로 부분 갱신 =====================
$("#csr-form").addEventListener("submit", async (e) => {
    e.preventDefault();                 // form의 기본 동작(페이지 이동)을 막는다 → 새로고침 없음
    const box = $("#csr-result");
    box.textContent = "서버에 보내는 중…";
    try {
        const { data, t } = await timedFetch("/api/echo", jsonPost({ text: $("#csr-text").value }));
        measure(t, data);
        // 받은 JSON으로 브라우저가 HTML을 만든다 (사용자 입력은 escape 후 삽입)
        box.innerHTML = `<dl>
            <dt>서버가 받은 값</dt><dd>${escapeHtml(data.received) || "(빈 문자열)"}</dd>
            <dt>대문자</dt><dd>${escapeHtml(data.upper)}</dd>
            <dt>글자 수</dt><dd>${data.length}</dd>
            <dt>뒤집기</dt><dd>${escapeHtml(data.reversed)}</dd>
            <dt>서버 시각</dt><dd>${escapeHtml(data.server_time)} · RTT ${fmtMs(t.rtt)}</dd>
        </dl>`;
    } catch (err) {
        box.textContent = "요청 실패: " + err.message;
    }
});

// 서버가 보낸 원본 HTML과 JS가 고친 현재 DOM 비교
$("#btn-source").addEventListener("click", async () => {
    const html = await (await fetch(location.pathname + location.search)).text();
    const doc = new DOMParser().parseFromString(html, "text/html"); // 문자열 → 문서 (script는 실행 안 됨)
    const pick = (root) => ["#ssr-result", "#csr-result"]
        .map((sel) => root.querySelector(sel)?.outerHTML ?? "(없음)")
        .join("\n\n");
    $("#raw-html").textContent = pick(doc);
    $("#live-dom").textContent = pick(document);
});

// ===================== ② 브라우저 시계 + 데이터 나이 (매 프레임) =====================
const AGE_FULL = 2000; // 이 나이가 되면 막대가 가득 차고 빨갛게 변함

function setAge(key, ageMs) {
    const a = Math.max(0, ageMs);
    const bar = $(`#bar-${key}`);
    bar.style.width = Math.min(a / AGE_FULL, 1) * 100 + "%";
    bar.classList.toggle("stale", a >= AGE_FULL);
    $(`#age-${key}`).textContent = fmtMs(a);
}

function frame() {
    const now = Date.now();
    const serverNow = now + clock.best.offset;   // 지금 서버 시계는 몇 시일지 추정
    els.clkBrowser.textContent = fmtTime(now);
    setAge("ssr", serverNow - R.renderedMs);
    if (clock.poll) setAge("poll", serverNow - clock.poll.serverMs);
    if (clock.sse) setAge("sse", serverNow - clock.sse.serverMs);
    els.hbDot.style.left = ((performance.now() % 1500) / 1500) * 100 + "%"; // 메인 스레드가 살아 있으면 계속 움직임
    requestAnimationFrame(frame);
}

// ===================== 시작 =====================
$("#age-browser").textContent = "항상 0 (지금 이 순간)";
connectSSE();
pollLoop(pollGen);
requestAnimationFrame(frame);
