"""[로지스틱 분류분석 문제1]

문1] 소득 수준에 따른 외식 성향을 나타내고 있다. 주말 저녁에 외식을 하면 1, 외식을 하지 않으면 0으로 처리되었다. 
다음 데이터에 대하여 소득 수준이 외식에 영향을 미치는지 로지스틱 회귀분석을 실시하라.
키보드로 소득 수준(양의 정수)을 입력하면 외식 여부 분류 결과 출력하라.
"""
# io 모듈에서 StringIO를 가져온다.
# StringIO: 문자열을 "파일처럼" 읽을 수 있게 감싸주는 도구 (pd.read_csv는 파일을 읽는 함수이기 때문)
from io import StringIO

# pandas 라이브러리를 가져오고, 관례적으로 pd라는 짧은 이름을 붙인다.
import pandas as pd

# 세 줄 따옴표(""")는 여러 줄 문자열을 만드는 문법이다.
# 첫 줄은 열 이름(헤더), 나머지는 데이터이며 값은 쉼표(,)로 구분한다.

raw = """요일,외식유무,소득수준
토,0,57
토,0,39
토,0,28
화,1,60
토,0,31
월,1,42
토,1,54
토,1,65
토,0,45
토,0,37
토,1,98
토,1,60
토,0,41
토,1,52
일,1,75
월,1,45
화,0,46
수,0,39
목,1,70
금,1,44
토,1,74
토,1,65
토,0,46
토,0,39
일,1,60
토,1,44
일,0,30
토,0,34
"""

# pd.read_csv(): 쉼표로 구분된 텍스트를 표(DataFrame)로 변환하는 함수
#   첫 번째 인자 StringIO(raw): 읽을 대상. 문자열 raw를 파일처럼 감싼 것
#   dtype={...}: 열별로 저장할 자료형을 직접 지정하는 인자 (딕셔너리 형태: {열이름: 자료형})
df = pd.read_csv(
    StringIO(raw),
    dtype={"외식유무": "int8", "소득수준": "int64"},
)

# 요일은 값의 종류가 7개로 정해져 있으므로 category 형으로 바꾼다.
#   pd.Categorical(값들, categories=[...], ordered=True)
#     categories: 허용할 값의 목록이자 순서
#     ordered=True: 월<화<...<일 순서가 있다고 지정 (정렬할 때 가나다순이 아니라 요일순이 됨)
df["요일"] = pd.Categorical(
    df["요일"],
    categories=["월", "화", "수", "목", "금", "토", "일"],
    ordered=True,
)
print(df.head())       # head(): 위에서 5행만 출력 (인자로 개수 지정 가능, 예: head(10))
print(df.shape)        # shape: (행 수, 열 수) 튜플 -> (28, 3)이 나와야 정상
print(df.dtypes)       # dtypes: 열별 자료형 확인

import numpy as np
import statsmodels.formula.api as smf

fomula='외식유무~소득수준'
result= smf.logit(formula=fomula, data=df).fit()
print(result.summary())

# 예측값
pred=result.predict(df)

print("'\n\n예측값 : ",pred[:5].values)
print("실제값: ",df[:5].values)

from sklearn.metrics import accuracy_score
pred=result.predict(df)
print('분류정확도 :' , accuracy_score(df['외식유무'],np.around(pred)))

# 사용자 입력
income=int(input("소득수준을 입력: "))
new_df=pd.DataFrame(income)
"""
# **모델 작성 방법1** : logit()이용
formula = '외식유무 ~ 소득수준'
# 범주형(종속변수) ~ 연속형(독립변수) 설정

result = smf.logit(formula=formula, data = data).fit()

print(result.summary()) # ols표와 같은 형태가 나온다.
# 결과 : 
#                            Logit Regression Results                           
# ==============================================================================
# Dep. Variable:                외식유무   No. Observations:                   21
# Model:                          Logit   Df Residuals:                       19
# Method:                           MLE   Df Model:                            1
# Date:                Wed, 04 Nov 2026   Pseudo R-squ.:                  0.6240
# Time:                        12:40:42   Log-Likelihood:                -5.4648
# converged:                       True   LL-Null:                       -14.532
# Covariance Type:            nonrobust   LLR p-value:                 2.058e-05
# ==============================================================================
#                  coef    std err          z      P>|z|      [0.025      0.975]
# ------------------------------------------------------------------------------
# Intercept    -11.8668      4.982     -2.382      0.017     -21.632      -2.102
# 소득수준       0.2375      0.100      2.366      0.018       0.041       0.434
# ==============================================================================

logit_pred = result.predict(data[:10])

print('logit 예측값 : ', np.around(logit_pred.values))
print('logit 실제값 : ', data['외식유무'][:10].values)
# 결과 : 
# logit 예측값 :  [1. 0. 0. 0. 1. 1. 0. 0. 1. 1.]
# logit 실제값 :  [0  0  0  0  1  1  0  0  1  1]



# **모델 작성 방법2** : glm()이용
result2 = smf.glm(formula = formula, data=data, family=sm.families.Binomial()).fit()

print(result2.summary())
# 결과 : 
#                  Generalized Linear Model Regression Results                  
# ==============================================================================
# Dep. Variable:                외식유무   No. Observations:                   21
# Model:                            GLM   Df Residuals:                       19
# Model Family:                Binomial   Df Model:                            1
# Link Function:                  Logit   Scale:                          1.0000
# Method:                          IRLS   Log-Likelihood:                -5.4648
# Date:                Wed, 04 Nov 2026   Deviance:                       10.930
# Time:                        12:40:42   Pearson chi2:                     11.7
# No. Iterations:                     7   Pseudo R-squ. (CS):             0.5783
# Covariance Type:            nonrobust                                         
# ==============================================================================
#                  coef    std err          z      P>|z|      [0.025      0.975]
# ------------------------------------------------------------------------------
# Intercept    -11.8668      4.982     -2.382      0.017     -21.632      -2.102
# 소득수준        0.2375      0.100      2.366      0.018       0.041       0.434
# ==============================================================================
glm_pred = result2.predict(data[:10])

print('glm 예측값 : ', np.around(glm_pred.values))
print('glm 실제값 : ', data['외식유무'][:10].values)
# 결과 : 
# glm 예측값 :  [1. 0. 0. 0. 1. 1. 0. 0. 1. 1.]
# glm 실제값 :  [0  0  0  0  1  1  0  0  1  1]


# 평가 - 모델의 학습과 통계적 적합도 평가 : 가능성(우도)
#      - 분류 정확도 확인 - confusion-matrix
#                        - accuracy_score()를 사용한다

# [분류 정확도 확인방법1 : confusion-matrix(수치에 대한 집계표(혼동 행렬)) - logit()사용]
conf_tab = result.pred_table()
print(conf_tab)
# 결과 : 
#      [[10.  1.]
#       [ 1.  9.]]

print('분류 정확도(logit) : ', (conf_tab[0][0] + conf_tab[1][1]) / len(data))
# 분류 정확도(logit) :  0.9047619047619048

# [분류 정확도 확인방법2 : accuracy_score()이용) - glm()사용]
from sklearn.metrics import accuracy_score
pred2 = result2.predict(data)
print('분류 정확도(glm) : ', accuracy_score(data['외식유무'], np.around(pred2)))
# 분류 정확도(glm) :  0.9047619047619048



# 새로운 값으로 예측하기 ----------------
newdf = pd.DataFrame()
newdf['소득수준'] = [23, 46, 92, 124, 0]
print(newdf)

# glm()모델에 새로운 newdf를 넣기
new_pred = result2.predict(newdf) 

print('예측결과 : ', np.rint(new_pred.values))  
# 시그모이드를 거친 확률(0~1)을 반올림해서 0 또는 1로 분류
# 결과 : 예측결과 :  [0.  0.  1.  1.  0.]
# 해석 : 소득수준이 23, 46, 0인 집안은 주말외식을 못하고 92, 124인 집안은 주말외식을 진행한다.

"""