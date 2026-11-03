# 회귀분석 문제 3)    
# kaggle.com에서 carseats.csv 파일을 다운 받아 (https://github.com/pykwon 에도 있음) Sales 변수에 영향을 주는 변수들을 선택하여 선형회귀분석을 실시한다.
# 변수 선택은 모델.summary() 함수를 활용하여 타당한 변수만 임의적으로 선택한다.
# 회귀분석모형의 적절성을 위한 조건도 체크하시오.
# 완성된 모델로 Sales를 예측.

#단순선형모델의 적절성 선행 조건 실습 - ols 사용
# 선형성, 정규성, 등분산성, 독립성, 다중공선성 검정을 기본적으로 확인함.

import pandas as pd
import numpy as np
import statsmodels.formula.api as smf
import statsmodels.api
import matplotlib.pyplot as plt
import koreanize_matplotlib 
import seaborn as sns

df = pd.read_csv("https://raw.githubusercontent.com/pykwon/python/refs/heads/master/testdata_utf8/Carseats.csv")
print(df.head(3), df.shape) #(400,11)
print(df.info())
df = df.drop([df.columns[6],df.columns[9],df.columns[10]], axis=1)
print(df.corr())

lm = smf.ols(formula='Sales ~ Income+Advertising+Price+Age', data=df).fit()
print(lm.summary()) #4개의 독립변수가 모두 p값이 0.05보다 작아 유의한 변수임
# skew(왜도 - 0dlaus whkdeocld): 0.218(대체로 대칭적 분포임)
# Kurtosis(첨도): 0.2903(3에 근사하므로 정규분포와 유사)
