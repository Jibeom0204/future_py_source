from flask import Flask, render_template,render_template_string, request,make_response,redirect,url_for,flash
# pip install pymysql
import pymysql
import os
from flask import get_flashed_messages # 저장해둔 메세지를 꺼내는 함수
# 예: flash("에러~~") -> 메세지를 세션에 잠시 저장 후 get_flashed_messsage만나면 메세지 읽기 가능

app=Flask(__name__);
app.secret_key="abcd1234" # 쿠키 서명용 비밀키

#MariaDB 연결정보
DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
DB_PORT = int(os.getenv("DB_PORT", "3306"))
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "123")
DB_NAME = os.getenv("DB_NAME", "test")

def get_conn():
    return pymysql.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        charset="utf8mb4" ,# 전세계 문자(한글 포함)+이모지까지 처리가능
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=False
    )
    # DictCursor: select 결과를  'dict type'형태로 접근 가능
    # 예: {'code':1 'sang':'mouse' ...} --> row['code'], row['sang'] 가능. 원래는 row[0] 이런식

@app.get("/") # 기본요청이라 "주소에 경로 없이 host:포트만 입력해도" 이게 실행됨
              # localhost:5000 -> 이 자체가 루트(/)임. "주소 뒤에 /는 브라우저가 자동으로 붙여서 요청함"
def index():
   return redirect(url_for("show_list")) # 33번 줄에서 /(루트)요청이 들어오면 show_list 함수를 호출해서 실행

##################################
@app.get("/show/") #get 방식으로 show_list 함수가 호출되면 show 요청을 실행
def show_list():
    conn=get_conn()

    try:
        with conn.cursor() as cur:
            cur.execute("select code, sang,su,dan from sangdata order by code asc") # DB와 연결. 쿼리 작성 및 실행
            rows = cur.fetchall() # 모두 한 줄씩 출력

        messages=list(get_flashed_messages()) #어디선가 발생하는 메세지를 리스트형식으로 받아서"messages"에 저장
        return render_template("list.html",rows=rows, messages=messages)
        # 쿼리문의 결과와 알람 메세지를 받아 list.html에 렌더링해서 전달

    except pymysql.err.IntegrityError as e:
        print(e)

    except Exception as e2:
        print(e2)

    finally:
        conn.close()
##################################

# 추가 단
######################################################################################################
####################################################################
@app.get("/add/") # list.html의 <a href="{{'add'}}">[상품 추가]</a>와 연동
def add_form(): # list.html의 <a href="{{'add_form'}}">과 연동. 둘 다 이 코드를 실행하는 역할은 같지만 실행하는 방식이 다름
    messages=list(get_flashed_messages())
    return render_template("form_add.html",messages=messages)
####################################################################

####################################################################
@app.post("/add/") # 같은 이름이어도 방식이 다르면 구동이 달라짐
def add_save(): # 추가처리
    sang=(request.form.get("sang")or"").strip() # post 방식이니까 html엣 <form> 태그 써야하고
    su_raw=(request.form.get("su")or"").strip() # form 태그 썼으니까 서버에서 request.form으로 받는다
    dan_raw=(request.form.get("dan")or"").strip()
    
    # 서버에서 클라이언트가 전달한 입력자료 검사
    if not sang or not su_raw.isdigit()or not dan_raw.isdigit():
        flash("sang은 필수. su,dan은 숫자만 허용")
        return redirect(url_for("add_form")) #위쪽 def add form 을 호출하고 64줄 실행-> 에러 메세지를 들고 어디에 ?전달

    su=int(su_raw) #연산없이 추가할 경우라면 숫자화하지 않아도 됨
    dan=int(dan_raw)

    # 새 상품 추가 처리
    conn=get_conn()
    try:
        with conn.cursor() as cur:
            #code는 자동증가를 위해 프로그램으로 작성
            cur.execute("select max(code) as max_code from sangdata")
            row=cur.fetchone()
            max_Code=row["max_code"] if row else None # 맨 앞 max_Code는 변수 row["max_code"]는 쿼리로 저장된 값
            next_code =(max_Code+1) if max_Code is not None else 1

            # 추가
            cur.execute("insert into sangdata(code,sang,su,dan) values (%s,%s,%s,%s)",
                (next_code,sang,su,dan)
            )
            conn.commit()
            return redirect(url_for("show_list")) #추가하고 목록보기
        
    except Exception as e:
        conn.rollback()
        flash(f"저장실패: {e}")
        return redirect(url_for("add_form"))
    
    finally:
        conn.close()
####################################################################
######################################################################################################

# 수정단
######################################################################################################
####################################################################
@app.get("/edit/<int:code>") 
def edit_form(code:int): # 수정 폼 호출 # (code:int) 안 써도 됨. 가독성 향상
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute("select * from sangdata where code =%s",(code,)) # (code,)) : 튜플로 만들어주기
            row = cur.fetchone()
        if not row:
            flash(" 해당 자료가 없음")
            return redirect(url_for("show_list"))
        
        messages=list(get_flashed_messages())
        return render_template("form_edit.html",row=row, messages=messages)
    finally:
        conn.close()
####################################################################
      
####################################################################
@app.post("/edit/<int:code>") # 수정 저장 # 실질적으로 작동하는 것. URL에 보이는 것 
def edit_save(code:int):    # 수정 저장

    sang=(request.form.get("sang")or"").strip() # post 방식이니까 html엣 <form> 태그 써야하고
    su_raw=(request.form.get("su")or"").strip() # form 태그 썼으니까 서버에서 request.form으로 받는다
    dan_raw=(request.form.get("dan")or"").strip()
    
    # 서버에서 클라이언트가 전달한 입력자료 검사
    if not sang or not su_raw.isdigit()or not dan_raw.isdigit():
        flash("sang은 필수. su,dan은 숫자만 허용")
        return redirect(url_for("edit_form",code=code)) #edit/<int:code>" 여기서 요청해서 code=code로 넘겨줌

    su=int(su_raw)
    dan=int(dan_raw)

    # 수정하기
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute("update sangdata set sang =%s,su =%s,dan =%s where code=%s",
            (sang,su,dan,code))
        conn.commit()
        return redirect(url_for("show_list")) #추가하고 목록보기

    except Exception as e:
        conn.rollback()
        flash(f"수정 실패: {e}")
        return redirect(url_for("edit_form",code=code))
    finally:
        conn.close()
####################################################################
######################################################################################################

##################################
@app.post("/delete/<int:code>") # 실질적으로 작동하는 것. URL에 보이는 것
def delete_row(code:int): # 1.호출되는 함수. by -> <form action="{{url_for('delete_row', code=r.code)}}" method="post">
    conn=get_conn()

    try:
        with conn.cursor() as cur:
            # 삭제하기
            cur.execute("delete from sangdata where code=%s",(code,))

        conn.commit()
        return redirect(url_for("show_list"))
    
    except Exception as e:
        conn.rollback()
        flash(f"삭제 실패: {e}")
        return redirect(url_for("show_list"))
    finally:
        conn.close()

if __name__=='__main__':
    app.run(debug=True,host='0.0.0.0',port=5000);