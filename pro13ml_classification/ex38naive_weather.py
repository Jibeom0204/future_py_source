# 나이브 베이즈 알고리즘을 이용한 분류 -weather
import pandas as pd
import numpy as np
df=pd.read_csv("https://raw.githubusercontent.com/pykwon/python/refs/heads/master/testdata_utf8/weather.csv")
print(df.head(2))
print(df.info)

# 전처리===
df=df.drop("Date",axis=1)
print("햇빛 평균",df['Sunshine'].mean())
df['Sunshine']=df['Sunshine'].fillna(df['Sunshine'].mean())  # 결측치를 0,혹은 평균으로 채우면 좋다

# 범주형 처리
df['RainToday']=df['RainToday'].map({'Yes':1, 'No':0})
df['RainTomorrow']=df['RainTomorrow'].map({'Yes':1, 'No':0})
print(df.head(2))

x=df.drop('RainTomorrow',axis=1)
y=df["RainTomorrow"] # label(class)

from sklearn.model_selection import train_test_split
x_train,x_test,y_train,y_test=train_test_split(x,y, test_size=0.2,random_state=42, stratify=y)

#Naivebayes 모델 학습
from sklearn.naive_bayes import GaussianNB,BernoulliNB,MultinomialNB
model=GaussianNB()
model.fit(x_train,y_train)

# 예측 및 평가 
from sklearn.metrics import accuracy_score,confusion_matrix
pred=model.predict(x_test)
print('분류 정확도: ',accuracy_score(y_test,pred))
print('confusion_matrix: \n', confusion_matrix(y_test,pred))

print() # 교차 검증
from sklearn.model_selection import cross_val_score
scores=cross_val_score(model,x,y,cv=5)
print(f'교차 검증에서 각 fold:{scores}, 평균:{scores.mean()}')
print()

# feature 중요도 분석: feature가 정규분포를 따른다는 가정하에 클래스별 평군
# GaussianNB의 멤버로 Theta_: 각 클래스 별 feature 평균을 반환
mean_0=model.theta_[0] # raintomorrow=0 비 안 오는날 평균
mean_1=model.theta_[1] # raintomorrow=0 비 오는날 평균

# 각 feature가 비오는날 vs 비 안오는 날에서 얼마나 차이가 나는가?
importance = np.abs(mean_1-mean_0)

feat_info=pd.DataFrame({
    'feature':x.columns, 'importance': importance
}).sort_values(by='importance',ascending=False)
print('feature  중요도',feat_info)

#importance 시각화
import matplotlib.pyplot as plt
import koreanize_matplotlib
plt.figure()
plt.bar(feat_info['feature'],feat_info['importance'])
plt.xlabel('feature')
plt.ylabel('중요도(평균차이)')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

print("새로운 자료에 대한 예측")
newdata=pd.DataFrame([{
    'MinTemp':1.3,
    'MaxTemp':15.0,
    'Rainfall':0.0,
    'Sunshine':10.0,
    'WindSpeed':3.0,
    'Humidity':40.0,
    'Pressure':1000.0,
    'Cloud':3,
    'Temp':20.0,
    'RainToday':0,
}])
newpred=model.predict(newdata)
print('예측결과: ' , '비옴'if newpred==1 else '비안옴')
print('확률은', model.predict_proba(newdata))