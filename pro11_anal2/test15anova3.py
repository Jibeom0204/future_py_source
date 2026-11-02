# 어느 음식점의 매출과 날씨 자료를 이용해 온도에 따른 매출액 평균의 차이 검정 -------------------------
# 어느 음식점의 매출 데이터와 기상청이 제공한 날씨 데이터를 활용하여 
# 강수 여부에 따른 매출액의 평균에 차이가 있는지 검정.

# 세 집단 : 추움 보통 더움

# 매출 데이터 : tsales.csv
# 날씨 데이터 : tweather.csv

# 귀무 : 온도에 따라 매출액의 평균에 차이가 없다.
# 대립 : 온도에 따라 매출액의 평균에 차이가 있다.

from scipy import stats
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import koreanize_matplotlib
import seaborn as sns

pd.set_option('display.max_columns', None)

# 매출 데이터 읽기
sales_data = pd.read_csv("https://raw.githubusercontent.com/pykwon/python/refs/heads/master/testdata_utf8/tsales.csv", dtype={'YMD':'object'})  # int -> object로 변환해 읽기
print(sales_data.head(2))
print(sales_data.info())   # 328 * 3

# 날씨 데이터 읽기
wt_data = pd.read_csv("https://raw.githubusercontent.com/pykwon/python/refs/heads/master/testdata_utf8/tweather.csv")
print(wt_data.head(2))
print(wt_data.info())      # 702 * 9

print()
# sales_data : YMD 20190514,  wt_data : tm 2018-06-01 이므로 병합을 위해 변환 필요
wt_data.tm = wt_data.tm.map(lambda x:x.replace("-", ""))
print(wt_data.head(2))
#    stnId        tm  avgTa  minTa  maxTa  sumRn  maxWs  avgWs  ddMes
# 0    108  20180601   23.8   17.5   30.2    0.0    4.3    1.9    0.0

print()
# 두 데이터 병합
frame = sales_data.merge(wt_data, how='left', left_on='YMD', right_on='tm')
print(frame.columns) 
# ['YMD', 'AMT', 'CNT', 'stnId', 'tm', 'avgTa', 'minTa', 'maxTa', 'sumRn','maxWs', 'avgWs', 'ddMes']
print(frame.head(3), ' ', len(frame))   # 328

data = frame.iloc[:,  [0, 1, 7, 8]]  # YMD  AMT  maxTa  sumRn
print(data.head())
print('결측치 확인 : ', data.isnull().sum(), '\n')

# plt.boxplot(data.maxTa)
# plt.show()
print("최대값",data.maxTa.describe()) #print(data['maxTa].describe()) 같은 기능 
# 최소 -4.9 평균 18.5 최대 36.8

# 온도를 세 극룹으로 분리(연속형 -> 범주형)
data['ta_gubun']=pd.cut(data.maxTa,bins=[-5,8,24,37],labels=[0,1,2])
print(data.head(7),' ', data['ta_gubun'].unique(),'\n')
# 요인 1개(온도): 그룹은 3개(0,1,2)

# 정규성/등분산성 확인
x1=np.array(data[data['ta_gubun']==0].AMT) # 추움 그룹 매출
x2=np.array(data[data['ta_gubun']==1].AMT) # 보통
x3=np.array(data[data['ta_gubun']==2].AMT) # 더움
print("x1만 출력",x1[:5],'\n') #x1만 출력 [1050500  770000 1054500  969000 1061500]

# shapiro(): 정규성(Normality)을 검정
# 정규성: 평균을 중심으로 좌우 대칭을 이루는 종 모양의 정규분포
print("x1 값: ",stats.shapiro(x1).pvalue) # 0.2481 > 0.05 정규성 만족
print("x2 값: ",stats.shapiro(x2).pvalue) # 0.0388 < 0.05 정규성 만족 x
print("x3 값: ",stats.shapiro(x3).pvalue,'\n') # 0.3182 > 0.05 정규성 만족

# levene(x1,x2,x3): 세 개 이상의 독립적인 표본 집단(x1, x2, x3) 간의 등분산성(Homoscedasticity)을 검정하는 르벤 검정 함수
# 등분산성: 평균을 비교하고자 하는 두 개 이상의 독립적인 집단들이 통계적으로 동일한 수준의 분산(데이터가 퍼져 있는 정도)을 가지고 있는 상태
print(stats.levene(x1,x2,x3).pvalue,'\n') # 0.03900<0.05 등분산성 만족


print("온도별 매출액 평균")
# Pandas 지수 표기 해제법
pd.options.display.float_format = '{:,.2f}'.format
spp=data.loc[:,['AMT','ta_gubun']]
print('매출액 평균: ',spp.groupby('ta_gubun').mean(),'\n')
print(f'x1 평균: {np.mean(x1):.2f}') # 1032362.32
print(f'x2 평균: {np.mean(x2):.2f}') # 818106.87
print(f'x3 평균: {np.mean(x3):.2f}','\n') # 553710.94 

group1,group2,group3=x1,x2,x3
print(stats.f_oneway(group1,group2,group3),'\n')
#F_onewayResult(statistic=np.float64(99.1908), pvalue=np.float64(2.3607e-34)) 
# 해석: pvalue=np.float64(2.3607e-34 < alpha 0.05이므로 귀무기각
# 해당 음식점은 온도에 따라 매출 평균에 차이가 있음을 인정

# 정규성이 깨지면 stats.kruskal() 사용, 등분산성이 깨지면 welch's ANOVA
#Kruskal-Wallis 검정
print("stats.kuskal 방식: ",stats.kruskal(group1,group2,group3),'\n')
#welch's ANOVA - 등분산 가정 불필요
print("ANOVA 방식: ", stats.f_oneway(group1,group2,group3,equal_var=False),'\n')


# 검정 방법을 제공하는 라이브러리는 다양함
# 예를 들어 다른 라이브러리로 welch's ANOVA 검정
# pip install pingouin

from pingouin import welch_anova
print("pingouin 라이브러리 활용\n",welch_anova(dv='AMT',between='ta_gubun',data=data))

print("===사후검정===")
from statsmodels.stats.multicomp import pairwise_tukeyhsd
tukResult = pairwise_tukeyhsd(endog=spp['AMT'], groups=spp['ta_gubun']) # df.region= df['region] 둘이 같음
print("tukResult 결과",tukResult,'\n')

# 시각화
tukResult.plot_simultaneous(xlabel='매출액평균',ylabel='온도')
plt.show()
# 그래프의 가로 실선이 겹치지 않으면 귀무 기각