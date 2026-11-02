"""
tv,radio,newspaper 간의 상관관계를 파악하시오. 
또한 sales와 관계를 알기 위해 sales에 상관 관계를 정렬한 후 TV, radio, newspaper에 대한 영향을 해석하시오.
그리고 이들의 관계를 heatmap 그래프로 표현하시오. 
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import koreanize_matplotlib
import seaborn as sns

data=pd.read_csv("https://raw.githubusercontent.com/pykwon/python/refs/heads/master/testdata_utf8/Advertising.csv")
data=data.set_index('no')
print("상위 5개\n",data.head(),'\n')
print("수치\n",data.describe(),'\n')
print("티비 vs 라디오 vs 신문 상관관계\n",data.corr(),'\n')

#data=data.corr() # 아예 저장해두기

# 항목별 sales와 상관관계
sales_corr=data.corr()
print("sales와 각 항목별 상관관계 통합 출력\n",sales_corr['sales'].sort_values(ascending=False)) # 전체 출력

# 자기 자신과의 상관관계 제거
fix_sales_corr=sales_corr['sales'].drop('sales')

print("상관관계 분석 결과===")
for name, r in fix_sales_corr.items():
    if r >0:
        msg="양의 상관관계"
    elif r <0:
        msg='음의 상관관계'
    else:
        msg='선형 상관관계 없음'

print(f'{name}:r={r:.3f},msg')
print("\nSales와 양의 상관관계가 높은 광고 매체",fix_sales_corr.idxmax())




sns.heatmap(sales_corr,annot=True)
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