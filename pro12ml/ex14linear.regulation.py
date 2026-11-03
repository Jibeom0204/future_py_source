# 과적합
"""
선형회귀 모델이 훈련데이터에 너무 과하게 학스뵈어
데이터에 포함된 노이즈나 지엽적인 특성까지 암기해버리는 현상

훈련 데이터에 대한 예측 오차는 매우 낮ㅈ지만 처음 보는 테스트 데이터나
새로운 데이터가 들어왔을 때 예측 성능이 크게 떨어짐

Linear Regressioon에서 과적합을 해결하는 방법
특성(Feature)줄이기, 정규화(Regularization) 적용, Train/Test 9split더 많은 데이터 수집하기

이 중에서 정규화 적용하기 진행
회귀계수 값이 너무 커지지 않도록 비용함수에 페널티를 부과(규제)
Ridge(L2)규제: 가중치들의 제곱합을 최소화 하여 계수들을 0에 가깝게 작게 만든다.
Lasso(L1)규제: 가중치들의 절대값 합을 최소화 하며, 중요하지 않은 특성의 계수를 아예 0으로
ElasticNet(Ridge+Lasso)

"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import koreanize_matplotlib
from sklearn.datasets import load_iris
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression,Ridge,Lasso,ElasticNet

iris=load_iris()
print("iris 원본\n",iris.keys(),'\n') #(['data', 'target', 'frame', 'target_names', 'DESCR', 'feature_names', 'filename', 'data_module'])

pd.set_option('display.max_columns',None)

iris_df=pd.DataFrame(iris.data, columns=iris.feature_names)

iris_df['target']=iris.target
iris_df['target_names']=iris.target_names[iris.target]
print("수정된 iris\n",iris_df.head(3),'\n')
# (['data', 'target', 'frame', 'target_names', 'DESCR', 'feature_names', 'filename', 'data_module'])
# sepal length (cm)  sepal width (cm)  petal length (cm)  petal width (cm)  \
# 0                5.1               3.5                1.4               0.2   
# 1                4.9               3.0                1.4               0.2   
# 2                4.7               3.2                1.3               0.2   

#    target target_names  
# 0       0       setosa  
# 1       0       setosa  
# 2       0       setosa  

print(iris_df.shape,'\n\n')

# train(학습) test(검증)로 분리. 7:3 비율
train_set, test_set = train_test_split(iris_df, test_size=0.3, random_state=12,shuffle=True)
# 위에서 df로 만든 iris 데이테의 3할을 검증 데이터로 분리
# suffle => 기본값은 Ture. 이건 명시해 주는 거고 데이터를 섞어서 7:3으로 구분
print("데이터 나눈거 보기\n",train_set.shape, test_set.shape,'\n')
print("학습 데이터 나눈거 보기\n",train_set.head(3),'\n')
print("테스트 데이터 나눈거 보기\n",test_set.head(3),'\n')


print("독립변수\n",test_set.iloc[:,[2]],'\n') #petal length (cm). 독립변수. 원인으로 씀
print("종속변수\n",test_set.iloc[:,[3]],'\n') #petal width (cm). 종속변수. 결과로 씀

# 회귀 분석 방법 1: LinearRegression

# 학습은 train dataset 사용
model_linear=LinearRegression().fit(X=train_set.iloc[:,[2]], y=train_set.iloc[:,[3]])
print("slope: ",model_linear.coef_)
print("bias: ",model_linear.intercept_)

# 모델 평가는 test dataset으로 작업
pred=model_linear.predict(test_set.iloc[:,[2]])
print('예측값 :', np.round(pred[:5].flatten(),1)) #[0.2 1.7 0.2 1.3 2.1]
print('실제값 :', test_set.iloc[:,[3]][:5].values.flatten()) #[0.3 1.9 0.2 1.3 2.3]

print(f'r2_score ,{r2_score(test_set.iloc[:,[3]], pred)}')
# 결정계수: 회귀분석 모델이 종속변수의 전체 변동 중 독립변수로 설명할 수 있는 비율을 나타내는 지표
# r2_score(실제값, 예측값)

plt.scatter(train_set.iloc[:, [2]], train_set.iloc[:,[3]],color='red') # 모든 행의 2열
plt.plot(np.array(test_set.iloc[:, [2]]), 
         model_linear.predict(test_set.iloc[:,[2]]))
plt.show()


# #####################################################
# # 과적합이 발생했다고 판단되는 경우 규제 사용
# print('\nRidge -----------')
# # 회귀분석 방법 - Ridge: alpha값을 조정(가중치 제곱합을 최소화)하여 과대/과소적합을 피한다. 다중공선성 문제 처리에 효과적.
# from sklearn.linear_model import Ridge
# model_ridge = Ridge(alpha=10).fit(X=train_set.iloc[:, [2]], y=train_set.iloc[:, [3]])

# #점수
# print(model_ridge.score(X=train_set.iloc[:, [2]], y=train_set.iloc[:, [3]]))  # 0.91880
# print(model_ridge.score(X=test_set.iloc[:, [2]], y=test_set.iloc[:, [3]]))    # 0.94101
# pred_ridge = model_ridge.predict(test_set.iloc[:, [2]])
# print('ridge predict : ', pred_ridge[:5])
# print('r2_score(결정계수):{}'.format(r2_score(test_set.iloc[:, [3]], pred_ridge)))  # 0.9410

# plt.scatter(train_set.iloc[:, [2]], train_set.iloc[:, [3]],  color='blue')
# plt.plot(np.array(test_set.iloc[:, [2]]), model_ridge.predict(test_set.iloc[:, [2]]))
# plt.show()

# print('\nLasso -----------')
# # 회귀분석 방법 - Lasso: alpha값을 조정(가중치 절대값의 합을 최소화)하여 과대/과소적합을 피한다.
# from sklearn.linear_model import Lasso
# model_lasso = Lasso(alpha=0.1).fit(X=train_set.iloc[:, [2]], y=train_set.iloc[:, [3]])

# #점수
# print(model_lasso.score(X=train_set.iloc[:, [2]], y=train_set.iloc[:, [3]])) # 0.913863
# print(model_lasso.score(X=test_set.iloc[:, [2]], y=test_set.iloc[:, [3]]))   # 0.940663
# pred_lasso = model_lasso.predict(test_set.iloc[:, [2]])
# print('lasso predict : ', pred_lasso[:5])
# print('r2_score(결정계수):{}'.format(r2_score(test_set.iloc[:, [3]], pred_lasso)))

# plt.scatter(train_set.iloc[:, [2]], train_set.iloc[:, [3]],  color='green')
# plt.plot(np.array(test_set.iloc[:, [2]]), model_lasso.predict(test_set.iloc[:, [2]]))
# plt.show()

# # 회귀분석 방법 4 - Elastic Net 회귀모형 : Ridge + Lasso의 형태로 가중치 절대값의 합(L1)과 제곱합(L2)을 동시에 제약 조건으로 가지는 모형
# print('\nElasticNet -----------')
# # 회귀분석 방법 - ElasticNet: alpha값을 조정(가중치 절대값의 합을 최소화)하여 과대/과소적합을 피한다.
# from sklearn.linear_model import ElasticNet
# model_elastic = ElasticNet(alpha=0.1).fit(X=train_set.iloc[:, [2]], y=train_set.iloc[:, [3]])

# #점수
# print(model_elastic.score(X=train_set.iloc[:, [2]], y=train_set.iloc[:, [3]])) # 0.913863
# print(model_elastic.score(X=test_set.iloc[:, [2]], y=test_set.iloc[:, [3]]))   # 0.940663
# pred_elastic = model_elastic.predict(test_set.iloc[:, [2]])
# print('ElasticNet predict : ', pred_elastic[:5])
# print('r2_score(결정계수):{}'.format(r2_score(test_set.iloc[:, [3]], pred_elastic)))

# plt.scatter(train_set.iloc[:, [2]], train_set.iloc[:, [3]],  color='cyan')
# plt.plot(np.array(test_set.iloc[:, [2]]), model_elastic.predict(test_set.iloc[:, [2]]))
# plt.show()