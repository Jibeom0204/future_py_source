# MariaDB에서 직원, 부서 테이블 활용
# 직원번호, 이름을 입력하여 로그인에 성공하면 해당 직원 부서 정보 출력
import MySQLdb
import json

# # DB 연결정보 읽기 3: json 파일 읽기
# with open('dbconnect.json', mode='r',encoding='utf-8') as f:
# # config_data = json.load(f) #json 파일을 읽어서 config_data에 매핑

# DB 연결 정보 읽기 4: .env 파일 읽기
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



def loginfnc():
    conn = None
    try:
        conn = MySQLdb.connect(**config)
        cursor = conn.cursor() ## 맨 앞 cursor는 객체의 이름임. 다른 이름 써도 됨
        jikwon_no = input("직원번호: ")
        jikwon_name = input("직원이름: ")
        if jikwon_no == "" or jikwon_name =="": # NULL로 쓰면 안되나
            print("로그인 정보를 입력하시오")
            return
        
        # sql = '''
        # select jikwonno as 직원번호, jikwonname as 직원명,
        # buserloc as 근무지역, jikwonjik as 직급, jikwongen as 성별
        # from jikwon
        # left outer join buser on jikwon.busernum=buser.buserno
        # where jikwonno={0} and jikwonname={1}
        # """.format(jikwon_no,jikwon_name)
        # '''#sql 짜기


        #권장방법
        sql = """
                select
                j.jikwonno as 직원번호, j.jikwonname as 직원명,
                b.busername as 부서이름, j.jikwonjik as 직급, j.jikwongen as 성별
                from jikwon j
                left outer join buser b on j.busernum=b.buserno
                where jikwonno=%s and jikwonname=%s
                """
                #sql 짜기
        #sql 실행
        cursor.execute(sql,(jikwon_no,jikwon_name))
        #로그인 성공 직원 정보
        data = cursor.fetchone()

        if data:
            print("로그인 성공")
            print("직원번호: ",data[0])
            print("직원이름: ",data[1])
            print("부서이름: ",data[2])
            print("직원직급: ",data[3])
            print("직원성별: ",data[4])
        else:
            print("로그인 실패: 입력자료 확인")

    except Exception as e:
        print('에러: ',e) 
    finally:
        if conn:
            conn.close()

if __name__ == '__main__':
    loginfnc()


