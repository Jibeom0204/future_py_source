"""
이미지 분류란 컴퓨터가 이미지의 픽셀값을 숫자 데이터로 처리하고,
해당 이미지에 부여된 정답(Label)을 바탕으로 특징과 패턴을 학습하여 새로운 이미지가 어떤 종류에 속하는지 예측하는 기술.
전통적인 머신러닝에서는 이미지의 픽셀값을 1차원 벡터로 변환하여 학습에 사용하고
CNN같은 딥러닝에서는 이미지이 공간적 구조를 유지하면서 특징을 학습한다.

이미지 분류는 이미지를 컴퓨터가 처리할 수 있는 숫자 데이터로 표현하고,
정답이 있는 이미지들을 이용해 특징과 패턴을 학습한 뒤,
새로운 이미지가 어떤클래스에 속하는지 예측하는 과정

이미지 분류과정: 
1) 원본 이미지 -> 픽셀 수치화 -> [[124, 85 , ...],[97,52,...] -> 배열로 표현]
2) 모델 학습(배열+정답) -> 모델 생성

특성공학 기법
1. 차원 축소: 무의미한 변수 제거, PCA 추출
2. Scaling: 표준화, 정규화
3. 변형: 연속적 변수를 구간화함(Bining), 범주형을 연속형으로(Dummy)
"""

"""
PCA(주성분 분석): 선형대수 관점에서 입략데이터의 공분산 행렬을  고유값 분해하고
구한 고유벡터에 입력 데일터를 선형 변환하는 것

공분산: 두 개의 확률 변수가 함께 변하는 정도
벡터: 어디로 얼마나 가는지를 알려주는 화살표라고 생각하면 된다!
예: [1, 0] → 오른쪽으로 1칸,  [0, 1] → 위로 1칸
선형변환: 이 화살표(벡터)를 늘림,회전,기울.. 단! 무조건 직선적인 방법으로만 바꿈
주성분: 데이터가 가장 넓게 퍼져 있는 방향을 가리키는 새로운 축(공분산 행렬의 고유벡터)-> PCA를 통해 구한다

이 고유 벡터가 pca의 주성분 벡터로서 입력 데이터의 분산이 큰 방향으로 나타낸다
입력 데이터의 성질을 최대한 유지한 상태로 고차원을 저차우너 데이터로 변환하는 기법

차원축소의 3가지 순기능
1) 차원이 낮아지면 대사에 대한 이해가 보다 쉬워지게 된다
2) 연산속도가 개선된ㄴ다
3) 차원의 저즈를 해결하는 열쇠가 된다
-> 차원 증가가에 따라 요구되는 데이터의 양이 기하급수적으로 늘어나기 때문에 차원축소를 함
"""
import numpy as np
img=np.random.randint(0,256,(28,28)) #28 28 크기의 가상 흑백이미지
print(img.shape)
vector=img.flatten() # 1ckdnjs qprxjfh qusghks
print(vector.shape) # 즉 28 28 개의 픽셀을 가진 이미지는 784개 벡터로 변환


# iris data로 차원 축소
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import koreanize_matplotlib 
import seaborn as sns
import pandas as pd
from sklearn.datasets import load_iris

iris=load_iris()
n=10
x=iris.data[:n ,:2] # sepal, length, width 열만 선택
print("차원 축소 전 x: \n", x, x.shape, type(x))
print(x.T)

# 시각화1:  각 샘플의 두 특성 값을 선으로 연결해 비교
plt.plot(x.T,'o:')
plt.xticks(range(2),['꽃받침 길이', '꽃받침 너비'])
plt.grid(True)
plt.title("Iris 크기 특성")
plt.xlabel("특성(feature)의 종류")
plt.ylabel("특성값")
plt.legend(["표본{}".format(i+1) for i in range(n)])
plt.show()

# 시각화2: 산점도
df=pd.DataFrame(x)
print(df)

ax=sns.scatterplot(x=0,y=1,data=df,markers='s',s=100,color='k')
for i in range(n):
    ax.text(x[i,0]-0.05, x[i,1]+0.055, '표본{}'.format(i+1))
plt.title("Iris 크기 특성")
plt.xlabel("특성(feature)의 종류")
plt.ylabel("특성값")
plt.show()
plt.close()

"""
위 두개의 그래프 결과 두 변수는 공통적인 특징이 있으므로 차원축소의 근거가 있다고 판단.
# 일정한 패턴이 있기 때문에 근거가 있음. 일정한 패턴이니까 차원 축소해도 패턴이 유지된다는 판단.
# x가 y에 미치는 영향과는 전혀 무관. 그냥 x에 대한 패턴만 본다.

PCA를 진행 - 선형변환을 통해 차원을 축소
순서1: 입력 데이터의 공분산 행렬을 생성
순서2: 공분산 행렬의 고유벡터와 고윳값(고유벡터 크기)를 계산한다
순서3: 고윳값이 큰 순서대로 k개(PCA 변환 차수)만큼 고유벡터 추출
순서4: 고윳값이 가장 큰 순으로 추출된 고유벡터를 이용해 새롭게 입력 데아터를 변환한다.
sklearn의 PCA를 이용하면 순서대로 진행을 함
"""

# pca1=PCA(n_components=1) # 변환할 차원 수. 제1 주성분(데이터 분산이 가장 큰 방향)
pca1=PCA(n_components=2) # 변환할 차원 수. 제2 주성분(제1 주성분과 직교(90도 이룸)하면서 분산이 두번째로 큰 방향)
x_low=pca1.fit_transform(x) # 특징 행렬을 낮은 차원의 근사행렬로 변환
print("차원축소 \n",'x_low : ', x_low, ' ', x_low.shape)

# 값비교
x2=pca1.inverse_transform(x_low) # 주 성분값 원복
print('원본: ', x[0, :])
print('주성분: ', x_low[0])
print('원본: ',x2[0, :])


# 주성분 분석값을 기반으로 시각화: PCA 방향벡터
# 주성분: 데이터가 가장 넓게 퍼져 있는 방향을 가리키는 새로운 축
pc1 = pca1.components_[0] # components : 주성분 벡터
mean=x.mean(axis=0)
for i in range(n):
    ax.text(x[i,0]-0.05, x[i,1]+0.055, '표본{}'.format(i+1))

# PCA 축(화살표)
plt.quiver(
    mean[0], mean[1], 
    pc1[0],pc1[1],
    scale=3,color='r',width=0.01
)
plt.title("Iris 크기 특성+제1 주성분")
plt.xlabel("꽃받침 길이")
plt.ylabel("꽃받침 너비")
plt.axis('equal') # x,y 눈금간격 동일 비율로 표시
plt.grid(True)
plt.show()
plt.close()

print("\n=====================================\n")

# 원본열 4개를 차원 축소해 2개의 열로 변환 후 SVM 분류 모델을 작성
x=iris.data
print(x[0,:])
pca2=PCA(n_components=2)
x_low2=pca2.fit_transform(x)
print('x_low2: ',x_low2[0,:], ' ', x_low2.shape)

# 변동성 비율 확인
print(pca2.explained_variance_ratio_)
x4=pca2.inverse_transform(x_low2)
print("최초 자료: ",x[0])
print("차원 축소: ",x_low2[0])
print("차원 복귀: ",x4[0, :],'\n')

iris1=pd.DataFrame(x,columns=['sepal length','sepal width','petal length','petal width'])
print(iris1.head(3))
iris2=pd.DataFrame(x_low2, columns=['var1','var2']) # var1,var2가 제1,2 주성분을 말하는게 아님
print(iris2.head(3))

from sklearn import svm, metrics
print("\n=========원본 데이터로 SVM 분류모델 작성=========\n")
feature1=iris1.values
print(feature1[:3])
label=iris.target
#(정답/Label): 각 꽃이 어떤 품종인지(Setosa=0, Versicolor=1, Virginica=2) 적혀있는 실제 정답 리스트
print(label[:3])

model1=svm.SVC(C=0.1, random_state=0).fit(feature1,label)
pred1=model1.predict(feature1)
print('model1 accuracy: ', metrics.accuracy_score(label,pred1))

print("\n========PCA본 데이터로 SVM 분류모델 작성=========\n")
feature2=iris2.values
print(feature1[:3])

model2=svm.SVC(C=0.1, random_state=0).fit(feature2,label)
pred2=model2.predict(feature2)
print('model1 accuracy: ', metrics.accuracy_score(label,pred2))