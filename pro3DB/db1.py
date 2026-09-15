# SQLlite: 개인용 DB, pyton에 기본으로 내장 되어 있음
import sqlite3

print(sqlite3.sqlite_version)
print()

conn = sqlite3.connect('exam.db') # exam.db 파일이 없으면 새로 생성, 있으면 연결. 파일에 데이터 보관
conn = sqlite3.connect(':memory:') # RAM에 DB 생성, 프로그램 종료시 사라짐. RAM에 DB를 올려서 사용하고 싶을 때 사용

try:
    cur = conn.cursor() # DB에 SQL문을 실행할 수 있는 커서 객체 생성

    # 테이블 생성 
    cur.execute("create table if not exists friends(name text, phone text, addr text)")
    # 테이블이 없으면 생성, 있으면 무시)

    # 데이터 삽입
    #방법1
    cur.execute("insert into friends values ('홍길동', '111-1111', '서초1동')")

    #방법2
    cur.execute("insert into friends values(?,?,?)",('이기자','111-2222','서초2동'))
    #모르는 값은 ?로 처리하고, 튜플로 전달 -> 튜플 말고 다른 방식도 가능
    
    #방법3
    inputdats = ('신묘한','111-1234','서초3동')
    cur.execute("insert into friends values(?,?,?)", inputdats)

    #방법4
    inputdatas2 = (('기묘한','111-3333','역삼1동'),('미묘한','111-4444','역삼2동'))
    cur.executemany("insert into friends values(?,?,?)", inputdatas2)
    # 여러명을 동시에 받을 때는 executemany()를 사용

    conn.commit() # DB에 실제로 반영, commit()을 하지 않으면 DB에 반영되지 않음

    # 자료보기
    cur.execute("select * from friends")
    print(cur.fetchone()) # 한개의 행 (레코드))읽기. redcord pointer가 다음 레코드로 이동
    # fetchone()은 한 행만 가져오기 때문에, 여러 행을 가져오려면 반복문을 사용해야 함
    # pointer가 다음 레코드로 이동하기 때문에, fetchone()을 반복해서 호출하면 다음 레코드를 가져올 수 있음
    # 순차적으로 읽는 것이지 한번에 다 읽는 것이 아님.
    # 여러 레코드를 가져오려면 fetchall()을 사용
    print()
    print(cur.fetchall())
    print()
    cur.execute("select name,phone,addr from friends")
    for r in cur:
        print(r)

    print()
    cur.execute("select name,addr,phone from friends")
    for r in cur:
        #print(r)
        print(r[0],r[1],r[2]) # 튜플로 가져오기 때문에 인덱스로 접근 가능

except Exception as e:
    print("error : ", e)
finally:
    conn.close() # DB 연결 종료 . 에러가 있던 없던 무조건 최종적으로 실행됨