# a= {1,2,3,4,5,5,5,5,5,5}
# b= (1,2,3,4,5,5,5,5,5,5)
# c= [1,2,3,4,5,5,5,5,5,5]
# for i in a,b,c:
#     print(i, end = ' ')
#     print()

# print('분산/표준편차')
# numbers = [1,3,5,7,9] #합은 25, 평균은 5.0
# # numbers = [3,4,5,6,7] #합은 25, 평균은 5.0
# # numbers = [-3,4,5,7,12] #합은 25, 평균은 5.0
# for a in numbers:
#     tot = 0
#     tot += a

#     print(f"합은 {tot},평균은 {tot/len(numbers)}")
#     avg =tot/len(numbers)

#     #편차제곱의  합
#     hap =0
#     for i in numbers:
#         hap+=(i-avg)**2

#     print(f"편차제곱의 합 : {hap}")
#     vari = hap /len(numbers)
#     print(f"분산 : {vari}")
#     print(f"표준편차 : {vari**0.5}")
#     print()

# colors = ['빨강', '초록', '파랑']

# # 1. 원본 리스트 기본 출력
# for v in colors:
#     print(v, end=' ')
# print()

# # 2. 이터레이터 객체 생성
# print('iter(): 반복 가능한 객체를 하나씩 꺼낼 수 있는 상태로 만들어 주는 함수')
# iterator = iter(colors)

# # [첫 번째 실행] 데이터를 모두 소모하며 정상 출력
# print('1번째 실행 결과:')
# for v in iterator:
#     print(v, end=' ')
# print()

# # [두 번째 실행] 이미 소모되었으므로 아무것도 출력되지 않음 (빈 값)
# print('2번째 실행 결과:')
# for v in iterator:
#     print(v, end=' ')
# print()


# print()
# for idx, d in enumerate(colors, start=5): #enumerate() : 반복 가능한 객체를 인덱스와 함께 꺼낼 수 있는 상태로 만들어 주는 함수
#         print(idx, d, end = ' ') #인덱스와 값을 반환

#     print()

#     print('\n사전형 ---')
#     datas = {'python' : '만능언어','java':'웹용언어' , 'c':'시스템언어'}  #'python' : '만능언어' python이[0]이고 만능언어가 [1]이다
#     print(datas.items())


#     print()

#     for i in datas.items():
#         print(i[0])
#         print(i[0],'~~',i[1])
#         # print(i[0],'~~',i[1],'~~', i[2]) #없는 인덱스 접근시 에러 발생


#     print()
#     print()

#     for k,v, in datas.items():
#         print(k,'~~',v)

#     print()
#     print()
    
#     for k in datas.keys():
#         print(k,end = ' ')
#         print()

#     for k in datas.values():
#             print(k,end = ' ')
#             print()


#     print()
#     print()
#     print()
#     print()


# print('\n다중 for ====')
# for n in [2,3]:  #집합형 자체를 반복문에 넣을 수 있다.
#         print(f'{n}단~~~')
#         for su in [1,2,3,4,5,6,7,8,9]:
#             print(f'{n} * {su} = {n*su}')

#     print()
#     print()

# print('\n for문도 continue / break 사용 가능')
# nums=[1,2,3,4,5]
# for i in nums:
#     if i ==2: continue #반복문 처음으로 돌아감
#     if i ==4: break #반복문 탈출
#     print(i, end = ' ')
# else:
#         print('for문 정상 종료') #반복문이 정상적으로 종료되면 수행

# print('\n\n 정규표현식 연습 + for문 연습')
# message = """
# blah blah blah
# 존 메이어 & $%#$스티비 레이본
# Gibson 59
# 클래식 바이브는 펜더 산하의 스콰이어라는 브랜드의 대표모델이다 존메이어는 펜더 를 많이 썼다. 스티비 레이본도 펜더를 썼다
# """ #문자열로 취급한다
# import re #정규표현식을 위한 라이브러리를 메모리에서 호출하기
# message2 = re.sub(r'[^가-힣\w\s]','',message) #이거 뭐고?  선택적으로 고른다= [], 시작  ^를 [] 앞에 쓰면 -> ^[]는 시작 글자, [^]이렇게 쓰면 부정
# #패턴과 일치하는 문자열을 다른 문자열로 치환 -> 여기서는 공백으로 치환
# message3 = re.sub(r'[^가-힣\w\s]','55',message) #여기서는 하나당 55로 치환
# print(message2)
# print(message3)

# print('\n\n)')
# message4 = message2.splitlines() #문자열을 줄 단위로 나누어 리스트로 반환
# message5 = message2.split() #문자열을 공백 단위로 나누어 리스트로 반환 -> 공백기준 문자열 분리
# print(f"message4: {message4}")
# print(f"message5: {message5}")
# print(f"message5 길이: {len(message5)}")

# #단어별 빈돗 출력: dictinary 자료형을 이용하여 단어별 빈도수 출력
# cou ={}
# for i in message5:
#       if i in cou: 
#           cou[i] += 1 # cau에 이미 존재하는 단어라면 1씩 증가
#       else:
#           cou[i] =1 #최초 단어일 경우 '단어' : 1로 초기화
#           print(f"cou: {cou}")
# print(f"단어별 빈도수: {cou}")



# print('정규표현식 좀 더')
# for imsi in['111-1234', '일이삼-일이삼사', '222--2847','984-7787']:
#     if re.match(r'^\d{3}-\d{4}$', imsi):
#         #^이거 처음 나옴 %d= 0~9까지라는 의미 {3} = 3자리 숫자, - = 하이픈, \d{4} = 4자리 숫자, $ = 끝나는 글자
#         print(imsi, '전화번호 맞음')
#     else: 
#         print(imsi, '전화번호 아님')



# print('\n\n')

# print('\n comprehension: 반복문+조건문+값생성을 한줄로 표현')
# a =[1,2,3,4,5,6,7,8,9,10]
# li=[]
# for i in a:
#      if i%2 == 0: #i를 2로 나눈 후 나머지가 0이라면 해당 i를
#          li.append(i) #li 리스트에 저장
# print(f"li: {li}") #2 4 6 8 10

# print(list(i for i in a if i %2 == 0)) #2 4 6 8 10 //이게 컴프리핸션(comprehension)
# print(list(i*2 for i in a if i %2 == 0)) #짝수 2배이벤트

# print()
# datas = [1,2,3,99,'a','alpha',True,3.0]
# for i in datas:
#     if type(i) == str: #정수형만 출력   datas변수에 i 가 문자열이면 출력
#         print(i, end = ' ')

# print('위에거 변형')
# lis = [i for i in datas if type(i) == str]
# print(lis)

# id_name ={1:'tom', 2:'james', 3:'maria'}  #키->밸류 형식 
# #순서를 뒤집고 싶으면
# nam_id ={val:key for key, val in id_name.items()} #for key, val in id_name.items()} 이걸 실행해서 val:key로 바꿔서 nam_id에 넣는다
# print(id_name)
# print(nam_id) #tom:1, james:2, maria:3



# print('\n\n')
# zz =[(1,2),(3,4),(5,6)] #(5)는 튜플이 아니라 정수형이다. 튜플은 반드시 2개 이상이어야 한다. (5,) 이렇게 써야 튜플이다.
# for a,b in zz: #튜플의 요소가 2개이므로 a,b
#     print('가로출력',a,b)
    
# print()
# print([a+b for a,b in zz]) #튜플의 요소가 2개이므로 a,b [3, 7, 11]d
# # a,b=[1,2,3]
# # print(a,b)  이거는 오류남 행열개수가 안맞아서
# # *a,b = [1,2,3] # *a = 1,2  b=3 이러면 순서 바뀜
# print('세로출력',*[a+b for a,b in zz], sep='\n')




# print('\n\n')

print('수열생성: range(start, stop, step)') #range(start, stop, step) 기본형식
print(list(range(1,6))) #1 2 3 4 5
print(list(range(1,6,1))) #1로 start 6에서 stop, 1씩 증가하는 step
print(list(range(1,6,2))) #1로 start 6에서 stop, 2씩 증가하는 step
print(tuple(range(1,6,2))) #맨 앞에 형식 적어주기, 얘는 튜플, 1로 start 6에서 stop, 2씩 증가하는 step
print(set(range(1,6,2))) #맨 앞에 형식 적어주기, 얘는 셋, 1로 start 6에서 stop, 2씩 증가하는 step
print(set(range(0,6,2)))
print(set(range(0,6,1)))#초기값 안주면 1로 시작 0 1 2 3 4 5 
print(set(range(6))) #목적지만 주기 0 1 2 3 4 5 위에거랑 같은 의미
print()
print("유형별로 봐보기 리스트,튜플,셋 순서")
print(f'리스트_대괄호: ',list(range(-10,-100,-20)))
print(f'튜플_소괄호: ', tuple(range(-10,-100,-20)))
print(f'셋_중괄호: ',set(range(-10,-100,-20)))

# print('\n\n')

# for i in range(6):
#      print(i, end =",")
# print()
# for _ in range(6): #반복하는데 변수를 쓰지 않을거다 왜??? 질문하기
#     print('반복')
# print()

# print("1~10까지 정수 합")
# tot = 0
# for i in range(1,11):
#      tot +=i
#      print('tot: ',tot)
#      print('tot: ',tot, '',sum(range(1,11)))#sum내장함수->for문을 편하게 해주는 함수, 그러나 원리는 알아야함
# print()
# for i in range(1,10):
#      print(f'2 *{i}={2*i}')

# print('2~9 구구단 출력(단은 행단위 출력)')
# for i in range(2,10):
#      for j in range(1,10):
#           print(f'{i}*{j}={i*j}', end='')
#           print()

# print('\n\n')
# print('주사위 두번 던져서 합이 4의 배수가 되는 경우만 출력')
# for i in range(6):
#      n1=i+1
#      for j in range(6):
#           n2 =j+1
#           n=n1+n2
#           if n%4 ==0:
#                print(n1,n2)
#                #이거 불편함 초기값을 주자

# print()
# for i in range(1,7,1):
#      for j in range(1,7):
#           hap =i+j
#           if hap%4==0:
#                print(i,j)
