# Decision tree (의사결정 나무) 분류 모델
# 데이터 균일도에 따른 규칙기반의 결정트리
#트리는 데이터를 직각(수직,수평) 기준으로 나누면서 영역을 만든다.
# 결정나무는 데이터에 있는 규칙이나 패턴을 if then 형태의 나무구조로 나타내어
# 분류나 회귀를 수행하는 지도 학습모델

from sklearn.datasets import make_classification
from sklearn.tree import DecisionTreeClassifier,plot_tree
import matplotlib.pyplot as plt
import koreanize_matplotlib
import numpy as np

x,y=make_classification(n_samples=100, n_features=2,
                        n_redundant=0, n_informative=2,
                        random_state=42)
# n_informative: 분류의 더 적합한 독립변수 2개 생성
print(x[:3])
print(y[:3])
model=DecisionTreeClassifier(criterion='gini',max_depth=3) # 트리 최대값
model.fit(x,y)

print("학습 정확도(Train Accuracy): ",model.score(x,y))


# 시각화
plt.figure(figsize=(10,6))
plot_tree(model,feature_names=['x1','x2'], class_names=['0','1'],filled=True)
plt.show()

# 지니 불순도: 정의: 노드에서 무작위로 샘플을 뽑아 라벨을 임의로 지정했을 때, 잘못 분류할 확률
# 독립 변수(특성, Feature): 날씨, 습도, 이메일 단어 수 등 가지를 치는 기준(질문)
# 종속 변수(클래스, Class): 트리가 최종적으로 도달하여 분류해낸 결과물(정답)

# 결정 경계 시각화
xx,yy =np.meshgrid(
    np.linspace(x[:, 0].min(), x[:,0].max(),100), # x1범위를 100개 구간으로
    np.linspace(x[:,1].min(),x[:,1].max(),100)
)
# 수직선은 x1, 수평선은 x2.
# 왼쪽은 class(결과)0, 오른쪽은 class(결과)1


# 모든 좌표에 대해 예측값 계산
z=model.predict(np.c_[xx.ravel(), yy.ravel()])
z=z.reshape(xx.shape) # 예측 결과를 원래 grid로 변환
print(z)

plt.contour(xx,yy,z,alpha=0.3) # 영역을 색을오 채워 결정경계 표현
plt.scatter(x[:,0],x[:,1],c=y)
plt.title('Decision Boundry')
plt.xlabel('x1')
plt.ylabel('x2')
plt.show()
# 수직선은 x1, 수평선은 x2.
# 왼쪽은 class(결과)0, 오른쪽은 class(결과)1