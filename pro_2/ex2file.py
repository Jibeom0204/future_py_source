print('파일 처리: 입출력')

import os #운영체제(os)와 관련된 기능제공

try:
    print('파일 읽기 ===== ')
    print(os.getcwd()) #getcwd() current working directory
    #C:\works\projects

    #읽을 파일 =>C:\works\projects
    # f1=open(os.getcwd()+r'\pro2\ftest.txt', mode='r', encoding='utf-8')

    f1 = open(r'ftest.txt',mode='r', encoding='utf-8')
    print(f1)
    print(f1.read())
    f1.close()

    print('===파일 저장===')
    f2 =open('ftest2.txt',mode='w', encoding='utf-8')
    f2.write("ㅎㅇㅎㅇ")
    f2.wirte('졸린데')
    f2.close()
    print('파일저장성공')

    print('===파일 내용 수정===')
    f3 =open('ftest2.txt',mode='a', encoding='utf-8')
    f3.write("이거 왜 안되는거지")
    f3.wirte('꺄오')
    f3.close()
    print('파일 추가 성공')

    #ftest2읽기
    f4 = f3 =open('ftest2.txt',mode='r', encoding='utf-8')
    print(f4.read())
    f4.close()

except Exception as e:
    print('처리 오류: ', e)