"""
전통적 방법의 선형회귀(기계학습 중 지도학습)
각 데이터에 대한 잔차제곱합이 최소가 되는 추세선(회귀선)을 만들고
이를 통해 독립변수가 종속변수에 얼마나 영향을 주는지 인고관계를 분석.
독립변수 : 연속형. 종속변수 : 연속형 -> 두 변수는 상관관계 및 인과관계가 있어야함
정량적인 모들을 생성
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import koreanize_matplotlib

import statsmodels.api as sm
from sklearn.datasets import make_regression

np.random.seed(1)

x,y,_=make_regression(n_samples=50, n_features=1,bias=50,coef=True, noise=50)
# n_samples	50	데이터 개수(행 수). 점 50개 생성
# n_features	1	입력 변수 개수(열 수). 1이면 x가 하나뿐인 단순회귀
# bias	50	절편. x=0일 때 y값이 50
# coef	True	데이터를 만들 때 사용한 실제 기울기도 함께 반환하라는 옵션

# x	(50, 1)	2차원 배열. 행 50개 × 열 1개. sklearn 모델은 입력을 항상 2차원으로 받기 때문
# y	(50,)	1차원 배열. 정답값 50개
# _	(1,)	실제 기울기. coef=True일 때만 3번째로 반환됨

# _의 의미: 파이썬 관례상 "받기는 하지만 쓰지 않을 값"을 담는 변수 이름입니다. 문법적으로는 일반 변수와 같으며, 이름으로 의도를 표시하는 것입니다.
print(x)#[-0.6871727 ]]
print(y)# -32.04272194] 서로 맨 마지막 것. x일때 y값

# 싸이킷런은 보통 x가 2차원 배열임
r=np.corrcoef(x.ravel(),y)[0,1] # 상관계수 구하려면 서로 차원이 같아야 하기에 2차원 배열인 x의 차원을 낮춤
print(f'상관계수:{r:.4f}') # 매우 강한 양의 상관관계


print('\n==========모델 작성 방법1:  LinearRegression 사용하여 모델 생성==========')
from sklearn.linear_model import LinearRegression # 파이썬 제공 모듈
model=LinearRegression()
fit_model= model.fit(x,y) # 내부에서 아래와 같은 작업을 진행
# 1) 독립변수(x)와 종속변수(y)를 입력 받음
# 2) 예측값과 실제값 사이의 오차제곱합이 최소가 되도록 계산
# 3) 최적의 회귀계수(기울기, 절편)를 구함
# 4) 계산된 계수를 모델에 저장
# 단순 선형회귀 모델에서는 y=mx+b와 같은 단순한 형태의 수식을 가진 모델이 만들어진다.
# 참고: LinerRegression은 신경망처럼 반복학습을 통해 가중치를 갱신하는 것이 아니라 연산을 통해 작성됨

print("기울기(가중치,weight,slope): ",fit_model.coef_) # [79.52463976]
print("절편(편향,bias): ",fit_model.intercept_) # 60.922212
# yhat=79.52463976+60.922212 일차 방정식 완성

# 예측값 확인
y_newpred1=fit_model.predict(x[[0]]) # 위에서 얻은 기존 데이터의 0번째 값을 새로운 입력값으로 줌
print("예측값1: ",y_newpred1) #[41.09112298]
y_newpred2=fit_model.predict(np.array([[0.12345],[0.3],[0.5]]))
print("예측값2: ",y_newpred2) #[ 70.73952904  84.77960419 100.68453214]