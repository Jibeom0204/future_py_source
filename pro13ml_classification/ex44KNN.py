# KNN -bresast Cancer_dataset 사용

import numpy as np
import pandas as pd
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler,MinMaxScaler
from sklearn.metrics import accuracy_score,classification_report,confusion_matrix

data=load_breast_cancer()
x=data.data # feature 특징
y=data.target #label (0:malignant, 1:benign)
print(x[:1],' ',x.shape)
print(y[:1],' ',np.unique(y)) 

x_train,x_test,y_train, y_test=train_test_split(
    x,y,test_size=0.2, random_state=42, stratify=y
)

# 스케일링 필요(∵: 거리 기반 모델이므로 크기가 영향을 미침) # ∵ 왜냐하면  ∴: 따라서?
scaler=StandardScaler()
x_train_scaled=scaler.fit_transform(x_train) # fit: 데이터로부터 변환에 필요한 평균, 표준편차, 최솟값, 최댓값 등 계산하고 학습
x_test_scaled=scaler.fit_transform(x_test)

# K-NN은 ㅏ값이 중요(작으면 과적합, 크면 과소적합)
# 최적의 k값을 확인하는것이 중요
train_acc=[]
test_acc=[]
k_range=range(3,12,2)

for k in k_range:
    model=KNeighborsClassifier(n_neighbors=k)
    model.fit(x_train_scaled,y_train)

    # 예측
    y_train_pred=model.predict(x_train_scaled)
    y_test_pred=model.predict(x_test_scaled)

    # 정확도
    train_acc.append(accuracy_score(y_train,y_train_pred))
    test_acc.append(accuracy_score(y_test,y_test_pred))

print("\n훈련 정확도: ",train_acc)
print("테스트 정확도: ",test_acc)

# test data 정확도를 비교해서 K값을 선택함
# 좀 더 바람직한 방법은 GridSearchCV를 사용하는게 맞음
best_idx=np.argmax(test_acc)
best_k=list(k_range)[best_idx]
best_acc=test_acc[best_idx]
print('\n최적의 k값: ',best_k)
print('최고 정확도: ',best_acc)

# 시각화
import matplotlib.pyplot as plt
plt.figure()
plt.plot(k_range,train_acc,marker='o', c='b', label='train acc')
plt.plot(k_range,test_acc,marker='s', c='r', label='test acc')
plt.xlabel('k value')
plt.ylabel('accuracy') # 하나만 들어가면 모든 한글이 다깨지나 애만 깨지나? -> 얘만 깨지네
plt.legend()
plt.grid()
plt.show()

# best_k갑승로 모델 생성 후 예측...생략..따로 해보기