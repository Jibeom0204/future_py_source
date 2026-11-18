# 쇼핑몰 고객 세분화
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import koreanize_matplotlib
from sklearn.cluster import KMeans

# 가상의 고객자료 생성
np.random.seed(0)
n_customers=200# 고객수
annul_spending=np.random.normal(50000,15000,n_customers)#연간 지출액
monthly_visits=np.random.normal(5,2,n_customers) # 월 방문 횟수

# 구간 나누기(음수 제거, clip 사용해서 0으로 대체)
# a=np.array([-3.2, -0.54, 1.5]) -> np.clip(a,0,1)  ->[0,0,1]
annul_spending=np.clip(annul_spending,0,None)
monthly_visits=np.clip(monthly_visits,0,None)

data=pd.DataFrame({
    'annul_spending': annul_spending,
    'monthly_visits':monthly_visits
})
print(data.head(),data.shape)

# 산포도
plt.scatter(data['annul_spending'],data['monthly_visits'])
plt.xlabel('연간 지출액')
plt.ylabel('한달 방문수')
plt.title('소비자 지출 현황')
plt.show()

# Kmeans 군집화
kmeans=KMeans(n_clusters=3,random_state=0)
clusters=kmeans.fit_predict(data)

# 군집별 자료 보기
data['cluster']=clusters
print(data.head(3))

# 군집 결과 시각화
for cluster_id in np.unique(clusters):
    clusters_data =data[data['cluster']==cluster_id]
    print(data[data['cluster']==cluster_id])

    plt.scatter(
        clusters_data['annul_spending'],
        clusters_data['monthly_visits'],
        label=f'군집{cluster_id}'
    )

# 중심점
plt.scatter(kmeans.cluster_centers_[:,0], kmeans.cluster_centers_[:,1],
            c='black', marker='x', s=200, label='중심점')
plt.xlabel('연간 지출액')
plt.ylabel('한달 방문수')
plt.title('소비자 군집 현황')
plt.legend()
plt.show()

print('\n 각 군집별 고객 출력======')
for cluster_id in range(3):
    clu_data=data[data['cluster']==cluster_id]
    print(f'\n===군집{cluster_id}===')
    print(f'고객수: {len(clu_data)}명')
    print(clu_data.to_string(index=True))

# ===군집2===
# 고객수: 61명
#      annul_spending  monthly_visits  cluster
# 5      35340.831802        1.766088        2
# 19     37188.563910        4.915486        2