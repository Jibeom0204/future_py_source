# 다층 신경망(MLP) 다항분리(3개)

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.datasets import load_wine
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score,confusion_matrix,classification_report
from sklearn.preprocessing import StandardScaler,MinMaxScaler # 표준화 정규화
from sklearn.neural_network import MLPClassifier


data=load_wine()
x=data.data
y=data.target
print(x[:2], ' ',x.shape)
print(y[:2],' ',np.unique(y))
x_train, x_test, y_train, y_test = train_test_split(
    x,y,test_size=0.2, random_state=42, stratify=y)

# Scaleing(MLP에서 권장)
scaler=StandardScaler()
x_train_scaled=scaler.fit_transform(x_train)
x_test_scaled=scaler.fit_transform(x_test)

# 모델 생성
model=MLPClassifier( 
    hidden_layer_sizes=(20,10), # 은닉층 2개(첫번째: Node 20개, 두번째 10개)
    solver='adam', # 손실 최소화
    activation='relu',  # 은닉층의 활성화 함수
    max_iter=150,
    learning_rate_init=0.001,
    random_state=42,
    verbose=1 # 학습 도중 로그 출력 여부
)

model.fit(x_train_scaled,y_train)
pred=model.predict(x_test_scaled)
print('모델 정확도 acc: ', accuracy_score(y_test, pred)) # 실제값, 예측값
print('classification:', classification_report(y_test,pred))

# 혼동행렬 시각화
cm=confusion_matrix(y_test, pred)
plt.figure(figsize=(5,4))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
plt.title('confusion matrix')
plt.xlabel('predict')
plt.ylabel("actual")
plt.show()