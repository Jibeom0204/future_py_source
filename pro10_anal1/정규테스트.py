import MySQLdb
import pandas as pd
import numpy as np
import sys
import numpy as np
import matplotlib.pyplot as plt

# # 칼럼(열)의 이름을 순서대로 "국어", "영어", "수학"으로 변경한다.
# # 아래 문제는 제시한 columns와 index 명을 사용한다.
# # 1) 모든 학생의 수학 점수를 출력하기
# # 2) 모든 학생의 수학 점수의 표준편차를 출력하기
# # 3) 모든 학생의 국어와 영어 점수를 Series 타입이 아니라 DataFrame type으로 출력하기

# from pandas import DataFrame
# data = {"a": [80, 90, 70, 30], "b": [90, 70, 60, 40], "c": [90, 60, 80, 70]}
# df=pd.DataFrame(data)


# df = df.rename(columns={"a":"국어", "b":"영어", "c":"수학"})
# print(df)
# print("수학 점수: \n",df['수학'],'\n')
# print("수학 표준편차: \n",df['수학'].std(),'\n')
# print("국어, 영어:\n",df[['국어','영어']],type(df))


# # 정규분포를 따르는 데이터 1000개를 생성하고, 히스토그램을 그리는 코드를 작성하시오.
# # 요구 조건
# # - 평균 : 0, 표준편차: 1
# # - 구간 : 20개
# # - 투명도 : 0.7
# # - 그래프 제목 : good

# data=np.random.randn(1000)
# df=pd.Series(data)
# df.hist(bins=20, alpha=0.7)
# plt.title='good'
# plt.show()

from pandas import Series,DataFrame
import numpy as np
import pandas as pd
df=pd.read_csv('sales_data.csv')
#날짜,제품,판매수량,가격

# 구조 재구성: year가 행. city가 열
print(df.pivot_table(index=['날짜'],columns=['제품']),'\n')
