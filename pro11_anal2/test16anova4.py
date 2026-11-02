# # 이원분산분석(two-way ANOVA)  ---------------------------
# 독립변인의 수가 두 개 이상일 때 집단 간 차이가 유의한지를 검증하는 데 사용한다. 
# 상호작용효과(Interaction effect) : 한 변수의 변화가 결과에 미치는 영향이 다른 변수의 수준에 따라 달라지는지를 확인하기 위해 사용된다.

# - 두 개의 요인에 대한 집단(독립변수) 각각이 종속변수(평균)에 영향을 주는지 검정
# - 주효과(개별효과) : 독립변수들이 각각 독립적으로 종속변수에 미치는 영향을 검정하는 것
# - 상호작용효과(교호작용) : 독립변수들이 서로 연관되어 종속변수에 미치는 영향을 검정하는 것
#                         한 독립변수가 종속변수에 미치는 영향이 다른 독립변수의 수준에 따라 달라지는 현상

# 예시
# a: 감기약을 먹으면 증상이 완화
# b: 물을 마시는 것은 건강에 문제가 없음
# 교호: 감기약을 물과 마시면 상관 없지만 술이랑 먹으면 치명적
# 약의 효과가 같이 복용한 음료 종류에 따라 달라짐

# 실습: 독의 종류와 처치방법에 따라 실험 동물의 평균 생존 시간에 차이가 있는가 검증

import pandas as pd
import numpy as np
import seaborn as sns
import scipy.stats as stats
import matplotlib.pyplot as plt
import koreanize_matplotlib
import urllib.request

from statsmodels.formula.api import ols 
from statsmodels.stats.anova import anova_lm
from statsmodels.stats.multicomp import pairwise_tukeyhsd


data=pd.read_csv("https://raw.githubusercontent.com/pykwon/python/refs/heads/master/testdata_utf8/poison_treat.csv",index_col=0)
# 첫번째 열(index 0)을 dataframe의 인덱스로사용

print(data.head(3))
print(data.shape)
"""
데이터 설명.txt
100%
# 데이터 설명
# - poison : 독의 종류 (3개 수준)
# - treat  : 처치방법 (4개 수준)
# - time   : 독에 노출된 실험동물의 생존시간
#
# 독 3종류 × 처치방법 4종류 = 12개 조합
# 각 조합에서 실험동물 4마리 관측 → 총 48개 자료
# 독이 퍼지는 시간이 아니라 '생존시간'을 분석함

# [주효과 가설 1 : 독의 종류]
# 귀무(H0) : 독의 종류에 따른 평균 생존시간은 모두 같다.
# 대립(H1) : 독의 종류에 따른 평균 생존시간 중 적어도 하나는 다르다.

# [주효과 가설 2 : 처치방법]
# 귀무(H0) : 처치방법에 따른 평균 생존시간은 모두 같다.
# 대립(H1) : 처치방법에 따른 평균 생존시간 중 적어도 하나는 다르다.

# [교호작용 가설]
# 귀무(H0) : 독의 종류와 처치방법 간 교호작용은 없다.
# 대립(H1) : 독의 종류와 처치방법 간 교호작용은 있다.
# 교호작용이 있다는 의미: 처치방법에 따른 생존시간 차이가 독의 종류에 따라 달라짐

# 주효과: 각각의 독립변수에 따라 종속변수의 평균이 달라지는가?
# 교호작용: 한 독립변수에 따른 평균 차이가 다른 독립변수의 수준에 따라 달라지는가?

"""

# 요인별 표본 수 확인
print("독 종류별 표본 수: ",data.groupby('poison').size())
print("처치 방법별 표본 수: ",data.groupby('treat').size())
print("독 종류 * 처치 방법 수: ",data.groupby(['poison','treat']).size(),'\n')
# 모든 조합에서 표본 수가 4로 동일함. 균형적인 설계가 되어있는 데이터

print("====요인별 기술통계====")

print("독 종류별 평균 생존시간: \n",data.groupby('poison')['time'].agg(['count','mean']),'\n')
print("처치 방법별 종류별 평균 생존시간: \n",data.groupby('treat')['time'].agg(['count','mean']),'\n')

# 이원분산분석=====
model=ols('time~C(poison) * C(treat)',data=data).fit() # C: 범주형 데이터를 의미함. * :주효과+교호작용 분석
#ols('종속변수 ~ C(요인1) + C(요인2)', data=...)  → 주효과만 분석 ++++
#ols('종속변수 ~ C(요인1) * C(요인2)', data=...)   → 주효과 + 교호작용 분석 ****
result=anova_lm(model,type=2)
print("이원 분산 분석 결과\n",result,'\n')

# 해석
p_poison=result.loc['C(poison)','PR(>F)']
p_treat=result.loc['C(treat)','PR(>F)']
p_interaction=result.loc['C(poison):C(treat)','PR(>F)']
alpha=0.05

if p_poison <alpha:
    print("독 종류: 귀무기각 => 독의 종류에 따라 평균 생존 시간에 유의한 차이가 존재")
else:
    print("독 종류: 귀무채택 => 우연히 발생한 데이터")


if p_treat <alpha:
    print("처치방법: 귀무기각 => 처치방법에 따라 평균 생존 시간에 유의한 차이가 존재")
else:
    print("처치방법: 귀무채택 => 우연히 발생한 데이터")


if p_interaction <alpha:
    print("교호작용: 귀무기각 => 독의 종류에 따라 처치 방법의 효과가 다름")
else:
    print("교호작용: 귀무채택 => 독 종류에 따라 처치방법 효과가 다르다는 주장의 근거가 부족함")



# 사후 검정(post-hoc test)
print("\n ========독 종류별 사후검정======== \n")

tkResult1=pairwise_tukeyhsd(endog=data['time'],groups=data['poison'],alpha=0.05)
print(tkResult1)
tkResult1.plot_simultaneous(xlabel="평균생존시간",ylabel="독 종류")
plt.title("독 종류별 생존 시간")
plt.show()
plt.close()


print("\n ========처치방법 종류별 사후검정======== \n")
tkResult2=pairwise_tukeyhsd(endog=data['time'],groups=data['treat'],alpha=0.05)
print(tkResult2)
tkResult2.plot_simultaneous(xlabel="평균생존시간",ylabel="처치방법")
plt.title("처치방법별 생존 시간")
plt.show()
plt.close()


"""
■■■블로그 정리■■■

일원 카이제곱 검정 (적합도 검정): 단일 범주형 변수에 대해, 실제 관측된 데이터의 빈도가 사전에 기대했던 이론적 빈도(비율)와 일치하는지 검정합니다.
(예: 특정 지역의 혈액형 분포가 국가 표준 분포와 같은가)

이원 카이제곱 검정 (독립성/동질성 검정): 두 개의 범주형 변수 교차표 상에서 두 변수 간에 통계적인 연관성이 있는지(독립적인지) 검정합니다.
(예: 성별에 따라 선호하는 정당에 차이가 있는가)

일원 분산분석 (One-way ANOVA): 하나의 범주형 독립변수(3개 이상의 집단)에 따라 연속형 종속변수의 평균에 유의미한 차이가 있는지 검정합니다.
(예: 3가지 다이어트 약물에 따른 체중 감량 수치의 차이)

이원 분산분석 (Two-way ANOVA): 두 개의 범주형 독립변수가 연속형 종속변수에 미치는 각각의 주효과(Main effect)와
두 변수가 결합할 때 발생하는 상호작용 효과(Interaction effect)를 동시에 검정합니다.
(예: 약물 종류와 환자 성별이 체중 감량에 미치는 영향)
"""