// 화살표 함수 객체 생성 후 $에 할당
const $= (sel) => document.querySelector(sel)
// function $(sel){ //sel은 element이거나 클래스이거나 등등..
// return document.querySelector(sel) sel을 반환}
//ex) $("sendBtn")하면 return document.querySelector(sel)이 실행
// sendBtn이 sel로 전달됨

$("#sendBtn").addEventListener("click",async() => {//비동기 처리. //버튼(#sendBtn)에서 클릭 사건(이벤트)이 발생하면 뒤에 오는 함수를 실행
    const name =$("#name").value.trim(); //id가 name인 객체를 sel로 넘겨주고 그 값을 공백 제거하고 봄. 위에 함수 선언해놔서 지속적으로 사용 가능
    //const name =DocumentTimeline.querySelector("#name").value.trim(); //위와 동일
    const age=$("#age").value.trim();
    //const params ={name,age}; // 이래도 실행하면 "get요청"버튼 누르면 console창에 `/api/friend?{params}` 이렇게 뜸
    const params =new URLSearchParams({name,age}); // 공백, 한글이 포함된 경우 자동 인코딩
    const url=`/api/friend?${params}`; 

    $("#result").textContent = "요청 중..." // 서버에 자료요청 시간이 길어지면 보이는 메세지

    try{
        const res = await fetch(url,{
            method: "GET",
            headers:{"Accept":"application/json"} //get 방식으로 요청된 자료를 json 타입으로 반환한다.
        });

        const data=await res.json(); //응답 본문을 JSON으로 파싱해서 JS 객체화
        //alert(data);

        if (!res.ok||data.ok===false){ //ok 데이터가 없으면
        $("#result").innerHTML =`<span class="error">에러 : ${data.error}</span>`;
        return; }
        
        
        // 요청 성공인 경우
        $("#result").innerHTML=`
        <div>이름:${data.name}</div>
        <div>나이:${data.age}</div>
        <div>연령대:${data.age_group}</div>
        <div>메세지:${data.message}</div>
        `;

    }catch(err){
        $("#result").innerHTML =`<span class="error">네트워크 파싱 오류 : ${err}</span>`;
    }


})
//###########################################################################################################
// 동기(Synchronous):
// 코드가 순서대로 하나씩 실행되는 방식입니다. 앞 작업이 끝날 때까지 다음 작업이 기다립니다.

// 비동기(Asynchronous):
// 시간이 오래 걸리는 작업(예: 서버 데이터 요청(API 호출), 파일 읽기, 타이머)을 뒤에서 처리하도록 맡겨두고,
// 다음 코드를 바로 먼저 실행하는 방식입니다.