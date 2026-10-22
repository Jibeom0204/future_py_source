# 표준 편차, 분산의 중요성
# 두반의 시험 성적이 있을 때, 평균이 같다고 성적 분포가 동일한가?
# 실제로 표준 편차의 대소에 따라 성적 편차가 다를 수 있다.

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import koreanize_matplotlib

np.random.seed(42)

# 목표 평균
target_mean=60
std_dev_small=10
std_dev_large=20

# 두 반의 데이터 만들기
class1_raw=np.random.normal(loc=target_mean,scale=std_dev_small,size=100)
class2_raw=np.random.normal(loc=target_mean,scale=std_dev_large,size=100)

print(class1_raw[:5])
print(class2_raw[:5])

# 평균 보정
class1_adj=class1_raw - np.mean(class1_raw)+target_mean
class2_adj=class2_raw - np.mean(class2_raw)+target_mean

# 정수화 및 범위 제한 np.clip(배열 최소 최대값)
class1=np.clip(np.round(class1_adj),10,100).astype(int) # 최소값 10, 최대값 100. int type
class2=np.clip(np.round(class2_adj),10,100).astype(int)
print(class1)
print(class2)

# 통계 계산
mean1,mean2=np.mean(class1), np.mean(class2)
std1,std2=np.std(class1),np.std(class2)
var1,var2=np.var(class1),np.var(class2)

print("1반 (성적 편차자 적음)")
print(f"평균 : {mean1}, 표준편차:{std1}, 분산{var1}")
print("2반 (성적 편차자 적음)")
print(f"평균 : {mean2}, 표준편차:{std2}, 분산{var2}")

# 자료를 파일로 저장
df =pd.DataFrame({
    'class':['1반']*100+["2반"]*100,
    'score':np.concatenate([class1,class2])
}) # 1반 점수 100명, 2반 점수 100명씩 데이터.
# 만든 데이터를 concentrate로 합침

print("시각화--------")
x1=np.random.normal(1,0.05,size=100)
x2=np.random.normal(2,0.05,size=100)

plt.figure(figsize=(10,6))
plt.scatter(x1,class1,alpha=0.8,label=f"1반 평균({mean1:2f},표준편차={std1:2f})")
plt.scatter(x2,class2,alpha=0.8,label=f"2반 평균({mean2:2f},표준편차={std2:2f})")
plt.hlines(target_mean,0.5,2.5,colors='red', linestyles='dashed', label=f"공통평균={target_mean}")
plt.xticks([1,2],["1반","2반"])# X축 눈금(Tick) 위치와 그 자리에 표시될 텍스트 라벨을 사용자 정의 xtick(x축 위치, 라벨 이름)
plt.ylabel("시험 점수")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

plt.figure(figsize=(10,6))
plt.boxplot([class1,class2],label=["1반","2반"])
plt.grid(True)
plt.show()
# 국어 선생님이 말하기를 
# 전통적 주장(귀무가설): 내가 가르치는 학생들 점수는 매년 두 반의 국어점수 평균(편차)에 차이가 없다.
# 누군가가 실험을 통해 데이터를 수집 후 두 반의 평균 점수에 차이가 있다. 라는 새로운 의견 제시
# 대립가설: 두 반의 국어 점수의 평균은 차이가 있다.
# 위 주장에 대해 누가 맞는지 가설 검정을 통해 판정을 내림.(t-test, anova를 사용)

from scipy import stats

# 독립표본 t검정()
t_stat,p_value_t=stats.ttest_ind(class1,class2,equal_var=False) # Welch's test 라고 함
print(f"t-통계값: {t_stat:.4f}")
print(f"p값: {p_value_t:.4f}")

if p_value_t <0.05:
    print("유의확률(p)가 유의수준(α)95% 신뢰구간에서 0.05) 보다 작으므로 두반의 평균은 차이가 있다. 유의하다")
else:
    print("유의확률(p)가 유의수준(α)95% 신뢰구간에서 0.05) 보다 크므로 두반의 평균은 차이가 없다. 유의하지 않다")