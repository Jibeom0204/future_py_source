# 이원카이제곱(chi-square test of independence)-교차분할표이용
# : 두개이상의변인(집단또는범주)을 대상으로 검정을 수행한다.
# 분석대상의 집단수에 의해서 독립성 검정과 동질성 검정으로 나뉜다.

# 독립성(관련성)검정- 동일집단의 두변인(학력수준과대학진학여부)을 대상으로 관련성이 있는가 없는가?
# 독립성 검정은 두 변수 사이의 연관성을 검정한다.

# 실습: 교육수준과 흡연율 간의 관련성 분석: smoke.csv

# 귀무: 교육수준과 흡연율 간의 관련가 없디.(독립이다. 연관성이 없다)
# 대립: 교육수준과 흡연율 간의 관련가 있다.(독립이 아니다. 연관성이 있다)
import pandas as pd
import scipy.stats as stats
data=pd.read_csv("https://raw.githubusercontent.com/pykwon/python/refs/heads/master/testdata_utf8/smoke.csv")
print(data.head(3))
print(data.tail(3))
print("데이터의 종류들 확인: ",data['education'].unique()) # 데이터의 종류들 확인:  [1 2 3]
print("데이터의 종류들 확인: ",data['smoking'].unique(),'\n\n') # 데이터의 종류들 확인:  [1 2 3]. 범주형임(int 숫자가 아님). 다만 숫자의 형태를 하고 있을 뿐

# 학력 수준별 흡연 빈도 수: 교차표 작성

ctab=pd.crosstab(index=data['education'],columns=data['smoking']) # normalize True하면 비율로. 없으면 빈도수
# ctab=pd.crosstab(index=data['education'],columns=data['smoking'],normalize=True) # normalize True하면 비율로. 없으면 빈도수
ctab.index=['대학원졸','대졸','고졸']
ctab.columns=['과흡연','보통','비흡연']
print(ctab)

# 이원카이제곱(독립성) 검정 시작
#chi_result = [ctab.loc['대학원졸'], ctab.loc['대졸'], ctab.loc['고졸']]
chi_result=ctab # 상동

chi2,pv,dof,expected=stats.chi2_contingency(chi_result)
# 1원일때는 chisquare 2원일때는chi2_contingency
print(f"chi2:{chi2:.7f}, pv:{pv:.7f}, dof:{dof}")
print(f"expected: \n {expected}")

# 판정 1: 유의수준 0.05 < p 0.0008183 이므로 귀무 기각.
# 교육 수준과 흡연율 간에 관계가 있다. smoke.csv(수집자료)는 우연히 발생된 자료가 아니다.

# 판정 2: chi2:18.9109157,dof:4 cd:9.49
# chi2값이 임계치 우측에 있으므로(귀무 기각역) 귀무가설 기각=대립가설 채택

print("\n\n 독립성 검정2-----------------------")
# 남성과 여성의 스포트 음료 선호도 검정

# 귀무: 성별과 음료 선호는 서로 관련이 없다
# 대립: 성별과 음료 선호는 서로 관련이 있다.

# 교차표 생성
data2=pd.DataFrame({
    "포카리 스웨트":[30,20],
    "칠성 사이다":[20,30],
    "비타500":[10,30]
}, index=["남성","여성"])

print(data)

chi2,pv,dof,expected=stats.chi2_contingency(data2)
print("p-value",pv)
print("chi2",chi2)
print("자유도 dof",dof)
print("expected",expected)

# 히트맵 시각화
import matplotlib.pyplot as plt
import koreanize_matplotlib
import seaborn as sns

sns.heatmap(data=data, annot=True, fmt='d', cmap="Blues")
plt.title("성별에 따른 음료 선호 분석")
plt.xlabel("음료 종류")
plt.ylabel("성별")
plt.show()