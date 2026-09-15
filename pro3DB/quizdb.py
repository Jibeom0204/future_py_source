"""문1) 직원번호와 직원명을 입력(로그인)하여 성공하면 아래의 내용 출력

직원번호 입력 : _______
직원명 입력 : _______
직원번호 직원명 부서명 부서전화 직급 성별
    1         홍길동 총무부 111-1111 이사 남           <== 홍길동으로 로그인한 경우

    
문1-1) 직원번호와 직원명을 입력(로그인)하여 성공하면 아래의 내용 출력
해당 직원이 근무하는 부서 내의 직원 전부를 직급별 오름차순우로 출력. 직급이 같으면 이름별 오름차순한다.

직원번호 입력 : _______
직원명 입력 : _______
직원번호 직원명 부서명 부서전화 직급 성별
1 홍길동 총무부 111-1111 이사 남
...
직원 수 :

이어서 로그인한 해당 직원이 관리하는 고객 자료도 출력한다.
고객번호 고객명 고객전화 나이
1 사오정 555-5555 34
관리 고객 수 :
"""

import MySQLdb
import json

from dotenv import load_dotenv
import os #pip install python-dotenv
load_dotenv()
config= {
    'host': os.getenv('DB_HOST'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_NAME'),
    'port': int(os.getenv('DB_PORT')),
    'charset': os.getenv('DB_CHARSET')
}


def emp():
    dbconnect = None
    try:
        dbconnect = MySQLdb.connect(**config) #dbconnect라는 변수에 config라는 환경변수 값을 읽어와 담아둔 파이썬 딕셔너리를
        #**로 config내에 작성된 접속 정보를 언패킹하여 connect 함수의 인자로 전달. 그 결과를 dbconnect변수에 저장하여 Mysql과 연동
        
  
        SQLobj=dbconnect.cursor() # dbconnect에 저장된 변수를 db에 sql을 호출할 수 있는 제어권을 가진 cursor 객체를 만들고 SQLobj에 할당
        
        jikwon_no=input("직원번호: ")
        jikwon_name=input("직원이름: ")
        if jikwon_name==''or jikwon_no=='':
             print("정보를 입력하시오")
             return

        
        #mariaSQL이란 변수에 담긴 쿼리문
        #1
        jikwonSQL= """
                select j.jikwonno as 직원번호, j.jikwonname as 직원이름, b.busername 부서명, b.busertel 부서전화,
                j.jikwonjik 직급, j.jikwongen 성별
                from jikwon j
                left outer join buser b on j.busernum=b.buserno
                where jikwonno=%s and jikwonname=%s #직원의 번호와 이름이 입력한것과 같고 그것이 DB에 있는 조건
                """
        # 1-1
        buserSQL="""select * from jikwon where busernum = (
        select busernum
        from jikwon j
        inner join buser b on j.busernum=b.buserno
        where jikwonno=%s and jikwonname=%s)
        ORDER BY jikwonjik desc, jikwonname desc; #직원의 번호와 이름이 입력한것과 같고 그것이 DB에 있는 조건
            """

        gogekSQL="""
        select * from gogek
        inner join jikwon on jikwonno=gogekdamsano
        where jikwonno=%s and jikwonname=%s
        """
        #sql을 실행할 수 있는 함수
        SQLobj.execute(jikwonSQL,(jikwon_no,jikwon_name))
        #커서 객체(SQLobj)의 execute 기본 내장 메서드를 호출하여, 첫 번째 인자인 SQL 쿼리문(mariaSQL)과
        # 두 번째 인자인 데이터 값((jikwon_no, jikwon_name) 튜플)을 데이터베이스 시스템으로 전달하고 실행을 요청한다."

        #로그인 성공 직원 정보
        data = SQLobj.fetchone() #실행된 쿼리의 결과 집합에서 첫 번째 레코드(행) 1개만을 튜플 형태로 인출하여 data 변수에 할당한다. 
        # (조회된 결과가 없다면 None을 반환한다.)". SQLobj는 커서 객체이다. 이것은 SQL 쿼리가 실행된 결과의 현재 읽기 위치를 가르키는 포인터이다.
        if data:
            print("로그인 성공")
            print("직원번호: ",data[0])
            print("직원이름: ",data[1])
            print("부서이름: ",data[2])
            print("부서전화: ",data[3])
            print("직원직급: ",data[4])
            print("직원성별: ",data[5])
        else:
            print("로그인 실패: 입력자료 확인")
        print()

        SQLobj.execute(buserSQL,(jikwon_no,jikwon_name))
        data = SQLobj.fetchall() 
        if data: 
            print("부서 로그인 성공")
            print("직원번호" "직원명" "부서명" "부서전화" " 직급" "성별")
            for row in data:
                print(f"{row[0]},{row[1]},{row[2]},{row[3]},{row[4]},{row[5]}")
        else:
            print("부서 실패")
            return
        print()

        SQLobj.execute(gogekSQL,(jikwon_no,jikwon_name))
        data = SQLobj.fetchall() 
        if data: 
            print("고객 로그인 성공")
            print("고객번호" "고객명" "고객전화" "고객주민" "담당사원")
            for row in data:
                print(f"{row[0]},{row[1]},{row[2]},{row[3]},{row[4]}")
        else:
            print("고객 실패")
            return
        print()


             
    except Exception as e:
            print('에러: ',e) 
    finally:
        if dbconnect:
            dbconnect.close()

if __name__=="__main__":
     emp()





            # emp_info = data[6] #data로 넘어오는 값들 저장

            # #1.1 쿼리
            # #해당 직원이 근무하는 부서 내의 직원 전부를 직급별 오름차순우로 출력. 직급이 같으면 이름별 오름차순한다.
            # #이어서 로그인한 해당 직원이 관리하는 고객 자료도 출력한다.

            # mariaSQL2="""
            # select * from jikwon where busernum = (
            # select busernum
            # from jikwon j
            # inner join buser b on j.busernum=b.buserno
            # where busernum=%s)
            # ORDER BY jikwonjik desc, jikwonname desc; #직원의 번호와 이름이 입력한것과 같고 그것이 DB에 있는 조건
            # """
            # SQLobj.execute(mariaSQL,(emp_info))
            # data2 = SQLobj.fetchall() #여러명 있을 수 있으니 fetchall

            # for row in data2:
            #     print(f"{row[0]},{row[1]},{row[2]},{row[3]},{row[4]},{row[5]},{row[6]}")
            # print(f"관리 고객 수 : {len(data2)}")

            # mariaSQL3 = """
            # SELECT gogekno, gogekname, gogektel, gogeknai
            #     FROM gogek
            #     WHERE gogekdamsano = %s
            # """
            # SQLobj.execute(mariaSQL3,(jikwon_no,jikwon_name))
            # data3 = SQLobj.fetchall()
            # for a in data3:
            #     print(f"{row[0]},{row[1]},{row[2]},{row[3]},{row[4]},{row[5]}")
            # print(f"관리 고객 수 : {len(data3)}")
                