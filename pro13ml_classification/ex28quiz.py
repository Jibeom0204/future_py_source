import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import accuracy_score


data = pd.read_csv("winequality-red.csv")

print("데이터 확인:\n", data.head(3))
print("데이터 모양:", data.shape)
df_x=data[['fixed acidity', 'volatile acidity', 'citric acid', 'residual sugar', 'chlorides',
           'free sulfur dioxide','total sulfur dioxide',
           'density','pH','sulphates','alcohol']].copy() # 독립변수,x,feature
print("독립변수 행,열 개수",df_x.shape)

df_y=data['quality']
# print(df_y.head())
print("종속변수 행,열 개수",df_y.shape)

# 훈련 데이터랑 결과 데이터 쪼개기
train_x,test_x,train_y,test_y=train_test_split(df_x, df_y, test_size=0.3, random_state=12)
print("데이터들 크기\n",train_x.shape,test_x.shape,train_y.shape,test_y.shape,'\n\n')

# 모델 생성
model=RandomForestClassifier(criterion='gini',n_estimators=500,random_state=12)

# 모델 학습
model.fit(train_x,train_y) # 문제랑 정답 제공해서 학습시키기
predict=model.predict(test_x)# 학습된 모델에 검증용 x 입력시켜서 예측값 뽑기

print("모델 예측값:\n",predict[:5])
print("모델 실제값:\n",test_y[:5])
print("맞춘 개수 :",sum(predict==test_y))
print('분류 정확도: ',accuracy_score(test_y,predict),'\n')

# 교차 검증
cross_val=cross_val_score(model, df_x,df_y,cv=7)
# 위모델을, 나눠놓은 데이터를 바탕으로, 7번 검증
print("교차 검증 결과:\n ",cross_val)
print("교차 검증 평균 정확도: ", np.round(np.mean(cross_val),4),'\n')

# 특성변수
print("특성변수 확인하기: ", model.feature_importances_)
# [0.0790304  0.10023555 0.07443986 0.06965759 0.07735441 0.06864025
#  0.10273921 0.09462211 0.07196175 0.10965017 0.15166871]
# 뭐가 뭔지 알 수 없다.

# 시각화
import matplotlib.pyplot as plt
import koreanize_matplotlib
n_features=df_x.shape[1] #인덱스 [1]을 지정해 열 개수인 11만 추출하여 n_features
plt.barh(range(n_features),model.feature_importances_,align='center')
plt.xlabel('변수별 중요도 점수')
plt.ylabel('독립변수')
plt.yticks(np.arange(n_features),df_x.columns) # 그래프에 변수 이름들 표시
plt.show()
plt.close()

# 독립변수 별 중요도
# impor=data[['fixed acidity', 'volatile acidity', 'citric acid', 'residual sugar', 'chlorides',
#            'free sulfur dioxide','total sulfur dioxide',
#            'density','pH','sulphates','alcohol']].copy()

# from sklearn.preprocessing import LabelEncoder
# encoder= LabelEncoder()
# df_y['quality']=encoder.fit_transform(data[['fixed acidity', 'volatile acidity', 'citric acid', 'residual sugar', 'chlorides',
#            'free sulfur dioxide','total sulfur dioxide',
#            'density','pH','sulphates','alcohol']])

train_x,test_x,train_y,test_y=train_test_split(df_x, df_y, test_size=0.3, random_state=12)
model.fit(train_x,train_y)

importances=model.feature_importances_

# 컬럼명+중요도
feature_df=pd.DataFrame({
    'feature':df_x.columns,
    'importance':importances
}).sort_values(by='importance',ascending=False)
print(feature_df)

# 시각화
import seaborn as  sns

plt.figure(figsize=(8,5))
sns.barplot(x="importance",y="feature", data=feature_df,orient='h')

plt.xlabel('변수별 중요도 점수')
plt.ylabel('독립변수')
plt.show()
plt.close()