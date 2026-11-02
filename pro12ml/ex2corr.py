# 공분산 / 상관계수
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import koreanize_matplotlib

data= pd.read_csv("https://raw.githubusercontent.com/pykwon/python/refs/heads/master/testdata_utf8/drinking_water.csv")
print(data.head())
print(data.describe(),'\n')

print('평균/표준편차')
print("친밀도: ",np.mean(data.친밀도),' ', np.std(data.친밀도))
print("적절성: ",np.mean(data.적절성),' ', np.std(data.적절성))
print("만족도: ",np.mean(data.만족도),' ', np.std(data.만족도),'\n')

# plt.hist([np.std(data.친밀도),np.std(data.적절성),np.std(data.만족도)])
# plt.show()
# std_values=[np.std(data.친밀도),np.std(data.적절성),np.std(data.만족도)]
# plt.hist(['친밀도','적절성','만족도'],std_values)
# plt.title('변수별 표준편차')
# plt.show()

print("======공분산 보기======")
print("친밀도vs적절성 공분산 \n",np.cov(data.친밀도,data.적절성),'\n') # numpy 함수
print("친밀도vs만족도 공분산\n",np.cov(data.친밀도,data.만족도),'\n')
print("공분산 표\n",data.cov(),'\n') # pandas Dataframe 함수.      cov()는 공통
#           친밀도       적절성       만족도
# 친밀도  0.941569  0.416422  0.375663
# 적절성  0.416422  0.739011  0.546333
# 만족도  0.375663  0.546333  0.686816
# 같은 이름으로 1:1로 된 것은 해당 값의 분산. 그것 이외 다른 값과의 관계는 공분산 관계

print("======상관계수======")
print("친밀도vs적절성 상관계수 \n",np.corrcoef(data.친밀도,data.적절성)) # numpy 함수. 0.4992
print("친밀도vs만족도 상관계수 \n",np.corrcoef(data.친밀도,data.만족도),'\n') # 0.4671
print("상관계수 표 \n",data.corr(),'\n')
# print(data.corr(method='pearson')) # 변수 연속형. 정규성을 따름
# # print(data.corr(method='spearman')) # 변수 서열형 . 정규성을 따름


print("======만족도에 따른 다른 특성 사이의 관계======")
co_re=data.corr()
print(co_re['만족도'].sort_values(ascending=False))

# 시각화
data.plot(kind='scatter', x='만족도',y='적절성')
plt.show()
plt.close()

from pandas.plotting import scatter_matrix
attr=['친밀도','적절성','만족도']
scatter_matrix(data[attr],figsize=(10,6))
plt.show()
plt.close()

import seaborn as sns
sns.heatmap(data.corr(),annot=True)
plt.show()

# heatmap에 텍스트 표시 추가사항 적용해 보기  ---------------
corr = data.corr()
# Generate a mask for the upper triangle
mask = np.zeros_like(corr, dtype=np.bool)  # 상관계수값 표시
mask[np.triu_indices_from(mask)] = True
# Draw the heatmap with the mask and correct aspect ratio
vmax = np.abs(corr.values[~mask]).max()
fig, ax = plt.subplots()     # Set up the matplotlib figure

sns.heatmap(corr, mask=mask, vmin=-vmax, vmax=vmax, square=True, linecolor="lightgray", linewidths=1, ax=ax)

for i in range(len(corr)):
    ax.text(i + 0.5, len(corr) - (i + 0.5), corr.columns[i], ha="center", va="center", rotation=45)
    for j in range(i + 1, len(corr)):
        s = "{:.3f}".format(corr.values[i, j])
        ax.text(j + 0.5, len(corr) - (i + 0.5), s, ha="center", va="center")
ax.axis("off")
plt.show()
