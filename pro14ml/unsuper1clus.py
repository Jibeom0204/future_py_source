"""
군집분석: 데이터 간의 유사도를 정의하고 그 야수도에 가까운 것부터
순서대로 합쳐가는 방법으로, 거리나 상관계수 등을 이용
이는 비슷한 특성을 가진 객체를 그룹으로 만들고,
군집 분리 후 t=test,Anova 분석등을 통해 군집간 평균의 차이를 확인할 수도 있음
군집 분석은 데이터만 주고 label은 제공하지 않는 비지도 학습이다.

클러스터링 기법 중 계층적 클러스터링 연습
- 응집형: 군집의 크기를 점점 늘리기_상향식
- 분리형: 군집의 크기를 줄여 나가기_하향식
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import koreanize_matplotlib

np.random.seed(123)
var=['x','y']
labels=['점0','점1','점2','점3','점4']
x=np.random.random_sample([5,2])*10
df=pd.DataFrame(x,columns=var,index=labels)
print(df)

plt.scatter(x[:,0], x[:,1],c='blue',marker='o',s=50)
#text 추가
for i,txt in enumerate(labels):
    plt.text(x[i,0],x[i,1],txt)

plt.grid(True)
plt.show()

# 각 점 간의 거리 계산
from scipy.spatial.distance import pdist,squareform
dist_vec=pdist(df,metric='euclidean')
print('dist_vec',dist_vec) # 누가 어떤거랑 거리를 가지는지 명확히 알 수 없음

# pdist의 결과를 사각형 형식으로 표현
# 누가 어디랑 어느정도 거리를 관계로 갖는지
row_dist=pd.DataFrame(
    squareform(dist_vec),columns=labels, index=labels)
print(row_dist,'\n\n')
#           점0        점1        점2        점3        점4
# 점0  0.000000  5.393133  1.388848  4.896710  2.401826
# 점1  5.393133  0.000000  5.090279  7.656440  2.998344
# 점2  1.388848  5.090279  0.000000  3.698301  2.405416
# 점3  4.896710  7.656440  3.698301  0.000000  5.792346
# 점4  2.401826  2.998344  2.405416  5.792346  0.000000

# 계층적 클러스터링(군집분석)
from scipy.cluster.hierarchy import linkage # 계층적 응집형
row_cluseters=linkage(dist_vec,method='ward')
# print(row_clusters)
df2=pd.DataFrame(row_cluseters,columns=['군집id1', '군집id2', '거리', '군집멤버'])
print(df2)
#    군집id1  군집id2        거리  군집멤버수
# 0    0.0    2.0  1.388848   2.0

# <-- 점0과 점2를 병합, 병합된 군집의 데이터수 :2 새로운 군집 id:5
# 1    4.0    5.0  2.657109   3.0  => 위의 점 0, 점2와 점 4가 합쳐서 점 5의 결과를 도출
# 그래서 군집 데이터 수가 3

# <-- 점4과 점5를 병합, 병합된 군집의 데이터수 :3 새로운 군집 id:6
# 2    1.0    6.0  5.454004   4.0

# <-- 점1과 점6를 병합, 병합된 군집의 데이터수 :3 새로운 군집 id:7
# 3    3.0    7.0  6.647102   5.0

# # 군집 7={점0, 점1, 점2, 점4}
# 3, 3.0 7.0 6.647102 5.0
# 하나씩 다 합쳐짐. 최종적으로 점 5개 점이 하나의 군집이 됨

print("\n=================군집 6에 속한 멤버(점)들 보기=================\n")
from scipy.cluster.hierarchy import to_tree
root,nodes=to_tree(row_cluseters,rd=True) # linkage결과를 트리구조로 변환
ids=nodes[6].pre_order() #군집6에 속한 원본 점 id
print('군집6의 점 id:',ids)
print('군집6dml wjadlfma : ',[labels[i] for i in ids])
print(df.iloc[ids]) # 군집 6에 포함된 실제 데이터

# 군집의 계층 구조를 계통도(dendrogram)로 출력
from scipy.cluster.hierarchy import dendrogram
dendrogram(row_cluseters, labels=labels)
plt.tight_layout()
plt.ylabel('유클리드 거리값')
plt.show()

