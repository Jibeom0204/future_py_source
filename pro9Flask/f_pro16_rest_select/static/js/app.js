const btnJikwon= document.querySelector("#btnJikwon")
const btnOne= document.querySelector("#btnOne")
const btnBuser= document.querySelector("#btnBuser")
const btnBuserPart= document.querySelector("#btnBuserPart")


const jikwonno= document.querySelector("#jikwonno")
const buserno= document.querySelector("#buserno")

const msg= document.querySelector("#msg")
const thead= document.querySelector("#thead")
const tbody= document.querySelector("#tbody")

function setMsg(text){
    msg.textContent=text;
}

function clearTable(){
    thead.innerHTML="";
    tbody.innerHTML="";
    //이게 DOM? DOM의 개념이 뭐고 어케 사용하노
}

function makeTable(rows){
    clearTable(); // 초기값으로 비우고 시작

     if(!rows||rows.length===0)//rows가 없거나 길이가 0이면. --> 길이가 0이면 없는것과 같다
     {
        setMsg("자료 없음"); // setMsg함수의 인자에 문자열을 넣어 호출
        return;
     }

     let header = "<tr>";
     Object.keys(rows[0]).forEach(key =>{
        header +="<th>" + key +"</th>" //key에 컬럼명이 들어감
        //문자열을 forEACH로 돌릴 수 없음 그래서 JSON 형식으로 만들어줘야함
        //그래서 웹이랑 서버 소통할 때 JSON 사용하는거임. 맞나?
     });
     header+="<tr>";
     thead.innerHTML=header; //위에서 작업한 컬럼명을 초기값으로 지정

     rows.forEach(r =>{
        let tr="<tr>"
        Object.values(r).forEach(v =>{
        tr +="<td>" + v +"</td>" //key에 컬럼명이 들어감
     });
        tr +="</tr>" // +=을 사용해서 변수의 값을 누적함. 이제야 기억난다.
        tbody.innerHTML+=tr;
     });
}

// 전체 직원
async function loadJikwon(){
    const res =await fetch("/acorn/jikwon")
    const mydata= await res.json();//aixos 사용하지 않고 fetch 사용해서 사용자가 직접 json으로 바꿔줘야함. 이해하려면 promise 객체를 알아야함. 따로 공부하자
    //mydata에 직원 전체 정보가 담겨져 있다. 뭘로 받아온거지?
    makeTable(mydata.data) // 전체 직원에 정보를 받은 변수  "mydata"의 .data를 maketable()함수의 인자로 넘겨줌
    setMsg("전체 직원 조회 완료")
}

// 직원 1명
async function loadOne(){
    const no=jikwonno.value; //번호를 받고
    const res =await fetch("/acorn/jikwon/"+ no);//번호를 전달함 -> 이게 rest full이라고?
    // const res =await fetch("/acorn/jikwon/"+ no,{
    //     method:"GET" //위와 같은 방식
    // })
    const mydataOne= await res.json();
    makeTable([mydataOne.data]) // 1명이라 리스트에 담음. 객체 하나씩 담으면 for로 돌릴 수 있기 때문에 이렇게 함
    setMsg("직원 1명 조회 완료")
}


// 부서 전체 조회
async function loadBuser(){
    const res =await fetch("/acorn/buser")
    const myBuserdata= await res.json();
    makeTable(myBuserdata.data) 
    // fetchone()	{...} (dict 하나) --> [data]로 감싸야 함
    // fetchall()	[{...}, {...}, ...] (이미 리스트)
    setMsg("전체 부서 조회 완료")
}


// 특정 부서
async function loadBuserOne(){
    const no=buserno.value; //번호를 받고
    const res =await fetch("/acorn/buser/"+ no);
    const myBuserdataOne= await res.json();
    makeTable(myBuserdataOne.data) // 부서 안에 모든 사람들의 값을 출력해야하니 통째로 넘겨줘야한다. 1명 조회 하는것처럼 []리스트에 담아보내면 안된다.

    // fetchone()	{...} (dict 하나) --> [data]로 감싸야 함
    // fetchall()	[{...}, {...}, ...] (이미 리스트)
    setMsg("{myBuserdataOne}번 부서 조회 완료") 
}

btnJikwon.onclick=loadJikwon;// 함수의 결과를 반환하면 안됨 loadJikwon() x --> 왜? 
btnOne.onclick=loadOne;
btnBuser.onclick=loadBuser;
btnBuserPart.onclick=loadBuserOne;