import matplotlib.pyplot as plt
import seaborn as sns
import koreanize_matplotlib
import pandas as pd
data=pd.read_csv("수련회 응답.csv")
member=pd.DataFrame(data)
# print("CSV 결과\n",data,type(data),'\n') # dataframe 타입
# print("CSV 데이터 프레임으로\n",member,type(member),'\n') # dataframe 타입

# 컬럼 이름 너무 기니까 변환
member.columns=["제출시간","이름","식사","부분참석","교회","성별","나이","연락처","이동수단","세례여부","참석여부","취침"]
# print(member.columns)

## 이름과 교회와 연락처만 출력

# 에바다만 출력하기_AI
ebada_member = member[member['교회'] == "에바다/김용우 목사님"]
# print(ebada_member)

# print("이름: ",ebada_member["이름"].values, "연락처: ",ebada_member["연락처"].values)

# '이름'과 '연락처' 두 개의 열만 선택해서 출력
print(ebada_member[['이름', '연락처']]) # 너무 쉬웠네 허무하다.