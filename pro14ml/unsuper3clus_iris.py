# 계층적 군집 분석: 데이터를 단계적으로 묵어 군집을 형성하는 알고리즘
# 거리가 가까운 데이터부터 계속 묶어가는 방식
# 군집 수를 미리 정하지 않아도 됨. 구조는 덴드로그램으로 확인

import numpy as np
import matplotlib.pyplot as plt
import koreanize_matplotlib
import seaborn as sns
import pandas as pd
from scipy.cluster.hierarchy import linkage,dendrogram,fcluster
from sklearn.datasets import load_iris
from sklearn.preprocessing import StandardScaler
#linkage: 데이터를 가까운 순서대로 병합하고, 그 병합 기록을 표(배열)로 반환
#fcluster: linkage가 만든 트리(Z)를 특정 기준으로 잘라서, 각 데이터가 어느 클러스터에 속하는지 번호를 붙여 주는 함수


iris=load_iris()
x=iris.data
y=iris.target
labels=iris.target_names

df=pd.DataFrame(x,columns=iris.feature_names)
print(df.head(2))

# 스케일링 - 권장
scaler=StandardScaler()#각 특성(Feature)의 평균을 0, 표준편차를 1로 만들어 표준 정규 분포 형태로 변환
# 거리기반: KNN, SVM, K-Means 등 데이터가 거리를 계산 하는 모델에서 단위(cm,원) 차이 떄문에 특정변수 과대평가 되는거 방지
# 선형 모델: 선형회귀(LinearRegression), 로지스틱 회귀(Logistic Regression) 등 경사하강법의 수렴속도 안정성 향상
x_scaled=scaler.fit_transform(x)

# 계층적 군집 분석
z=linkage(x_scaled,method='ward')

# 덴드로그램
plt.figure(figsize=(12,5))
dendrogram(Z=z)
plt.title('아이리스로 계층적 군집 분석')
plt.xlabel('샘플')
plt.ylabel('거리(유클리드)')
plt.show()

# 덴드로그램을 분리해 최대 3개의 군집 만들기
clusters= fcluster(Z=z,t=3,criterion='maxclust')
df['cluster'] = clusters
print(df.head(3))

# 2개 feature 시각화(산점도)
plt.figure(figsize=(6,5))
sns.scatterplot(x=x_scaled[:,0], y=x_scaled[:,1],hue=clusters,palette='Set1')
#hue=clusters: 클러스터 중심 palette='Set1 : 색상스타일'
plt.title('군집결과')
plt.xlabel('feature1')
plt.ylabel('feature2')
plt.show() # 꽤 비슷하게 나눠짐. 군집은 라벨이 없음
print('실제라벨: ',y[:10]) #[0 0 0 0 0 0 0 0 0 0]. y=iris.target
print('군집결과:',clusters[:10],'\n') #[1 1 1 1 1 1 1 1 1 1].  실제 0이 군집 1로 그룹화

print('================군집 결과 검증================')
print("교차표: 실제 라벨 vs 군집 결과")
ct=pd.crosstab(y,clusters)
print("빈도표\n",ct,'\n')
print(ct.shape)
# col_0   1   2   3
# row_0            
# 0      49   1   0
# 1       0  27  23
# 2       0   2  48
# col_0(군집결과): cluster1 cluster2 cluster3
# row_0(실제라벨): 0-setosa  1-versicolor  2-verginica
# setosa는 완벽 분리도이고 1-versicolor  2-verginica는 일부 섞임

print("================교차표 보조 설명================")
for i in range(ct.shape[0]):
    max_cluster = ct.iloc[i].idxmax()
    print(f'실제 클래스 {i} -> 군집 {max_cluster} (갯수:{ct.iloc[i].max()})')
print()

# 정량적 평가: 군집 결과가 실제 정답과 얼마나 유사한지를 수치화
from sklearn.metrics import adjusted_mutual_info_score,normalized_mutual_info_score
# adjusted_mutual_info_score: ARI(수정된)- 같은 그룹끼리 잘 묶였는지 평가
ari=adjusted_mutual_info_score(y,clusters)
print(f'평가지표(ARI): {ari:.4f}')
# 해석기준: 0.7 이상 (매우 잘 된 군집) // 0.5~0.7(잘 된 군집) // 0.5 미만(별로)

# normalized_mutual_info_score:NMI: 정보량 기준으로 얼마나 유사한지 확
# (군집간 얼마나 같은 정보를 공유하는가)
nmi=normalized_mutual_info_score(y,clusters)
print(f'평가지표(NMI): {nmi:.4f}') #0~1 사이의 값. 1에 가까울수록 완벽