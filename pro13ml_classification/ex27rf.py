"""
Randomforest 분류 알고리즘
머신러닝에서 분류와 회귀 분석에 널리 사용되는
강력한 앙상블 학습 알고리즘
여러개의 결정 트리를 생성하고 이들의 예측결과를 종합하여
최종적인 분류 결과를 도출
앙상블 기법 중 배깅을 사용
복수의 샘플 데이터와 결정트리를 학습시키고 결과를 집계하는 방식
참고 우수한 성능은 부스팅, 과적합이 걱정된다면 배깅

"""

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split,cross_val_score
from sklearn.metrics import accuracy_score

df=pd.read_csv("https://raw.githubusercontent.com/pykwon/python/refs/heads/master/testdata_utf8/titanic_data.csv")
# print(df.head(2))
# print(df.info())
# print(df.shape) #(891, 12)
# print(df.isnull().any())

df=df.dropna(subset=['Pclass','Age','Sex'])
print(df.shape) #(891, 12)-- Null 제외 -->(714, 12)
df_x=df[['Pclass','Age','Sex']].copy() # feature
print("df_x.shape",df_x.shape) # .shape: 데이터프레임의 행과 열의 갯수를 튜플로
print(df_x.head(3))
#    Pclass   Age     Sex
# 0       3  22.0    male
# 1       1  38.0  female
# 2       3  26.0  female


# 범주형(문자열)데이터를 숫자형태로 바꿔줘야함
# 전처리 --Sex 열(male,female) -> Label Encoding(문자(범주형) -> 정수로)
from sklearn.preprocessing import LabelEncoder
encoder= LabelEncoder()
df_x['Sex']=df_x['Sex'].astype('object') # 정수 대입 가능 자료형으로 변경
df_x['Sex'] = encoder.fit_transform(df_x['Sex'])
print(df_x.head(3))
#    Pclass   Age  Sex
# 0       3  22.0    1 male
# 1       1  38.0    0 female


df_y=df['Survived'] # label(class) # 원본 데이터에서 Null값 제외한 것 중 Survived(생존자)수를 결과 데이터프레임에 새로 저장
print(df_y.head(3)) # 1 생존 0 사망
print()


train_x,test_x,train_y,test_y=train_test_split(df_x, df_y, test_size=0.3, random_state=12)
print("데이터들 크기\n",train_x.shape,test_x.shape,train_y.shape,test_y.shape)
# (499, 3) (215, 3) (499,) (215,)

# 모델 생성
model=RandomForestClassifier(criterion='gini',n_estimators=500,random_state=12)
# criterrion 'entropy' 도 가능. DecsionTree의 개수 -> n+estimators= 100이 기본
print("모델 생성 결과: \n",model,'\n')

model.fit(train_x,train_y) # 문제와 정답을 같이 줘서 학습시킴.
pred=model.predict(test_x)

print('예측값:',pred[:5])
print('실제값:',np.array(test_y[:5]))
print('맞춘 개수: ',sum(test_y==pred))
print("전체 대비 맞춘 비율: ",sum(test_y==pred)/len(test_y))
print('분류 정확도: ',accuracy_score(test_y,pred),'\n')

# 교차검증(KFold)
cross_vali=cross_val_score(model, df_x, df_y,cv=5)
# cv=kfold 몇번 접어서 검증할지. 위에서 선언한 train데이터 0.7을 5번 접는 비율로 나누어서 검정

print("==========교차 검증단==========")
print(cross_vali) #[0.75524476 0.8041958  0.81818182 0.83216783 0.83098592] => cv 1회당 검증결과
print("교차 검증 평균 정확도: ", np.round(np.mean(cross_vali),4),'\n')

# ##########RandomForestClassifier는 중요 변수 제공################
print('\n==============중요 변수 확인하기==============\n')
print('특성(변수,feature) 중요도: ',model.feature_importances_)
# model.feature_importances_ : 각 특성이 예측에 기여한 정도(중요도)를 수치로 반환
# 중요도 값의 합은 1.0, 수치가 클수록 해당 변수가 불순도 감소에 더 많이 기여함=종속 변수
# 수치는 독립변수 열 순서와 동일('Pclass',''Age','Sex')

# 시각화
import matplotlib.pyplot as plt
import koreanize_matplotlib
n_features=df_x.shape[1]
plt.barh(range(n_features),model.feature_importances_,align='center')
plt.xlabel('변수별 중요도 점수')
plt.ylabel('독립변수')
plt.yticks(np.arange(n_features),df_x.columns)
plt.show()
plt.close()

print()
# 전체 변수 대상으로 중요도 확인
# Ticket,Cabin,Embarked: 문자형 - 바로 상ㅇ불가함
# PassengerID,Name,Survived와 상관없는 변수-> 제외하기

df_imsi=df[['Pclass','Age','Sex','Fare','SibSp','Parch']].copy()
df_imsi['Sex']=df_imsi['Sex'].astype('object')# 정수대입 가능 자료형
df_imsi['Sex']=encoder.fit_transform(df_imsi['Sex'])
train_x,test_x,train_y,test_y=train_test_split(df_imsi, df_y, test_size=0.3, random_state=12)
model.fit(train_x,train_y)

importances=model.feature_importances_

# 컬럼명+중요도
feature_df=pd.DataFrame({
    'feature':df_imsi.columns,
    'importance':importances
}).sort_values(by='importance',ascending=False)
print(feature_df)
#   feature  importance
# 1     Age    0.292984
# 3    Fare    0.276886
# 2     Sex    0.241788
# 0  Pclass    0.090802
# 4   SibSp    0.057529
# 5   Parch    0.040012

# 시각화
import seaborn as  sns

plt.figure(figsize=(8,5))
sns.barplot(x="importance",y="feature", data=feature_df,orient='h')

plt.xlabel('변수별 중요도 점수')
plt.ylabel('독립변수')
plt.show()
plt.close()