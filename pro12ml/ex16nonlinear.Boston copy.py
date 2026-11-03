"""
주요 변수 (Features & Target)

• CRIM: 자치시(town)별 1인당 범죄율
• ZN: 25,000 평방피트를 초과하는 주거용 토지의 비율
• INDUS: 자치시별 비소매 상업용지 넓이 비율
• CHAS: 찰스강(Charles River) 경계 인접 여부 (1: 인접, 0: 비인접)
• NOX: 일산화질소 농도 (1,000만 당 파트)
• RM: 주택당 평균 방 개수
• AGE: 1940년 이전에 건축된 자가소유 주택의 비율
• DIS: 5개의 보스턴 고용 센터까지의 가중 거리
• RAD: 고속도로 접근성 지수
• TAX: 재산세율 (10,000달러당)
• PTRATIO: 자치시별 학생-교사 비율
• B: 흑인 인구 비율을 변형한 지표 (1000(Bk - 0.63)²)
• LSTAT: 저소득층 인구의 비율(%)
• MEDV (Target): 자가소유 주택의 중앙값 가격 (단위: 1,000달러)
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import koreanize_matplotlib
from sklearn.metrics import r2_score
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures # 다항회귀식

pd.set_option('display.max_columns',None) # 컬럼 양이 많아도 ...으로 표현하지 않고 다 표현하기
df=pd.read_csv("https://raw.githubusercontent.com/pykwon/python/refs/heads/master/testdata_utf8/housing.data", header=None,sep=r'\s+')#정규표현식 쓸 때 항상 소문자 r
df.columns = ['CRIM', 'ZN', 'INDUS', 'CHAS', 'NOX', 'RM', 'AGE', 'DIS', 'RAD', 'TAX', 'PTRATIO', 'B', 'LSTAT', 'MEDV']

print(df.head(2))
print(df.corr()) # LSTAT(저소득층 인구), MEDV(주택가격) -0.737663. 저소득층의 인구가 주택가격에 영향을 주는 것이 강한 음의 상관계수를 가짐

# 선형회귀 분석 모델
x=df[['LSTAT']].values
y=df[['MEDV']].values
print('저속득자 \n',x[:3],'\n')#linearRegression 쓰려면 2차원으로 해야함. 왜? sklear이라서?
print('집값 \n',y[:3],'\n') #head()처럼 상위 3개만 보려고 씀

# 단항을 통한 단순 선형 회귀 모델
model=LinearRegression()

# 다항 특성(변수)
quad=PolynomialFeatures(degree=2)
cubic=PolynomialFeatures(degree=3)
# PolynomialFeatures: 기존 데이터의 특성(Feature)들을 제곱, 세제곱하거나 서로 곱해서 새로운 다항식 특성들을 만들어내는 전처리(Preprocessing) 도구

# 선형 회귀 모델은 기본적으로 $y = w_1 x + b$ 와 같은 직선 형태만 학습할 수 있음
# 하지만 실제 데이터는 아래 그림처럼 단순 직선이 아니라 곡선(U자 형태, S자 형태 등) 형태로 분포하는 경우가 다수.
# PolynomialFeatures를 사용해 $x^2, x^3$ 등의 특성을 만들어 입력하면,
# 선형 모델의 식 자체는 그대로 유지하면서도 실제 예측 결과는 곡선 형태로 데이터에 맞춰지는 효과를 얻음.

x_quad=quad.fit_transform(x)
x_cubic=cubic.fit_transform(x)
print(x_quad[:3])
print(x_cubic[:3])

# 단순회귀
model.fit(x,y)
x_fit=np.arange(x.min(),x.max(),1)[:,np.newaxis] # x의 최소값, 최대값을 범위로 1씩 증가하는 배열 생성. np.newaxis: 1차원 배열을 2차원으로 바꿔줌
y_lin_fit=model.predict(x_fit) # 그래프에 표시용 
#print('y_lin_fit : ',y_lin_fit)

model_r2=r2_score(y,model.predict(x))
print('단순회귀 model_r2 출력',model_r2)#0.54414


# 다항(2차)
model.fit(x_quad,y)
y_quad_fit=model.predict(quad.fit_transform(x_fit))
q_r2=r2_score(y,model.predict(x_quad))
print('다항회귀 q_r2 출력',q_r2) #0.64071
# R²결정계수: 모델이 평균값을 기준으로 얼마나 잘 설명하는지 나타내는 지표. 0~1 사이의 값. 1에 가까울수록 모델이 데이터를 잘 설명함.

# 다항(3차)
model.fit(x_cubic,y)
y_cubic_fit=model.predict(cubic.fit_transform(x_fit))
c_r2=r2_score(y,model.predict(x_cubic))
print('다항회귀 c_r2 출력',c_r2) #0.65784

# 시각화
plt.scatter(x,y, label='초기 데이터')
plt.plot(x_fit,y_lin_fit, linestyle=':',label='Linear fit(d=1), $R^2=%.2f$' %model_r2, lw=3,c='b')
plt.plot(x_fit,y_quad_fit, linestyle='-',label='Quadratic fit(d=2), $R^2=%.2f$' %q_r2, lw=3,c='r')
plt.plot(x_fit,y_cubic_fit, linestyle='--',label='Cubic fit(d=3), $R^2=%.2f$' %c_r2, lw=3,c='k')
plt.xlabel('저소득층 인구 비율')
plt.ylabel('주택가격')
plt.legend()
plt.show()