"""
xor 분류: LogisticRegression과 Svm으로 분류
"""
x_data=[
    [0,0,0],
    [0,1,0],
    [1,0,0],
    [1,1,1]
]
import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn import svm,metrics

x_df=pd.DataFrame(x_data)
print(x_df)
print(x_df)
feature=np.array(x_df.iloc[:,0:2])
label=np.array(x_df.iloc[:,2])
print(feature)
print(label)

lmodel=LogisticRegression()# 선형 분류모델
smodel=svm.SVC(kernel='linear') # 비선형 분류모델 모델 rbf도 가능

# 모델별 학습
lmodel.fit(feature,label)
smodel.fit(feature,label)

pred1=lmodel.predict(feature)
print("lmodel 예측값: ",pred1)
pred2=lmodel.predict(feature)
print("smodel 예측값: ",pred2)

acc1=metrics.accuracy_score(label,pred1)
print("lmodel 정확도: ",acc1)
acc2=metrics.accuracy_score(label,pred2)
print("lmodel 정확도: ",acc2)