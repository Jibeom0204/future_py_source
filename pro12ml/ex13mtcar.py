#LinearRegression 사용: mtcars dataset으로 모델 생성 후 평가
from sklearn.linear_model import LinearRegression

import statsmodels.api
from sklearn.metrics import r2_score, mean_squared_error

import numpy as np
import matplotlib.pyplot as plt

mtcars=statsmodels.api.datasets.get_rdataset('mtcars').data
print(mtcars.head(3))
print('상관계수 : \n',mtcars.corr(method='pearson'))
print()

# hp가 mpg에 영향을 주는 인과관계가 있다고 가정하고 모델 생성추진
x=mtcars[['hp']].values
print(x[:5])
y=mtcars['mpg'].values
print(y[:5])
lmodel=LinearRegression().fit(X=x,y=y)
print('slope: ',lmodel.coef_)
print('intercept: ',lmodel.intercept_)

plt.scatter(x,y)
plt.plot(x, lmodel.coef_*x + lmodel.intercept_, c='r')
# plt.plot(x,lmodel.predict(y), c='r') # 상동
plt.show()

# mpg 예측
pred=lmodel.predict(x) # x에 대한 값 예측
print("예측값: ",np.round(pred[:5],1))
print("실체값: ",y[:5])
# 예측값:  [22.6 22.6 23.8 22.6 18.2]
# 실체값:  [21.  21.  22.8 21.4 18.7]

# 모델 성능 지표
# MSE(평균 제곱 오차): 모델 내부 비교, 계산 편리(단위가 제곱된 값)
# RMSE(MSE 제곱근): 보고/해석용, 해석이 편리(원래 단위값 사용)
print('MSE : ', mean_squared_error(y,pred)) #13.989822298268805
print('RMSE : ',np.sqrt(mean_squared_error(y,pred))) #3.7402970868994894
print("r2_score 결정계수, 설명력 : ",r2_score(y,pred)) # y는 실체값 pred는 예측값. # 0.602437341423934
# 모델 평가 시 r2_score 하나만 보고 모델 판단 x (이상치에 민감, 변수가 많으면 설명력이 좋아짐)
# 모델 평가는 r2_score, RMSE 등과 함께 적어준다

# 모델 저장 및 읽기는 이전 실습 ex11과 동일

print('\n==========새로운 hp로 mpg예측==========\n')
new_hp=[[100],[110],[120]]
new_pred = lmodel.predict(new_hp)
print('예측 결과: ', np.round(new_pred.ravel(),2)) # 예측 결과:  [23.28 22.59 21.91]
# 기존 자료값
# 예측값:  [22.6 22.6 23.8 22.6 18.2]
# 실체값:  [21.  21.  22.8 21.4 18.7]