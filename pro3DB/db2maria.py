#원격 데이터 베이스와 연동 프로그래밍
#준비1) MariaDB 연동: IP(네트워크에서 컴퓨터나 장치를 구분 프로토콜(규약)) 주소 필요.
#준비2) DBMS 설치 필요. (MariaDB, MySQL, Oracle, MS-SQL 등) 연결용 Dirver 설치 필요. (MariaDB Connector/Python 설치 필요 -- pip install mariadb)

import MySQLdb

#연결 정보 매핑 방법 1
""" 
conn = MySQLdb.connect( ## 연결방법 1. 나 혼자 DB 연결할 때 쓰는 방법

    host ='localhost', # DBMS가 설치된 컴퓨터의 IP주소 or host='127.0.0.1' 혹은 ipconfig.get('host') or cmd에서 ipconfig 명령어로 확인 가능
    user='root', # DBMS 접속 계정
    password='123', # DBMS 접속 계정의 비밀번호
    database='test', # 접속할 DB명
    port=3306, # DBMS 접속 포트번호. MariaDB, MySQL은 기본 3306, Oracle은 1521, MS-SQL은 1433
    #우리가 설치한 포트번호는 3307
)
"""

# #연결 정보 매핑 방법 2. 나 혼자 DB 연결할 때 쓰는 방법
# config_data = {
#     "host": "localhost",
#     "user": "root",
#     "password": "123",
#     "database": "test",
#     "port": 3306,
#     "charset": "utf8"
# }
# # 키 밸류 형식으로 json 타입으로 저장할 수 있다.

#연결 정보 매핑 방법 3:json 파일로 저장 후 불러오기
import json
with open('dbconnect.json', mode='r',encoding='utf-8') as f:
    config_data = json.load(f) #json 파일을 읽어서 config_data에 매핑

def myFunc():
    try:
        ## 연결방법 2,3와 매핑
        conn =MySQLdb.connect(**config_data) 
        cursor = conn.cursor()
        #conn.autocommit(True) # 자동 커밋 설정.
        #conn.autocommit(False) # 자동 커밋 해제. # 수동 커밋: 기본값
        sql ="select code,sang,su,dan from sangdata" # sql문으로 sangdata 테이블의 레코드 가져오기

        # ## 자료 추가
        # isql= "insert into sangdata(code, sang, su, dan) values('6','마스크',5,10000)"
        # cursor.execute(isql) # 내 로컬에 있는 DBMS에 SQL문을 실행
        # conn.commit() # 원격 DB에 실제로 반영, commit()을 하지 않으면 DB

        # isql= "insert into sangdata values(%s,%s,%s,%s)" # sangdata 테이블에 레코드 추가
        # ins_data = (6,'커피',10,50000) # 추가할 레코드 데이터
        # #ins_data = 6,'커피',10,50000 # 위의 코드와 같음. 둘 다 튜플로 인식됨. 튜플은 () 생략 가능
        # cursor.execute(ins_data) # 내 로컬에 있는 DBMS에 SQL문을 실행
        # conn.commit() # 원격 DB에 실제로 반영, commit()을 하지 않으면 DB

        # ## 자료 수정 1
        # usql = "update sangdata set sang=%s,su=%s,dan=%s where code=%s"# code가 %s인 레코드의 sang, su, dan 값을 수정
        # up_data=('물티슈',3,1000,5) #'물티슈',3,1000,5와 같음
        # cursor.execute(usql,up_data) #usql에 up_data를 매핑하여 실행
        # conn.commit()

         ## 자료 수정 2
        # usql = "update sangdata set sang=%s,su=%s,dan=%s where code=%s"# code가 %s인 레코드의 sang, su, dan 값을 수정
        # up_data=('콜라',11,3000,6) # 6번을 콜라로 바꿈
        # # insert, update, delete는 성공하면 성공갯수, 실패하면 0을 반환
        # cou=cursor.execute(usql,up_data) #usql에 up_data를 매핑하여 실행
        # print("수정된 레코드 수: ",cou) # 수정된 레코드 수 출력
        # conn.commit()

        #자료 삭제
        code = '5';
        #dsql = "delete from sangdata where code=%"+code
        # 참고: secure codeing guide에 의해 code가 문자열이므로 + 연산자로 연결 가능. code가 숫자이면 + 연산자로 연결 불가. 이때는 str()로 형변환 필요
        # SQL 인젝션은 사용자의 입력값을 검증하지 않고 SQL문에 직접 삽입하여 공격하는 방법. 위의 코드는 SQL 인젝션 공격에 취약함.
        
        ##첫번째 삭제 방법
        #dsql = "delete from sangadta where code = '{0}'".format(code)
        ## code가 6211인 레코드 삭제. format()으로 문자열 포맷팅
        
        #두번째 삭제 방법 # ★권장방법
        dsql = "delete from sangdata where code=%s" # code가 %s인 레코드 삭제
        cursor.execute(dsql,code) #dsql에 code를 매핑하여 실행. 튜플로 전달해야 함. (code,)로 전달해야 함. (code)로 전달하면 튜플이 아님. (code,)로 전달해야 함.
        cou=cursor.execute(dsql,(code,)) # 삭제 후 반환값 얻기. (code,)로 전달해야 함. (code)로 전달하면 튜플이 아님. (code,)로 전달해야 함.
        if cou !=0: 
            print("삭제 성공")
        else:
            print("삭제 실패")

        conn.commit()


        # 자료 읽기
        #sql="select * from sangdata"
        cursor.execute(sql) # 내 로컬에 있는 DBMS에 SQL문을 실행
        for data in cursor.fetchall(): # fetchall()은 모든 레코드를 가져옴. 레코드가 많으면 메모리 부족으로 에러 발생 가능
            #print(data)
            print("읽기 방법 1")
            print("%s %s %s %s"%data)
        print()   

        # 읽기 방법 2
        print("읽기 방법 2")
        cursor.execute(sql)
        for data in cursor:
            print(data[0],data[1],data[2],data[3]) # 튜플로 가져오기 때문에 인덱스로 접근 가능
        print()

        # 읽기 방법 3
        print("읽기 방법 3")
        cursor.execute(sql)
        for code,sang,su,dan in cursor:
            print(code,sang,su,dan)
        print()

        # 읽기 방법 4
        print("읽기 방법 4")
        cursor.execute(sql)
        for a,b,수량,단가 in cursor:
            print(a,b,수량,단가)
        print()



    except Exception as e:
        print("error : ", e)

  
    finally:
        conn.close() # DB 연결 종료 . 에러가 있던 없던 무조건 최종적으로 실행됨


if __name__ == '__main__':
    myFunc()