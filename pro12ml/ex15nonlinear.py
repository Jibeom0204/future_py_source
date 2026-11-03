"""
비선형 회귀 분석(Non-Linear Regression)
직선의 회귀선을 곡선으로 변환해 더 정확하게 데이터 변화를 예측 가능
선형 가정이 어긋날 때(비 정규성) 대처할 수 있는 방법이다. 다항식 항을 추가해 다항회귀 모델을 작성
"""
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import r2_score

x=np.array([1,2,3,4,5])
y=np.array([4,2,1,3,7])

print("상관관계 출력", np.corrcoef(x,y)[0,1]) # 0.4807619

plt.scatter(x,y)
plt.show()

# 선형회귀 모델을 적용
from sklearn.linear_model import LinearRegression
x=x[:,np.newaxis] # sklearn의 모든 것은 2차원으로 값을 넣어야함. 1차원이면 차원확대 해줘야함 
print(x)

model=LinearRegression().fit(x,y) #?
ypred=model.predict(x) # 예측모델
print('예측값 y: ', ypred)
print('결정예수: ', r2_score(y,ypred))

plt.scatter(x,y)
plt.plot(x,ypred,c='red')
plt.show()

# 비선형 모델 작성
# 여러 방법 중 가장 일반적인 방법을 사용 (PolynomialFeatures, log 변환, curve_fit()....)
from sklearn. preprocessing import PolynomialFeatures # 다항식 특징(변수)를 추가하는 기능.
# 기존 데이터의 특성(Feature)들을 제곱, 세제곱하거나 서로 곱해서 새로운 다항식 특성들을 만들어내는 전처리(Preprocessing) 도구
poly=PolynomialFeatures(degree=2, include_bias=False) # degree=열의 개수. include_bias= 출력할 때 고정된 상수값 출력할지 여부

# 선형 회귀 모델은 기본적으로 $y = w_1 x + b$ 와 같은 직선 형태만 학습할 수 있습니다.
# 하지만 실제 데이터는 아래 그림처럼 단순 직선이 아니라 곡선(U자 형태, S자 형태 등) 형태로 분포하는 경우가 많습니다.
# PolynomialFeatures를 사용해 $x^2, x^3$ 등의 특성을 만들어 입력하면,
# 선형 모델의 식 자체는 그대로 유지하면서도 실제 예측 결과는 곡선 형태로 데이터에 맞춰지는 효과를 얻을 수 있습니다.


x2=poly.fit_transform(x)  # x(원본데이터)값의 제곱. degree가 3이면 제곱, 세제곱 값들도 출력
print('x값 출력',x) 
print('x2값 출력',x2) # x의 값이 제곱된 값이 출력됨

# fit(): 데이터의 통계값(예: 평균, 표준편차, 최댓값/최솟값 등)을 계산하여 저장
# transeform(): fit()에서 계산된 통계값을 바탕으로 데이터를 실제 변환(스케일링, 정규화

model2=LinearRegression().fit(x2,y) # 추가된 특징 행렬값으로 모델 생성
ypred2=model2.predict(x2)
print('예측값 y: ',ypred2) #[4.1428 1.6285 1.257 3.0285 6.9428]
print('결정계수: ',r2_score(y,ypred2)) #0.98921. 이미 오버피팅.
# degree가 올라가면 성능은 올라가는데 과적합에 유의해야 한다.

plt.scatter(x,y)
plt.plot(x, ypred2, c='red')
plt.show()