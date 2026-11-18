"""
DBSCAN: 노이즈가 포함된 응용의 밀도 기반 공간 클러스터링
k-means와 같은 전통적인 클러스터링 방법과 달리 DNSCAN은 클러스터 수를
미리 지정할 필요가 없으면 불규칙한 형태와 다양한 밀도를 가진 데이터 셋에 특히 적합
DBSCAN은 밀도가 다양하지 않거나 모양이 불규칙한 클러스터가 있는
데이터와 같이 모양이 잘 정의되지 않고 이상치가 많은 데이터를 처리할 때
유용하게 사용 가능하다.
"""
import matplotlib.pyplot as plt
from matplotlib import style
from sklearn.datasets import make_moons
from sklearn.cluster import KMeans, DBSCAN

# data
x,y=make_moons(n_samples=200,noise=0.05, shuffle=True, random_state=0)
print(x[:5], x.shape)

plt.scatter(x[:,0], x[:,1],c=y)
plt.show() # 두 값이 겹치는 부분이 처리하기 어려움

print('\n===========KMeans로 군집화===========\n')
km=KMeans(n_clusters=2, init='k-means++',random_state=0)
pred1=km.fit_predict(x)
print("K -means 예측 군집",pred1[:10])

# km 시각화
def plotResult(x,pr):
    plt. scatter(x[pr==0,0], x[pr==0,1],c='blue',marker='o',s=40, label='cluster1')
    plt. scatter(x[pr==1,0], x[pr==1,1],c='red',marker='s',s=40, label='cluster2')
    plt.scatter(km.cluster_centers_[:,0],km.cluster_centers_[:,1], color='black', marker='+', label='centroid')
    plt.title("클러스터링 결과")
    plt.legend()
    plt.show()


plotResult(x,pred1) # 결과가 옳지 않음?


print('\n===========DBSCAN으로 군집화===========\n')
dbs=DBSCAN(eps=0.2,min_samples=5,metric='euclidean')
#eps: 샘플간 최대 거리, min_samples: 점에 대한 이웃 샘플 수(반경포인트들)
pred2=dbs.fit_predict(x)
print('DBSCAN 군집 id',pred2[:10])
print('군집 종류: ',set(pred2))

plotResult(x,pred2) # 분류가 제대로 됨. 모양에 따라 군집 생성
# KMeans는 k개의 군집의 갯수를 ㅁ자추고 DBNSCAN은 밀도에 의;해 군집 형태를 구성함.