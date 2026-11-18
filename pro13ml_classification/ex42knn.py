"""
최근접 이웃: K - Nearest Neighbors
알고리즘은 우리가 예측하려고 하는 임의의 데이터와 가장 가까운 거리의
데이터 K개를 찾아 다수결에 의해 데이터를 예측하는 방법
거리가 가까운 K개의 이웃을 선택할 때 유클리드 거리를 사용한다
"""

from sklearn.neighbors import KNeighborsClassifier
import matplotlib.pyplot as plt
import numpy as np

train=[
    [5,3,2],
    [1,3,5],
    [4,5,6]
] # 세로로 특성 1,2,3. 열별로 특성. 5 1 4/3 3 5/2 5 6 이 특성
label=[0,1,1] # 정답지

train=np.array(train)
plt.scatter(train[:,0],train[:1], c=label,s=100,cmap='coolwarm')
plt.xlabel('특성1')
plt.ylabel('특성2')
plt.show()

# 가까운 이웃 3개를 참조. 가까운 이웃일술곧 더 높은 가중치를 부여
Kmodel=KNeighborsClassifier(n_neighbors=3, weights='distance')
Kmodel.fit(train,label)
pred=Kmodel.predict(train)
print("pred: ",pred)
print(f'시험 정확도: {Kmodel.score(train,label)}')

# 새로운 데이터로 예측하기
new_data=[[1,2,9],[6,2,1]]
new_pred=Kmodel.predict(new_data)