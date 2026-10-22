"""
matplotlib: 프로팅 라이브러리. 그래ㅑ프 작성을 위한 다양한 함수 제공

데이터 시각화의 장점:

복잡한 정보의 명확한 전달
패턴, 추세, 이상값 파악
데이터 기반의 빠른 의사결정
효과적인 스토리텔링과 설득력 강화
통계적 함정 방지 (앤스컴의 사중주 등)
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
plt.rc('font', family='malgun gothic') # 한글 글꼴 지정 없으면 글자 깨짐
# 이거를 주면 음수가 깨짐
plt.rcParams['axes.unicode_minus']=False # 음수 깨짐 방지. 없으면 음수 깨짐
# 위에 두개는 같이 써야함

import koreanize_matplotlib # 이거 쓰면 한번에 한글 글꼴, 음수 다 처리할 수 있음

x=["서울", "인천", "수원"] # 그래프의 x축 값은 인덱스. 0부터 시작하지만 사용자가 지정해주는거임
y=[5,3,7] #list
y=(5,3,7) # tuple. ※ {}set은 불가능
plt.xlabel('지역명')
plt.ylabel('투자액')

plt.xlim([-1,3])
plt.ylim([0,10])

plt.yticks(list(range(0,11,3))) # y축의 라벨을 인위적으로 변경. 이거 없으면 기본값 지정된 걸로 출력

plt.plot(x,y)
plt.show()

data=np.arange(1,11,2)
plt.plot(data) # x축의 구간은 자동 설정
x=[0,1,2,3,4]
for a,b in zip(x,data):
    plt.text(x=a,y=b,s=str(b))
plt.show()

x=np.arange(10)
y=np.sin(x)
# print(x,y)
# plt.plot(x,y)
# plt.plot(x,y,'bo') #color,marker 표시
plt.plot(x,y,'ro--',linewidth=2,markersize=12) # bo는 파란점, go는 녹색점, ro는 빨간점
plt.show()

# hold: 복수의 plot으로 여러 개의 차트를 겹쳐 그림
x=np.arange(0,np.pi*3,0.1)
print(x)
y_cos=np.cos(x)
y_sin=np.sin(x)
plt.figure(figsize=(10,5)) # 그래프 전체 크기 지정(w,h)
plt.plot(x,y_sin,'r') # 선
plt.scatter(x,y_cos) # 산점도
plt.legend(['사인','코싸인']) # 범례
plt.show()

print()
# subplot: 하나의 figure를 여러개의 axes(plot)으로 나누기
plt.subplot(2,1,1) # 1행
plt.plot(x,y_sin)
plt.title('sin')
plt.subplot(2,1,2) # 2행
plt.plot(x,y_cos)
plt.title('cosin')
plt.show()

print()
irum=['a','b','c','d','e']
kor=[80,90,74,81,47]
eng=[88,62,24,73,89]
plt.plot(irum,kor,'ro-')
plt.plot(irum,eng,'bo--')
plt.ylim([20,100])
plt.title('시험 점수')
plt.legend(['국어','영어'],loc=4)
plt.grid(True)

# 그래프를 이미지 파일로 저장
fig=plt.gcf()
plt.show()
fig.savefig('mplot1.png')

# 이미지 읽기
from matplotlib.pyplot import imread
img=imread('mplot1.png')
plt.imshow(img)
# plt.imshow('mplot1.png') # 얘도 가능
plt.show()