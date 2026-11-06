"""
Logistic Regression(로지스틱 회귀분석): 정성적 분류 모델
선형결합을 로그오즈(LOGIT())로 해석하고 이를 시그모이드 함수를 통해 확률로 변환
이항분류(다항분류도 가능)-독립변수(feature)가 연속형, 범주형 모두 가smd, 종속변수(label,class)
참고: Logistic Regression을 근거로 뉴럴넷의 뉴런이 사용
"""

#mtcars dataset을 사용
import statsmodels.api as sm

mtcarsdata=sm.datasets.get_rdataset("mtcars")
print(mtcarsdata.keys())
mtcars=mtcarsdata.data
print(mtcars.head(2))
print(mtcars.info(),'\n')

# 연비와 마력수에 다른 변속기 분류(수동,자동)
mtcar = mtcars.loc[:,['mpg', 'hp','am']]
print("mtcar.head(3)")
print(mtcar['am'].unique()) #[1수동 0자동]

# 모델 작성 방법 1: logit()
print("==============모델 작성 방법 1: logit()==============" \
"======================================================================")
import numpy as np
import statsmodels.formula.api as smf
# statsmodels.formula.api: 가져올 대상의 경로 (점 '.'은 "안쪽에 있는"이라는 뜻)
#   - statsmodels : 통계 모델링 라이브러리 (회귀, 로지스틱 회귀, 시계열 등)
#   - formula     : statsmodels 안의 "수식 문자열" 관련 하위 패키지
#   - api         : 자주 쓰는 함수들을 모아 놓은 공개용 창구 모듈
# as smf: 긴 이름 대신 'smf'라는 별명을 붙여 쓰겠다는 뜻 (관례적인 별명)

fomula='am~hp+mpg' #am  : '~' 왼쪽 = 종속변수(예측하려는 값)hp  : 독립변수 1 (설명 변수)+mpg : 독립변수 2
result= smf.logit(formula=fomula, data=mtcar).fit()
print(result.summary()) # hp,mpg가 am에 끼치는 영향. P>|z|를 보고 판단할 수 있다. 0.05보다 작으면 유의. 영향을 준다
#                            Logit Regression Results                           
# ==============================================================================
# Dep. Variable:                     am   No. Observations:                   32
# Model:                          Logit   Df Residuals:                       29
# Method:                           MLE   Df Model:                            2
# Date:                Wed, 04 Nov 2026   Pseudo R-squ.:                  0.5551
# Time:                        10:19:23   Log-Likelihood:                -9.6163
# converged:                       True   LL-Null:                       -21.615
# Covariance Type:            nonrobust   LLR p-value:                 6.153e-06
# ==============================================================================
#                  coef    std err          z      P>|z|      [0.025      0.975]
# ------------------------------------------------------------------------------
# Intercept    -33.6052     15.077     -2.229      0.026     -63.156      -4.055
# hp             0.0550      0.027      2.045      0.041       0.002       0.108
# mpg            1.2596      0.567      2.220      0.026       0.147       2.372
# ==============================================================================

pred=result.predict(mtcar[:10])#mtcar의 모든 행 중 10개 열만.
print("'\n\n예측값 : ",pred.values) #예측값 :  [0.25004729 0.25004729 0.5580
print("np around 예측값 : ",np.around(pred.values)) # 0.5기준으로 0,1 을 출력
print("실제값 : ",mtcar['am'][:10].values,'\n\n')
# np around 예측값 :  [0. 0. 1. 0. 0. 0. 0. 1. 1. 0.]
# 실제값 :            [1  1  1  0  0  0  0  0  0  0]

"""
혼동 행렬(Confusion Matrix, 오차 행렬)은 인공지능이나 머신러닝의 분류(Classification) 모델이 예측한 결과가
실제 정답과 얼마나 맞고 틀렸는지를 4가지 경우의 수로 정리한 2×2 표
"""
print('========수치에 대한 집계표(혼동 행렬)========\n')

print('========현재 모델의 분류 정확도 확인방법 1: Confusion Matrix 이용========\n')
conf_tab=result.pred_table()
print(conf_tab,'\n')
#                                         예측
#                         positive                     negative
# 실제 참:                  [[16.                         3.]        
# 실제 거짓:                [ 3.                          10.]]
# 1. 실제 참을 모델이 참으로 맞춤               2. 실제 참을 모델이 거짓으로 잘못 예측(2종 오류)
# 3. 실제 거짓을 모델이 참으로 맞춤(1종 오류)    4. 실제 거짓을 모델이 거짓이라고 맞힘

print('분류 정확도1 : ',(16+10)/len(mtcar))
print('분류 정확도2 : ',(conf_tab[0][0] + conf_tab[1][1]) / len(mtcar),'\n\n') # 실제 맞춘값만 사용하기


print('========현재 모델의 분류 정확도 확인방법 2: accuracy_score(실제값, 예측값) 이용========\n')
from sklearn.metrics import accuracy_score,confusion_matrix
pred2=result.predict(mtcar)


# 예측 확률을 클래스(0 또는 1)로 변환
pred_class = (pred2 > 0.5).astype(int)
conf_mat=confusion_matrix(mtcar['am'],pred_class) # am은 실제갑, pre_class는 예측값
print("confusion_matrix 혼동행렬:\n", conf_mat)
print("분류 정확도: ", accuracy_score(mtcar['am'],np.around(pred2)))


print('분류정확도 :' , accuracy_score(mtcar['am'],np.around(pred2)))
print("==============logit() 끝끝==============" \
"======================================================================\n\n\n\n")




print("==============모델 작성 방법 2: glm(): 일반화된 선형 모델. pred_table 지원 x==============" \
"======================================================================")
result2=smf.glm(formula=fomula, data=mtcar,family=sm.families.Binomial()).fit()
#family=sm.families.Binomial:이항분포, Gaician: 정규분포-기본값
print(result2.summary())

glm_pred=result2.predict(mtcar[:10]) # 이항분포의 로지스틱 회귀값 저장하는 변수 내에 들어간 값을 예측하는 메서드 사용
print('glm 예측값: ',np.around(glm_pred.values))
print('glm 실제값: ',mtcar['am'][:10].values)

glm_pred2=result2.predict(mtcar) #d
print('glm 분류 정확도: ', accuracy_score(mtcar['am'],np.around(glm_pred2)),'\n')
#logit(): 로지스틱 회귀 전용 모델, 이진 분류
# glm(): 일반화 선형 모델, 이진 분류/개수 데이터 등, 연결함수는 분포에 따라 지정

print("새로운 값으로 예측하기====")
import pandas as pd
newdf=pd.DataFrame()
newdf['mpg']=[10,30,120,130]
newdf['hp']=[100,110,80,130]
print(newdf)
new_pred=result2.predict(newdf)# 이항분포의 로지스틱 회귀값 저장하는 변수 내에 들어간 값을 예측하는 메서드 사용
print("예측결과: ",np.around(new_pred.values)) # 소수점 지정 가능
print("예측결과: ",np.rint(new_pred.values)) # 소수점 지정 불가

# 머신러닝의 포용성
# 머신러닝 모델을 평가할 때 훈련 데이터의 100% 정확도라는 숫자에 집착하기보다
# 이 모델이 현실의 불확실성과 다양한 변수를 얼마나 유연하게 포용할 수 있는가를 고려해야 함
# 수학에서는 100%의 답을 원하지만 ML은 95%가 될지라도 주변값을 포용하도록 하는 것이 중요함
# 예를 들어 고양이 분류 모델이 경우 꼬리가 없는 고양이도 분류할 수 있어야 한다. 

"""모델의 일반화
편향-분산 트레이드 오프
상반관계: 편향과 분산은 일반적으로 반비례 관계에 있다
모델을 단순하게 만들면 편햐잉 커지고 분산이 작아짐(과소적합 위험).
모델을 복잡하게 만들면 편향이 작아지고 분산이 커짐(과적합 위험)
목표: 편향과 분사의 합(총 오차)이 최소가 되는 지점, 즉 일반화 성능이 가장 좋은 최적의 모델 복잡도를 찾는 것

좋은 모델은 포용성이 있는 일반화 된 모델이다.
"""