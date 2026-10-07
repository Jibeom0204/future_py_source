//엘리멘트(요소) 얻기
const code=document.querySelector("#code");
const sang=document.querySelector("#sang");
const su=document.querySelector("#su");
const dan=document.querySelector("#dan");

const msg=document.querySelector("#msg");
const tbody=document.querySelector("#tbody");

const btnAdd=document.querySelector("#btnAdd");
const btnUpdate=document.querySelector("#btnUpdate");
const btnDelete=document.querySelector("#btnDelete");
// const btnReload=document.querySelector("#btnReload");

function setMsg(text){
    msg.textContent=text;
}

//입력폼 초기화
function clearForm(){
    code.value="";
    sang.value="";
    su.value="";
    dan.value="";
    code.focus();
}


//전체 자료 읽기-- 시작 시, 추가 후 호출. 총 2번 실행된다.
async function loadAll(){
    const res =await fetch("/api/sangdata",{method:"GET"});
    const result_datas=await res.json(); //app.py에서 db에서 불러오고 sql로 정리한 값을 result_datas에 저장하여 가져옴.
    // 가져온 값을 json형식으로 가공. AXIOS가 아니라 일일이 JSON으로 가공해줘야함.
    // console.log(datas);
    // alert(datas);

    tbody.innerHTML="";

    result_datas.datas.forEach(r => {
        const tr =document.createElement("tr"); //??? 무슨 기능이고 왜 쓰지
        tr.innerHTML=
        "<td>"+r.code+"</td>"+
        "<td>"+r.sang+"</td>"+
        "<td>"+r.su+"</td>"+     
        "<td>"+r.dan+"</td>";
        tbody.appendChild(tr);
    });
    clearForm(); // 추가 이후 입력폼이 비워지는 기능이 실행이 됨
    // setMsg("조회완료");
}

// 상품추가
async function addData(){
    alert("add");
    //입력자료  검사가 끝났다고 가정하고 아래 문장 실행
    const add_data={
        code:code.value,
        sang:sang.value,
        su:Number(su.value),
        dan:Number(dan.value)
    }
    // alert (add_data); //object:object 팝업 출력
    // alert(JSON.stringify(add_data))//js 객체를 JS 문자열로 변환. 


    // 브라우저랑 서버가 소통할 때는 객체를 인식하지 못한다. 무조건 문자열만 인식한다.
    // 따라서 객체를 문자열로 바꿔주는데 JSON 형식이 처리하기 쉬워 JSON 문자열로 변환해서 보내준다.
    const res =await fetch("/api/sangdata",
    {
    method:"POST",
    headers:{"Content-Type":"application/json"},
    body:JSON.stringify(add_data) //js객체를 json 문자열로 변환해 서버로 전송
    });

    await res.json();
    setMsg("추가 완료");
    clearForm();

    loadAll(); //추가 후 전체자료 내보내기
}



// 상품 수정
async function updateData(){
    //입력자료  검사가 끝났다고 가정하고 아래 문장 실행
    const up_data={
        sang:sang.value,
        su:Number(su.value),
        dan:Number(dan.value)
    }

    const res =await fetch("/api/sangdata/"+code.value,
    {
    method:"PUT", //자료수정
    headers:{"Content-Type":"application/json"},
    body:JSON.stringify(up_data)
    });

    const imsi=await res.json();
    if(imsi.ok)
        setMsg("수정 완료");
    else
        setMsg("수정 실패");
    clearForm();
    
    loadAll(); //수정 후 전체자료 보기
}

// 자료 삭제
async function deleteData(){
    //입력자료  검사가 끝났다고 가정하고 아래 문장 실행

    if(!code.value.trim()){
        alert("삭제할 상품 코드를 입력하세요");
        code.focus();
        return;
    }
    
    const res =await fetch("/api/sangdata/"+code.value, {method:"DELETE"} );

    const imsi=await res.json();
    if(imsi.ok)
        setMsg(imsi.msg);
    else
        setMsg("삭제 실패: "+imsi.msg);
    clearForm();

    loadAll();
}

window.onload=loadAll;
btnAdd.onclick=addData;
btnUpdate.onclick=updateData;
btnDelete.onclick=deleteData;