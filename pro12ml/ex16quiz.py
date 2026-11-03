"""
데이터 로드 (Servo, UCI) : "https://archive.ics.uci.edu/ml/machine-learning-databases/servo/servo.data"

제어 시스템(servo system), 특히 서보 제어기의 응답 속도(response time) 를 예측하기 위해 수집된 고전 데이터.
당시 뉴럴 네트워크와 회귀 분석 연구에 자주 쓰임.

cols = ["motor", "screw", "pgain", "vgain", "class"]  # 모터 위치, 스크류 위치, P게인(비례 이득), V게인(속도 이득), 응답 시간(타깃)

 - 타깃/피처 (숫자만 사용: pgain, vgain)
   x = df[["pgain", "vgain"]].astype(float)   
   y = df["class"].values
 - 학습/테스트 분할 ( 8:2 )
 - 스케일링 (StandardScaler)
 - 다항 특성 (degree=2) + LinearRegression 또는 Ridge 학습
 - 성능 평가 
 - 시각화
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import koreanize_matplotlib
from sklearn.metrics import r2_score
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures # 다항회귀식

pd.set_option('display.max_columns',None) # 컬럼 양이 많아도 ...으로 표현하지 않고 다 표현하기
df=pd.read_csv("https://archive.ics.uci.edu/ml/machine-learning-databases/servo/servo.data")
df=pd.DataFrame(df)

df.columns = ["motor", "screw", "pgain", "vgain", "class"]
print(df.columns[2], df.columns[3]) #pgain vgain
x = df[["pgain", "vgain"]].astype(float)  # astype(float) : object -> float 변환 
y = df["class"].values # class가 타깃(응답시간)임. values : class라는 컬럼을 1차원 배열로 변환

print(x,'\n', y) # 2차원, 1차원 배열 확인
#      pgain  vgain
# 0      6.0    5.0
# ..     ...    ...
# y 값
# [166 rows x 2 columns] 
#  [0.5062525  0.35625148 5.500033

train_set, test_set = train_test_split(df, test_size=0.2, random_state=12,shuffle=True)

model=LinearRegression()
double=PolynomialFeatures(degree=2) # 2차 다항식 특성 생성

x_double=double.fit_transform(x)
# PolynomoailFeatures 클래스를 바탕으로 만들어진 douvle 객체의 fit_transform() 메서드를 사용하여 x 데이터를 변환하면, 원래의 특성에 대한 2차 다항식 특성이 추가된 새로운 배열이 생성됨.
print(x_double[:3]) # 2차 다항식 특성 확인

# 다항회귀
model.fit(x_double,y) # fit(): 평균, 분산, 회귀계수 등 학습. x_double에 대한 y값을 학습시킴. 2차 다항식 특성으로 학습
y_pred=model.predict(x_double) # predict(): 예측. 학습된 모델을 바탕으로 x_double에 대한 y값을 예측
# 같은 기능 다른방식
# y_pred2=model.predict(double.fit_transform(x)) # fit_transform()으로 x를 변환한 후 predict()로 예측
print('y_pred : ',y_pred[:3]) # 예측값 확인
r2=r2_score(y,y_pred)
print('다항회귀 결정계수 : ', r2)

# 시각화
plt.scatter(x,y, label='초기 데이터')
plt.plot(x_double,y_pred, linestyle='-',label='Quadratic fit(d=2), $R^2=%.2f$' %r2, lw=3,c='r')
plt.xlabel('P 게인, V 게인')
plt.ylabel('응답 시간')
plt.legend()
plt.show()

"""
	                            1차 (단항)	                                  2차 이상 (다항)
특성 1개 (단순)	        ① 단순 선형 회귀 y = w₁x + b                  ③ (단순) 다항 회귀y = w₁x + w₂x² + b
	
특성 2개 이상 (다중)	② 다중 선형 회귀y = w₁x₁ + w₂x₂ + b           ④ 다중 다항 회귀y = w₁x₁ + w₂x₂ + w₃x₁² + w₄x₁x₂ + w₅x₂² + b
"""


# 다른 사람 답
"""
100%
# 다항회귀분석 문제) 
# 데이터 로드 (Servo, UCI) : "https://archive.ics.uci.edu/ml/machine-learning-databases/servo/servo.data"
# 제어 시스템(servo system), 특히 서보 제어기의 응답 속도(response time) 를 예측하기 위해 수집된 고전 데이터.
# 당시 뉴럴 네트워크와 회귀 분석 연구에 자주 쓰임.
# cols = ["motor", "screw", "pgain", "vgain", "class"]  # 모터 위치, 스크류 위치, P게인(비례 이득), V게인(속도 이득), 응답 시간(타깃)
#  - 타깃/피처 (숫자만 사용: pgain, vgain)
#    x = df[["pgain", "vgain"]].astype(float)   
#    y = df["class"].values
#  - 학습/테스트 분할 ( 8:2 )
#  - 스케일링 (StandardScaler)
#  - 다항 특성 (degree=2) + LinearRegression 또는 Ridge 학습
#  - 성능 평가 
#  - 시각화

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import koreanize_matplotlib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error

# 데이터 로드
pd.set_option('display.max_columns', None)
df = pd.read_csv("https://archive.ics.uci.edu/ml/machine-learning-databases/servo/servo.data",header=None)
df.columns = ['motor', 'screw', 'pgain', 'vgain', 'class']
print(df.head(2))
#   motor screw  pgain  vgain     class
# 0     E     E      5      4  0.281251
# 1     B     D      6      5  0.506252
print(df[['pgain', 'vgain', 'class']].corr())
#           pgain     vgain     class
# pgain  1.000000  0.812268 -0.598129
# vgain  0.812268  1.000000 -0.364383
# class -0.598129 -0.364383  1.000000

# 타깃 / 피처 (숫자만 사용)
x = df[['pgain', 'vgain']].astype(float) # x : pgain, vgain 두 개의 입력 변수 (2차원)
y = df['class'].values # y : 응답 시간 값 (1차원)
print(x.head(3))
#    pgain  vgain
# 0    5.0    4.0
# 1    6.0    5.0
# 2    4.0    3.0
print(y[:3]) # [0.28125095 0.5062525  0.35625148]

# 학습 / 테스트 분할 (8:2)
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)
# 학습 데이터(x_train, y_train) 대략 80%, 테스트 데이터(x_test, y_test) 대략 20%   8 : 2

# 스케일링
scaler = StandardScaler()
x_train_scaled = scaler.fit_transform(x_train)
x_test_scaled = scaler.transform(x_test)
# x_train_scaled, x_test_scaled는 스케일링된 독립변수 데이터

# 다항 특성 (2차)
quad = PolynomialFeatures(degree=2, include_bias=False)
x_train_quad = quad.fit_transform(x_train_scaled)
x_test_quad = quad.transform(x_test_scaled)
print(quad.get_feature_names_out(['pgain', 'vgain']))
print(x_train_quad[:3]) # [[ 1.84967634 ... 1.24881136]]

# 1차 선형회귀 (피처가 두 개이므로 다중선형회귀)
model = LinearRegression()
model.fit(x_train_scaled, y_train)
y_lin_pred = model.predict(x_test_scaled)
model_r2 = r2_score(y_test, y_lin_pred)

print('\n1차 선형회귀')
print('예측값 :', y_lin_pred)                             # [2.64610672 ... 2.64610672]
print('실측값 :', y_test)                                 # [4.499986 ... 4.6999955]
print('학습 결정계수 :', model.score(x_train_scaled, y_train))   # 0.365525
print('테스트 결정계수 :', model_r2)                             # 0.511371
print('MAE :', mean_absolute_error(y_test, y_lin_pred))         # 0.933675
print('RMSE :',np.sqrt(mean_squared_error(y_test, y_lin_pred))) # 1.087191

# 다항회귀 (2차)
model_quad = LinearRegression()
model_quad.fit(x_train_quad, y_train)
y_quad_pred = model_quad.predict(x_test_quad)
q_r2 = r2_score(y_test, y_quad_pred)
print('\n2차 다항회귀')
print('예측값 :', y_quad_pred)                              # [3.44493849 ... 3.44493849]
print('실측값 :', y_test)                                   # [4.499986 ... 4.6999955]
print('학습 결정계수 :', model_quad.score(x_train_quad, y_train)) # 0.565527
print('테스트 결정계수 :', q_r2)                                  # 0.511371
print('MAE :', mean_absolute_error(y_test, y_quad_pred))         # 0.630769
print('RMSE :',np.sqrt(mean_squared_error(y_test, y_quad_pred))) # 0.860625

# 시각화
plt.scatter(y_test, y_lin_pred, label='linear fit(d=1), $R^2=%.3f$'%model_r2, lw=2, c='b')
plt.scatter(y_test, y_quad_pred, label='quad fit(d=2), $R^2=%.3f$'%q_r2, lw=2, c='r')
min_value = min(y_test.min(), y_lin_pred.min(), y_quad_pred.min())
max_value = max(y_test.max(), y_lin_pred.max(), y_quad_pred.max())
plt.plot([min_value, max_value], [min_value, max_value], linestyle='--', c='k', label='실제값 = 예측값')
plt.xlabel('실제 응답 시간')
plt.ylabel('예측 응답 시간')
plt.title('Servo 선형회귀와 다항회귀 비교')
plt.legend()
plt.show()

"""