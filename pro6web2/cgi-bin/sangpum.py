# cgi-bin/sangpum.py : 웹용 파이썬 - Maria DB에 
import sys
sys.stdout.reconfigure(encoding='utf-8')  # 한글 깨짐 방지

import MySQLdb
from dotenv import load_dotenv
import os

load_dotenv() #env 파일은 sangpum.py와 같은 폴더 위치에 있어야 함
config= {
    'host': os.getenv('DB_HOST'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_NAME'),
    'port': int(os.getenv('DB_PORT')),
    'charset': os.getenv('DB_CHARSET')
}

# print("Contet-Type:text/html; charset=utf-8") # 얘는 꼭 라인스킵하고 띄어쓰기 조심
# print() #무조건 라인스킵
# print("<html>")
# print("<body>")
# print("<h2>*상품정보*</h2>")
# print("<table border='1'>")
# print("<tr><td>코드</td><td>품명</td><td>수량</td><td>단가</td></tr>")

# print("</table>")
# print("</body>")
# print("</html>")

print("""
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <title>상품정보</title>
</head>
<body>
    <h2>*상품정보*</h2>
""")

conn =None
try:
    conn = MySQLdb.connect(**config) # 클래스로 내부 메서드로 config 내용 dict로 받기
    cursor=conn.cursor() #읽을 수 있는 객체 생성함
    cursor.execute("""
    select code,sang,su,dan from sangdata
    """) ##  SQL 받을 코드 준비하고 SQL 쿼리 작성

    datas =cursor.fetchall() # cursor 객체에 저장(저장은 아니라고 햇는데)된 데이터 
    #한 줄씩 읽어오기

    print("<table border='1'>")
    print("<tr><td>코드</td><td>품명</td><td>수량</td><td>단가</td></tr>")

    for s_data in datas:
        print("<tr>")
        print(f"<td>{s_data[0]}</td>")
        print(f"<td>{s_data[1]}</td>")
        print(f"<td>{s_data[2]}</td>")
        print(f"<td>{s_data[3]}</td>")
        #print(f"<td>{s_data[4]}</td>")
        #print(f"<td>{datas[5]}</td>")# 테이블 튜플에 맞지 않는 추가적인 값이 들어오면 에러남
        print("</tr>")


except Exception as e:
    print('잉 에러 남 ㅋㅋ',e)
finally:
    if conn:
        conn.close()


print("""
</body>
</html>"""
)